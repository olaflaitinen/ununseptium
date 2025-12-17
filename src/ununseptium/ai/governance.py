"""Model governance and lifecycle management.

Provides model registry, validation, and model cards.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class ModelStage(str, Enum):
    """Model lifecycle stages."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class ValidationStatus(str, Enum):
    """Model validation status."""

    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    WAIVED = "waived"


class ModelMetrics(BaseModel):
    """Model performance metrics.

    Attributes:
        accuracy: Classification accuracy.
        precision: Precision score.
        recall: Recall score.
        f1: F1 score.
        auc_roc: Area under ROC curve.
        brier_score: Brier score for calibration.
        ece: Expected Calibration Error.
        custom_metrics: Additional custom metrics.
    """

    accuracy: float | None = None
    precision: float | None = None
    recall: float | None = None
    f1: float | None = None
    auc_roc: float | None = None
    brier_score: float | None = None
    ece: float | None = None
    custom_metrics: dict[str, float] = Field(default_factory=dict)


class ModelCard(BaseModel):
    """Model card for documentation and governance.

    Attributes:
        model_id: Unique model identifier.
        model_name: Human-readable name.
        version: Model version.
        stage: Lifecycle stage.
        description: Model description.
        intended_use: Intended use cases.
        limitations: Known limitations.
        training_data: Training data description.
        metrics: Performance metrics.
        fairness_analysis: Fairness evaluation results.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
        created_by: Creator identifier.
        approved_by: Approver identifier.
        tags: Model tags.
        metadata: Additional metadata.
    """

    model_id: str = Field(default_factory=lambda: f"MODEL-{uuid4().hex[:8].upper()}")
    model_name: str
    version: str = "1.0.0"
    stage: ModelStage = ModelStage.DEVELOPMENT
    description: str = ""
    intended_use: str = ""
    limitations: str = ""
    training_data: str = ""
    metrics: ModelMetrics = Field(default_factory=ModelMetrics)
    fairness_analysis: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str | None = None
    approved_by: str | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def promote(self, new_stage: ModelStage, approved_by: str) -> None:
        """Promote model to new stage.

        Args:
            new_stage: Target stage.
            approved_by: Approver identifier.
        """
        self.stage = new_stage
        self.approved_by = approved_by
        self.updated_at = datetime.now(UTC)


class ValidationResult(BaseModel):
    """Result of model validation.

    Attributes:
        model_id: Model identifier.
        status: Validation status.
        checks: Individual check results.
        message: Summary message.
        validated_at: Validation timestamp.
        validator: Validator identifier.
    """

    model_id: str
    status: ValidationStatus
    checks: dict[str, bool] = Field(default_factory=dict)
    message: str = ""
    validated_at: datetime = Field(default_factory=datetime.utcnow)
    validator: str | None = None


class ModelValidator:
    """Validate models before promotion.

    Example:
        ```python
        from ununseptium.ai import ModelValidator, ModelCard

        validator = ModelValidator()

        card = ModelCard(model_name="risk_model")
        card.metrics.auc_roc = 0.85
        card.metrics.accuracy = 0.78

        result = validator.validate(card)
        if result.status == ValidationStatus.PASSED:
            card.promote(ModelStage.STAGING, "reviewer@example.com")
        ```
    """

    def __init__(self) -> None:
        """Initialize the validator."""
        self._rules: dict[str, dict[str, Any]] = {}
        self._load_default_rules()

    def _load_default_rules(self) -> None:
        """Load default validation rules."""
        self._rules = {
            "min_auc": {
                "check": lambda m: m.auc_roc is not None and m.auc_roc >= 0.7,
                "message": "AUC-ROC must be at least 0.7",
            },
            "min_accuracy": {
                "check": lambda m: m.accuracy is not None and m.accuracy >= 0.7,
                "message": "Accuracy must be at least 0.7",
            },
            "has_metrics": {
                "check": lambda m: any(
                    [
                        m.accuracy is not None,
                        m.auc_roc is not None,
                        m.f1 is not None,
                    ]
                ),
                "message": "Model must have at least one performance metric",
            },
        }

    def add_rule(
        self,
        name: str,
        check: Any,
        message: str,
    ) -> None:
        """Add a validation rule.

        Args:
            name: Rule name.
            check: Function that takes ModelMetrics and returns bool.
            message: Failure message.
        """
        self._rules[name] = {"check": check, "message": message}

    def validate(
        self,
        model_card: ModelCard,
        *,
        validator: str | None = None,
    ) -> ValidationResult:
        """Validate a model.

        Args:
            model_card: Model card to validate.
            validator: Validator identifier.

        Returns:
            ValidationResult.
        """
        checks: dict[str, bool] = {}
        failed_messages: list[str] = []

        for name, rule in self._rules.items():
            try:
                passed = rule["check"](model_card.metrics)
                checks[name] = passed
                if not passed:
                    failed_messages.append(rule["message"])
            except (KeyError, TypeError, AttributeError):
                checks[name] = False
                failed_messages.append(f"Error evaluating {name}")

        all_passed = all(checks.values())
        status = ValidationStatus.PASSED if all_passed else ValidationStatus.FAILED

        message = (
            "All validation checks passed"
            if all_passed
            else f"Failed: {'; '.join(failed_messages)}"
        )

        return ValidationResult(
            model_id=model_card.model_id,
            status=status,
            checks=checks,
            message=message,
            validator=validator,
        )


class ModelRegistry:
    """Registry for model management.

    Example:
        ```python
        from ununseptium.ai import ModelRegistry, ModelCard

        registry = ModelRegistry()

        card = ModelCard(model_name="risk_model_v1")
        registry.register(card)

        # Get model
        model = registry.get("risk_model_v1")

        # List production models
        prod_models = registry.list_models(stage=ModelStage.PRODUCTION)
        ```
    """

    def __init__(self) -> None:
        """Initialize the registry."""
        self._models: dict[str, ModelCard] = {}
        self._by_name: dict[str, list[str]] = {}

    def register(self, model_card: ModelCard) -> str:
        """Register a model.

        Args:
            model_card: Model card to register.

        Returns:
            Model ID.
        """
        self._models[model_card.model_id] = model_card

        if model_card.model_name not in self._by_name:
            self._by_name[model_card.model_name] = []
        self._by_name[model_card.model_name].append(model_card.model_id)

        return model_card.model_id

    def get(self, model_id: str) -> ModelCard | None:
        """Get a model by ID.

        Args:
            model_id: Model identifier.

        Returns:
            ModelCard if found.
        """
        return self._models.get(model_id)

    def get_by_name(
        self,
        name: str,
        *,
        version: str | None = None,
        stage: ModelStage | None = None,
    ) -> ModelCard | None:
        """Get a model by name.

        Args:
            name: Model name.
            version: Specific version.
            stage: Filter by stage.

        Returns:
            Matching ModelCard.
        """
        model_ids = self._by_name.get(name, [])

        for model_id in reversed(model_ids):  # Latest first
            card = self._models.get(model_id)
            if card:
                if version and card.version != version:
                    continue
                if stage and card.stage != stage:
                    continue
                return card

        return None

    def list_models(
        self,
        *,
        stage: ModelStage | None = None,
        tag: str | None = None,
    ) -> list[ModelCard]:
        """List registered models.

        Args:
            stage: Filter by stage.
            tag: Filter by tag.

        Returns:
            List of matching models.
        """
        models = list(self._models.values())

        if stage:
            models = [m for m in models if m.stage == stage]

        if tag:
            models = [m for m in models if tag in m.tags]

        return sorted(models, key=lambda m: m.updated_at, reverse=True)

    def update(self, model_card: ModelCard) -> None:
        """Update a model card.

        Args:
            model_card: Updated model card.
        """
        model_card.updated_at = datetime.now(UTC)
        self._models[model_card.model_id] = model_card

    def delete(self, model_id: str) -> bool:
        """Delete a model.

        Args:
            model_id: Model to delete.

        Returns:
            True if deleted.
        """
        if model_id in self._models:
            card = self._models[model_id]
            del self._models[model_id]

            if card.model_name in self._by_name:
                self._by_name[card.model_name] = [
                    m for m in self._by_name[card.model_name] if m != model_id
                ]

            return True
        return False
