"""Physics constraints for Scientific ML.

Provides constraint interfaces for enforcing physical laws.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

import numpy as np
from pydantic import BaseModel, Field


class ConstraintResult(BaseModel):
    """Result of constraint evaluation.

    Attributes:
        satisfied: Whether constraint is satisfied.
        violation: Magnitude of violation.
        residual: Residual values at points.
        message: Description of violation.
    """

    satisfied: bool
    violation: float = 0.0
    residual: np.ndarray = Field(default_factory=lambda: np.array([]))
    message: str = ""

    model_config = {"arbitrary_types_allowed": True}


class PhysicsConstraint(ABC):
    """Abstract base for physics constraints.

    Constraints can be used as loss terms or hard constraints
    during training and inference.
    """

    @abstractmethod
    def evaluate(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> ConstraintResult:
        """Evaluate constraint.

        Args:
            prediction: Model predictions.
            inputs: Input data.

        Returns:
            ConstraintResult.
        """
        ...

    @abstractmethod
    def loss(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> float:
        """Compute constraint loss term.

        Args:
            prediction: Model predictions.
            inputs: Input data.

        Returns:
            Loss value.
        """
        ...


class SoftConstraint(PhysicsConstraint):
    """Soft constraint enforced via loss penalty.

    Example:
        ```python
        from ununseptium.ai.sciml import SoftConstraint
        import numpy as np

        # Conservation constraint: sum should be constant
        def conservation_fn(pred, inputs):
            return np.sum(pred) - inputs[0, -1]  # Last input is target sum

        constraint = SoftConstraint(
            name="mass_conservation",
            constraint_fn=conservation_fn,
            weight=10.0
        )

        pred = np.array([0.3, 0.3, 0.4])
        inputs = np.array([[0, 0, 1.0]])

        result = constraint.evaluate(pred, inputs)
        loss = constraint.loss(pred, inputs)
        ```
    """

    def __init__(
        self,
        name: str,
        constraint_fn: Callable[[np.ndarray, np.ndarray], np.ndarray | float],
        weight: float = 1.0,
        tolerance: float = 1e-6,
    ) -> None:
        """Initialize soft constraint.

        Args:
            name: Constraint name.
            constraint_fn: Function computing residual (should be ~0).
            weight: Loss weight.
            tolerance: Tolerance for satisfaction.
        """
        self.name = name
        self.constraint_fn = constraint_fn
        self.weight = weight
        self.tolerance = tolerance

    def evaluate(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> ConstraintResult:
        """Evaluate constraint."""
        residual = self.constraint_fn(prediction, inputs)

        if isinstance(residual, np.ndarray):
            violation = float(np.mean(np.abs(residual)))
            residual_arr = residual
        else:
            violation = abs(residual)
            residual_arr = np.array([residual])

        satisfied = violation <= self.tolerance

        return ConstraintResult(
            satisfied=satisfied,
            violation=violation,
            residual=residual_arr,
            message="" if satisfied else f"{self.name}: violation={violation:.6f}",
        )

    def loss(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> float:
        """Compute weighted loss."""
        residual = self.constraint_fn(prediction, inputs)

        if isinstance(residual, np.ndarray):
            return float(self.weight * np.mean(residual**2))
        return float(self.weight * residual**2)


class BoundConstraint(PhysicsConstraint):
    """Constraint on prediction bounds.

    Example:
        ```python
        from ununseptium.ai.sciml import BoundConstraint

        # Predictions must be non-negative
        constraint = BoundConstraint(lower=0.0)

        pred = np.array([0.1, -0.2, 0.3])
        result = constraint.evaluate(pred, np.array([]))
        ```
    """

    def __init__(
        self,
        lower: float | None = None,
        upper: float | None = None,
        weight: float = 100.0,
    ) -> None:
        """Initialize bound constraint.

        Args:
            lower: Lower bound.
            upper: Upper bound.
            weight: Penalty weight.
        """
        self.lower = lower
        self.upper = upper
        self.weight = weight

    def evaluate(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> ConstraintResult:
        """Evaluate bound constraint."""
        violations = []

        if self.lower is not None:
            lower_violations = np.maximum(0, self.lower - prediction)
            violations.append(lower_violations)

        if self.upper is not None:
            upper_violations = np.maximum(0, prediction - self.upper)
            violations.append(upper_violations)

        if violations:
            total_violation = sum(np.sum(v) for v in violations)
            satisfied = total_violation == 0
        else:
            total_violation = 0.0
            satisfied = True

        return ConstraintResult(
            satisfied=satisfied,
            violation=float(total_violation),
            message="" if satisfied else f"Bound violation: {total_violation:.6f}",
        )

    def loss(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> float:
        """Compute penalty loss for violations."""
        loss = 0.0

        if self.lower is not None:
            violations = np.maximum(0, self.lower - prediction)
            loss += np.sum(violations**2)

        if self.upper is not None:
            violations = np.maximum(0, prediction - self.upper)
            loss += np.sum(violations**2)

        return float(self.weight * loss)


class ConservationConstraint(SoftConstraint):
    """Conservation law constraint.

    Enforces that some quantity is conserved.

    Example:
        ```python
        from ununseptium.ai.sciml.constraints import ConservationConstraint

        # Mass conservation
        constraint = ConservationConstraint(
            name="mass",
            conserved_quantity=lambda pred, _: np.sum(pred),
            target_value=1.0
        )
        ```
    """

    def __init__(
        self,
        name: str,
        conserved_quantity: Callable[[np.ndarray, np.ndarray], float],
        target_value: float,
        weight: float = 10.0,
    ) -> None:
        """Initialize conservation constraint.

        Args:
            name: Constraint name.
            conserved_quantity: Function computing conserved quantity.
            target_value: Target value for conservation.
            weight: Loss weight.
        """
        def constraint_fn(pred: np.ndarray, inputs: np.ndarray) -> float:
            return conserved_quantity(pred, inputs) - target_value

        super().__init__(
            name=f"{name}_conservation",
            constraint_fn=constraint_fn,
            weight=weight,
        )


class ConstraintSet:
    """Collection of constraints.

    Example:
        ```python
        from ununseptium.ai.sciml.constraints import ConstraintSet, BoundConstraint

        constraints = ConstraintSet()
        constraints.add(BoundConstraint(lower=0, upper=1))

        total_loss = constraints.total_loss(prediction, inputs)
        report = constraints.evaluate_all(prediction, inputs)
        ```
    """

    def __init__(self) -> None:
        """Initialize constraint set."""
        self._constraints: list[PhysicsConstraint] = []

    def add(self, constraint: PhysicsConstraint) -> None:
        """Add a constraint.

        Args:
            constraint: Constraint to add.
        """
        self._constraints.append(constraint)

    def total_loss(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> float:
        """Compute total constraint loss.

        Args:
            prediction: Model predictions.
            inputs: Input data.

        Returns:
            Sum of all constraint losses.
        """
        return sum(c.loss(prediction, inputs) for c in self._constraints)

    def evaluate_all(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> list[ConstraintResult]:
        """Evaluate all constraints.

        Args:
            prediction: Model predictions.
            inputs: Input data.

        Returns:
            List of ConstraintResults.
        """
        return [c.evaluate(prediction, inputs) for c in self._constraints]

    def all_satisfied(
        self,
        prediction: np.ndarray,
        inputs: np.ndarray,
    ) -> bool:
        """Check if all constraints are satisfied.

        Args:
            prediction: Model predictions.
            inputs: Input data.

        Returns:
            True if all satisfied.
        """
        return all(r.satisfied for r in self.evaluate_all(prediction, inputs))

    def __len__(self) -> int:
        """Number of constraints."""
        return len(self._constraints)
