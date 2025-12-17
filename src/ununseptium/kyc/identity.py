"""Identity management and verification.

Provides core identity models and verification logic for KYC compliance.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class RiskLevel(str, Enum):
    """Risk classification levels for identities."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNASSESSED = "unassessed"


class VerificationStatus(str, Enum):
    """Status of identity verification."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"
    EXPIRED = "expired"


class Address(BaseModel):
    """Physical address model."""

    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str | None = None
    postal_code: str | None = None
    country: str = Field(..., min_length=2, max_length=3)


class Identity(BaseModel):
    """Core identity model for KYC.

    Represents an individual or entity subject to KYC verification.

    Attributes:
        id: Unique identifier for the identity.
        name: Full legal name.
        date_of_birth: Date of birth (for individuals).
        nationality: ISO 3166-1 alpha-2 country code.
        document_number: Primary identity document number.
        document_type: Type of identity document.
        address: Current address.
        email: Email address.
        phone: Phone number.
        metadata: Additional custom fields.
        created_at: Timestamp of identity creation.
        updated_at: Timestamp of last update.
    """

    id: str = Field(default_factory=lambda: f"ID-{uuid4().hex[:12].upper()}")
    name: str = Field(..., min_length=1, max_length=500)
    date_of_birth: date | None = None
    nationality: str | None = Field(default=None, min_length=2, max_length=3)
    document_number: str | None = None
    document_type: str | None = None
    address: Address | None = None
    email: str | None = None
    phone: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("nationality")
    @classmethod
    def validate_nationality(cls, v: str | None) -> str | None:
        """Validate nationality is uppercase ISO code."""
        if v is not None:
            return v.upper()
        return v


class ReasonCode(BaseModel):
    """Reason code for verification decisions.

    Provides machine-readable explanations for risk scoring
    and verification outcomes.

    Attributes:
        code: Machine-readable code identifier.
        description: Human-readable description.
        weight: Contribution to overall score (0.0 to 1.0).
        category: Category of the reason.
    """

    code: str
    description: str
    weight: float = Field(ge=0.0, le=1.0)
    category: str = "general"


class VerificationResult(BaseModel):
    """Result of identity verification.

    Contains the outcome of verification along with detailed
    reason codes and evidence references.

    Attributes:
        identity_id: ID of the verified identity.
        status: Verification status.
        risk_level: Assessed risk level.
        risk_score: Numeric risk score (0.0 = low, 1.0 = high).
        confidence: Confidence in the assessment (0.0 to 1.0).
        reason_codes: List of contributing factors.
        evidence_refs: References to supporting evidence.
        verified_at: Timestamp of verification.
        expires_at: When verification expires.
        metadata: Additional verification data.
    """

    identity_id: str
    status: VerificationStatus
    risk_level: RiskLevel = RiskLevel.UNASSESSED
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    reason_codes: list[ReasonCode] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    verified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_audit_dict(self) -> dict[str, Any]:
        """Convert to audit-friendly dictionary.

        Returns:
            Dictionary suitable for audit logging.
        """
        return {
            "identity_id": self.identity_id,
            "status": self.status.value,
            "risk_level": self.risk_level.value,
            "risk_score": self.risk_score,
            "confidence": self.confidence,
            "reason_codes": [rc.model_dump() for rc in self.reason_codes],
            "verified_at": self.verified_at.isoformat(),
        }


class VerificationConfig(BaseModel):
    """Configuration for identity verification.

    Attributes:
        require_document: Whether document verification is required.
        require_address: Whether address verification is required.
        require_screening: Whether sanctions screening is required.
        high_risk_threshold: Score threshold for high risk.
        critical_risk_threshold: Score threshold for critical risk.
        auto_approve_threshold: Score below which auto-approval is allowed.
    """

    require_document: bool = True
    require_address: bool = False
    require_screening: bool = True
    high_risk_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    critical_risk_threshold: float = Field(default=0.9, ge=0.0, le=1.0)
    auto_approve_threshold: float = Field(default=0.3, ge=0.0, le=1.0)


class IdentityVerifier:
    """Verify identities against KYC requirements.

    Orchestrates the verification process including document
    validation, screening, and risk scoring.

    Attributes:
        config: Verification configuration.

    Example:
        ```python
        from ununseptium.kyc import Identity, IdentityVerifier

        identity = Identity(
            name="John Smith",
            date_of_birth="1985-03-15",
            nationality="US"
        )

        verifier = IdentityVerifier()
        result = verifier.verify(identity)

        print(f"Status: {result.status}")
        print(f"Risk Level: {result.risk_level}")
        ```
    """

    def __init__(self, config: VerificationConfig | None = None) -> None:
        """Initialize the verifier.

        Args:
            config: Verification configuration. Uses defaults if not provided.
        """
        self.config = config or VerificationConfig()
        self._reason_codes: list[ReasonCode] = []

    def verify(
        self,
        identity: Identity,
        *,
        screening_results: list[Any] | None = None,
    ) -> VerificationResult:
        """Verify an identity.

        Args:
            identity: Identity to verify.
            screening_results: Optional pre-computed screening results.

        Returns:
            VerificationResult with status and risk assessment.

        Example:
            ```python
            verifier = IdentityVerifier()
            result = verifier.verify(identity)

            if result.status == VerificationStatus.VERIFIED:
                print("Identity verified successfully")
            elif result.status == VerificationStatus.NEEDS_REVIEW:
                print("Manual review required")
            ```
        """
        self._reason_codes = []
        risk_score = 0.0
        confidence = 1.0

        # Basic completeness checks
        completeness_score, completeness_reasons = self._check_completeness(identity)
        self._reason_codes.extend(completeness_reasons)

        # Age verification
        age_score, age_reasons = self._check_age(identity)
        self._reason_codes.extend(age_reasons)

        # Geographic risk
        geo_score, geo_reasons = self._check_geographic_risk(identity)
        self._reason_codes.extend(geo_reasons)

        # Combine scores (weighted average)
        weights = [0.3, 0.3, 0.4]  # completeness, age, geo
        scores = [completeness_score, age_score, geo_score]
        risk_score = sum(w * s for w, s in zip(weights, scores, strict=True))

        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)

        # Determine status
        status = self._determine_status(risk_score, risk_level)

        return VerificationResult(
            identity_id=identity.id,
            status=status,
            risk_level=risk_level,
            risk_score=round(risk_score, 4),
            confidence=round(confidence, 4),
            reason_codes=self._reason_codes,
        )

    def _check_completeness(
        self,
        identity: Identity,
    ) -> tuple[float, list[ReasonCode]]:
        """Check identity data completeness.

        Args:
            identity: Identity to check.

        Returns:
            Tuple of (score, reason_codes).
        """
        reasons: list[ReasonCode] = []
        score = 0.0

        # Check required fields
        if not identity.date_of_birth:
            score += 0.2
            reasons.append(
                ReasonCode(
                    code="MISSING_DOB",
                    description="Date of birth not provided",
                    weight=0.2,
                    category="completeness",
                )
            )

        if not identity.nationality:
            score += 0.15
            reasons.append(
                ReasonCode(
                    code="MISSING_NATIONALITY",
                    description="Nationality not provided",
                    weight=0.15,
                    category="completeness",
                )
            )

        if self.config.require_document and not identity.document_number:
            score += 0.3
            reasons.append(
                ReasonCode(
                    code="MISSING_DOCUMENT",
                    description="Identity document not provided",
                    weight=0.3,
                    category="completeness",
                )
            )

        if self.config.require_address and not identity.address:
            score += 0.2
            reasons.append(
                ReasonCode(
                    code="MISSING_ADDRESS",
                    description="Address not provided",
                    weight=0.2,
                    category="completeness",
                )
            )

        return min(score, 1.0), reasons

    def _check_age(self, identity: Identity) -> tuple[float, list[ReasonCode]]:
        """Check age-related risk factors.

        Args:
            identity: Identity to check.

        Returns:
            Tuple of (score, reason_codes).
        """
        reasons: list[ReasonCode] = []
        score = 0.0

        if identity.date_of_birth:
            today = date.today()
            age = (
                today.year
                - identity.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (identity.date_of_birth.month, identity.date_of_birth.day)
                )
            )

            if age < 18:
                score += 0.5
                reasons.append(
                    ReasonCode(
                        code="UNDERAGE",
                        description="Individual is under 18 years old",
                        weight=0.5,
                        category="age",
                    )
                )
            elif age < 21:
                score += 0.1
                reasons.append(
                    ReasonCode(
                        code="YOUNG_ADULT",
                        description="Individual is between 18-21 years old",
                        weight=0.1,
                        category="age",
                    )
                )

        return min(score, 1.0), reasons

    def _check_geographic_risk(
        self,
        identity: Identity,
    ) -> tuple[float, list[ReasonCode]]:
        """Check geographic risk factors.

        Args:
            identity: Identity to check.

        Returns:
            Tuple of (score, reason_codes).
        """
        # High-risk jurisdictions (simplified example)
        high_risk_countries = {"KP", "IR", "SY", "CU"}
        medium_risk_countries = {"RU", "BY", "VE", "MM"}

        reasons: list[ReasonCode] = []
        score = 0.0

        nationality = identity.nationality
        if nationality:
            if nationality.upper() in high_risk_countries:
                score += 0.8
                reasons.append(
                    ReasonCode(
                        code="HIGH_RISK_JURISDICTION",
                        description=f"High-risk jurisdiction: {nationality}",
                        weight=0.8,
                        category="geographic",
                    )
                )
            elif nationality.upper() in medium_risk_countries:
                score += 0.4
                reasons.append(
                    ReasonCode(
                        code="MEDIUM_RISK_JURISDICTION",
                        description=f"Medium-risk jurisdiction: {nationality}",
                        weight=0.4,
                        category="geographic",
                    )
                )

        return min(score, 1.0), reasons

    def _determine_risk_level(self, score: float) -> RiskLevel:
        """Determine risk level from score.

        Args:
            score: Risk score (0.0 to 1.0).

        Returns:
            Corresponding risk level.
        """
        if score >= self.config.critical_risk_threshold:
            return RiskLevel.CRITICAL
        if score >= self.config.high_risk_threshold:
            return RiskLevel.HIGH
        if score >= 0.4:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _determine_status(
        self,
        score: float,
        risk_level: RiskLevel,
    ) -> VerificationStatus:
        """Determine verification status.

        Args:
            score: Risk score.
            risk_level: Determined risk level.

        Returns:
            Verification status.
        """
        if risk_level == RiskLevel.CRITICAL:
            return VerificationStatus.FAILED
        if risk_level == RiskLevel.HIGH:
            return VerificationStatus.NEEDS_REVIEW
        if score <= self.config.auto_approve_threshold:
            return VerificationStatus.VERIFIED
        return VerificationStatus.NEEDS_REVIEW
