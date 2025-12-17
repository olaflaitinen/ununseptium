"""KYC workflow orchestration.

Provides workflow management for KYC verification processes,
coordinating multiple verification steps and tracking state.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    pass


class WorkflowState(str, Enum):
    """State of a KYC workflow."""

    CREATED = "created"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class StepStatus(str, Enum):
    """Status of a workflow step."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStep(BaseModel):
    """A step in a KYC workflow.

    Attributes:
        id: Unique step identifier.
        name: Step name.
        step_type: Type of verification step.
        status: Current step status.
        required: Whether step is required.
        order: Execution order.
        input_data: Data passed to the step.
        output_data: Data produced by the step.
        error_message: Error message if failed.
        started_at: When step started.
        completed_at: When step completed.
    """

    id: str = Field(default_factory=lambda: f"STEP-{uuid4().hex[:8].upper()}")
    name: str
    step_type: str
    status: StepStatus = StepStatus.PENDING
    required: bool = True
    order: int = 0
    input_data: dict[str, Any] = Field(default_factory=dict)
    output_data: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def start(self) -> None:
        """Mark step as started."""
        self.status = StepStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()

    def complete(self, output_data: dict[str, Any] | None = None) -> None:
        """Mark step as completed.

        Args:
            output_data: Optional output data from step.
        """
        self.status = StepStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        if output_data:
            self.output_data = output_data

    def fail(self, error_message: str) -> None:
        """Mark step as failed.

        Args:
            error_message: Error description.
        """
        self.status = StepStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error_message = error_message

    def skip(self) -> None:
        """Mark step as skipped."""
        self.status = StepStatus.SKIPPED
        self.completed_at = datetime.utcnow()


class WorkflowResult(BaseModel):
    """Result of a completed workflow.

    Attributes:
        workflow_id: ID of the workflow.
        identity_id: ID of the verified identity.
        state: Final workflow state.
        steps: All workflow steps.
        verification_result: Final verification result.
        decision: Workflow decision.
        decision_reason: Reason for decision.
        completed_at: Completion timestamp.
        metadata: Additional workflow data.
    """

    workflow_id: str
    identity_id: str
    state: WorkflowState
    steps: list[WorkflowStep] = Field(default_factory=list)
    verification_result: dict[str, Any] | None = None
    decision: str = "pending"
    decision_reason: str | None = None
    completed_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KYCWorkflow(BaseModel):
    """KYC verification workflow.

    Orchestrates the complete KYC verification process including
    identity verification, document validation, and screening.

    Attributes:
        id: Unique workflow identifier.
        identity_id: ID of the identity being verified.
        state: Current workflow state.
        steps: List of workflow steps.
        current_step_index: Index of current step.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
        metadata: Additional workflow data.

    Example:
        ```python
        from ununseptium.kyc import KYCWorkflow, Identity

        identity = Identity(name="John Smith")

        workflow = KYCWorkflow.create_standard(identity.id)
        workflow.start()

        while not workflow.is_complete():
            step = workflow.current_step()
            # Execute step...
            workflow.complete_current_step({"result": "success"})

        result = workflow.get_result()
        ```
    """

    id: str = Field(default_factory=lambda: f"WF-{uuid4().hex[:12].upper()}")
    identity_id: str
    state: WorkflowState = WorkflowState.CREATED
    steps: list[WorkflowStep] = Field(default_factory=list)
    current_step_index: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def create_standard(cls, identity_id: str) -> KYCWorkflow:
        """Create a standard KYC workflow.

        Args:
            identity_id: ID of the identity to verify.

        Returns:
            Configured KYCWorkflow instance.
        """
        steps = [
            WorkflowStep(
                name="Identity Verification",
                step_type="identity_verification",
                order=1,
                required=True,
            ),
            WorkflowStep(
                name="Document Validation",
                step_type="document_validation",
                order=2,
                required=True,
            ),
            WorkflowStep(
                name="Sanctions Screening",
                step_type="sanctions_screening",
                order=3,
                required=True,
            ),
            WorkflowStep(
                name="Risk Assessment",
                step_type="risk_assessment",
                order=4,
                required=True,
            ),
        ]

        return cls(identity_id=identity_id, steps=steps)

    @classmethod
    def create_enhanced(cls, identity_id: str) -> KYCWorkflow:
        """Create an enhanced KYC workflow with additional checks.

        Args:
            identity_id: ID of the identity to verify.

        Returns:
            Configured KYCWorkflow instance.
        """
        steps = [
            WorkflowStep(
                name="Identity Verification",
                step_type="identity_verification",
                order=1,
                required=True,
            ),
            WorkflowStep(
                name="Document Validation",
                step_type="document_validation",
                order=2,
                required=True,
            ),
            WorkflowStep(
                name="Address Verification",
                step_type="address_verification",
                order=3,
                required=True,
            ),
            WorkflowStep(
                name="Sanctions Screening",
                step_type="sanctions_screening",
                order=4,
                required=True,
            ),
            WorkflowStep(
                name="PEP Screening",
                step_type="pep_screening",
                order=5,
                required=True,
            ),
            WorkflowStep(
                name="Adverse Media Check",
                step_type="adverse_media",
                order=6,
                required=False,
            ),
            WorkflowStep(
                name="Risk Assessment",
                step_type="risk_assessment",
                order=7,
                required=True,
            ),
        ]

        return cls(identity_id=identity_id, steps=steps)

    def start(self) -> None:
        """Start the workflow execution."""
        if self.state != WorkflowState.CREATED:
            msg = f"Cannot start workflow in state: {self.state}"
            raise ValueError(msg)

        self.state = WorkflowState.IN_PROGRESS
        self.updated_at = datetime.utcnow()

        if self.steps:
            self.steps[0].start()

    def current_step(self) -> WorkflowStep | None:
        """Get the current step.

        Returns:
            Current WorkflowStep or None if complete.
        """
        if self.current_step_index >= len(self.steps):
            return None
        return self.steps[self.current_step_index]

    def complete_current_step(
        self,
        output_data: dict[str, Any] | None = None,
    ) -> bool:
        """Complete the current step and advance.

        Args:
            output_data: Output data from step execution.

        Returns:
            True if workflow continues, False if complete.
        """
        step = self.current_step()
        if step is None:
            return False

        step.complete(output_data)
        self.updated_at = datetime.utcnow()

        # Move to next step
        self.current_step_index += 1

        if self.current_step_index < len(self.steps):
            self.steps[self.current_step_index].start()
            return True

        # Workflow complete
        self._complete_workflow()
        return False

    def fail_current_step(self, error_message: str) -> None:
        """Fail the current step.

        Args:
            error_message: Error description.
        """
        step = self.current_step()
        if step is None:
            return

        step.fail(error_message)
        self.updated_at = datetime.utcnow()

        if step.required:
            self.state = WorkflowState.REJECTED
        else:
            # Skip optional step and continue
            step.status = StepStatus.SKIPPED
            self.current_step_index += 1
            if self.current_step_index < len(self.steps):
                self.steps[self.current_step_index].start()

    def skip_current_step(self) -> bool:
        """Skip the current step if optional.

        Returns:
            True if skipped, False if required.
        """
        step = self.current_step()
        if step is None:
            return False

        if step.required:
            return False

        step.skip()
        self.current_step_index += 1
        self.updated_at = datetime.utcnow()

        if self.current_step_index < len(self.steps):
            self.steps[self.current_step_index].start()

        return True

    def is_complete(self) -> bool:
        """Check if workflow is complete.

        Returns:
            True if workflow has finished.
        """
        return self.state in {
            WorkflowState.APPROVED,
            WorkflowState.REJECTED,
            WorkflowState.CANCELLED,
            WorkflowState.EXPIRED,
        }

    def cancel(self, reason: str | None = None) -> None:
        """Cancel the workflow.

        Args:
            reason: Cancellation reason.
        """
        self.state = WorkflowState.CANCELLED
        self.updated_at = datetime.utcnow()
        if reason:
            self.metadata["cancellation_reason"] = reason

    def get_result(self) -> WorkflowResult:
        """Get the workflow result.

        Returns:
            WorkflowResult with final state and data.
        """
        # Aggregate step outputs
        step_outputs = {step.step_type: step.output_data for step in self.steps}

        # Determine decision
        decision = "pending"
        if self.state == WorkflowState.APPROVED:
            decision = "approved"
        elif self.state == WorkflowState.REJECTED:
            decision = "rejected"
        elif self.state == WorkflowState.CANCELLED:
            decision = "cancelled"

        return WorkflowResult(
            workflow_id=self.id,
            identity_id=self.identity_id,
            state=self.state,
            steps=self.steps,
            verification_result=step_outputs.get("risk_assessment"),
            decision=decision,
            completed_at=self.updated_at if self.is_complete() else None,
            metadata=self.metadata,
        )

    def _complete_workflow(self) -> None:
        """Complete workflow and determine final state."""
        # Check for any failed required steps
        failed_required = any(
            step.status == StepStatus.FAILED and step.required for step in self.steps
        )

        if failed_required:
            self.state = WorkflowState.REJECTED
        else:
            # Check risk assessment output
            risk_step = next(
                (s for s in self.steps if s.step_type == "risk_assessment"),
                None,
            )

            if risk_step and risk_step.output_data.get("needs_review"):
                self.state = WorkflowState.PENDING_REVIEW
            else:
                self.state = WorkflowState.APPROVED

        self.updated_at = datetime.utcnow()
