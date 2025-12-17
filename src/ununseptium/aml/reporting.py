"""Regulatory reporting for AML.

Provides report generation for regulatory filings
including Suspicious Activity Reports (SARs).
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ununseptium.aml.cases import Case


class ReportType(str, Enum):
    """Types of regulatory reports."""

    SAR = "sar"
    STR = "str"  # Suspicious Transaction Report
    CTR = "ctr"  # Currency Transaction Report
    WIRE_TRANSFER = "wire_transfer"
    CASH_REPORT = "cash_report"
    CUSTOM = "custom"


class ReportStatus(str, Enum):
    """Status of a report."""

    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    REJECTED = "rejected"


class SubjectType(str, Enum):
    """Type of report subject."""

    INDIVIDUAL = "individual"
    BUSINESS = "business"
    BOTH = "both"


class ReportSubject(BaseModel):
    """Subject of a report.

    Attributes:
        subject_type: Type of subject.
        name: Subject name.
        identifiers: Identity documents.
        address: Address.
        date_of_birth: DOB for individuals.
        occupation: Occupation.
        relationship: Relationship to institution.
    """

    subject_type: SubjectType = SubjectType.INDIVIDUAL
    name: str
    identifiers: dict[str, str] = Field(default_factory=dict)
    address: str | None = None
    date_of_birth: date | None = None
    occupation: str | None = None
    relationship: str | None = None


class SuspiciousActivity(BaseModel):
    """Description of suspicious activity.

    Attributes:
        activity_type: Type of suspicious activity.
        start_date: When activity started.
        end_date: When activity ended.
        amount_involved: Total amount involved.
        currency: Currency.
        description: Detailed description.
        indicators: List of suspicious indicators.
    """

    activity_type: str
    start_date: date
    end_date: date | None = None
    amount_involved: float | None = None
    currency: str = "USD"
    description: str
    indicators: list[str] = Field(default_factory=list)


class SARReport(BaseModel):
    """Suspicious Activity Report.

    Attributes:
        id: Report identifier.
        report_type: Type of report.
        status: Report status.
        filing_institution: Filing institution name.
        filing_institution_id: Institution identifier.
        subjects: Report subjects.
        suspicious_activity: Description of activity.
        transaction_ids: Related transactions.
        case_id: Related case ID.
        narrative: Detailed narrative.
        created_at: Creation timestamp.
        submitted_at: Submission timestamp.
        acknowledgment_number: Regulatory acknowledgment.
        prepared_by: Who prepared the report.
        reviewed_by: Who reviewed the report.
        metadata: Additional data.
    """

    id: str = Field(default_factory=lambda: f"SAR-{uuid4().hex[:8].upper()}")
    report_type: ReportType = ReportType.SAR
    status: ReportStatus = ReportStatus.DRAFT
    filing_institution: str
    filing_institution_id: str | None = None
    subjects: list[ReportSubject] = Field(default_factory=list)
    suspicious_activity: SuspiciousActivity | None = None
    transaction_ids: list[str] = Field(default_factory=list)
    case_id: str | None = None
    narrative: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    submitted_at: datetime | None = None
    acknowledgment_number: str | None = None
    prepared_by: str | None = None
    reviewed_by: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def submit(self) -> None:
        """Mark report as submitted."""
        self.status = ReportStatus.SUBMITTED
        self.submitted_at = datetime.now(UTC)

    def acknowledge(self, acknowledgment_number: str) -> None:
        """Record regulatory acknowledgment.

        Args:
            acknowledgment_number: Acknowledgment reference.
        """
        self.status = ReportStatus.ACKNOWLEDGED
        self.acknowledgment_number = acknowledgment_number

    def to_xml(self) -> str:
        """Export report to XML format.

        Returns:
            XML string representation.

        Note:
            This is a simplified implementation. Production use
            requires format-specific templates (e.g., FinCEN SAR XML).
        """
        # Simplified XML generation
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            "<SuspiciousActivityReport>",
            f"  <ReportId>{self.id}</ReportId>",
            f"  <FilingInstitution>{self.filing_institution}</FilingInstitution>",
            "  <Subjects>",
        ]

        for subject in self.subjects:
            xml_parts.append("    <Subject>")
            xml_parts.append(f"      <Name>{subject.name}</Name>")
            xml_parts.append(f"      <Type>{subject.subject_type.value}</Type>")
            xml_parts.append("    </Subject>")

        xml_parts.append("  </Subjects>")

        if self.suspicious_activity:
            xml_parts.append("  <SuspiciousActivity>")
            xml_parts.append(f"    <Type>{self.suspicious_activity.activity_type}</Type>")
            xml_parts.append(
                f"    <Description>{self.suspicious_activity.description}</Description>"
            )
            xml_parts.append("  </SuspiciousActivity>")

        xml_parts.append(f"  <Narrative>{self.narrative}</Narrative>")
        xml_parts.append("</SuspiciousActivityReport>")

        return "\n".join(xml_parts)


class ReportGenerator:
    """Generate regulatory reports.

    Creates reports from cases and transaction data.

    Example:
        ```python
        from ununseptium.aml import ReportGenerator, Case

        generator = ReportGenerator(
            institution_name="Example Bank",
            institution_id="12345"
        )

        report = generator.create_sar_from_case(case)
        report.submit()
        ```
    """

    def __init__(
        self,
        institution_name: str,
        institution_id: str | None = None,
    ) -> None:
        """Initialize the report generator.

        Args:
            institution_name: Filing institution name.
            institution_id: Institution identifier.
        """
        self.institution_name = institution_name
        self.institution_id = institution_id

    def create_sar(
        self,
        subjects: list[ReportSubject],
        activity: SuspiciousActivity,
        narrative: str,
        *,
        transaction_ids: list[str] | None = None,
        case_id: str | None = None,
        prepared_by: str | None = None,
    ) -> SARReport:
        """Create a Suspicious Activity Report.

        Args:
            subjects: Report subjects.
            activity: Suspicious activity details.
            narrative: Detailed narrative.
            transaction_ids: Related transaction IDs.
            case_id: Related case ID.
            prepared_by: Preparer identifier.

        Returns:
            Created SARReport.
        """
        return SARReport(
            filing_institution=self.institution_name,
            filing_institution_id=self.institution_id,
            subjects=subjects,
            suspicious_activity=activity,
            narrative=narrative,
            transaction_ids=transaction_ids or [],
            case_id=case_id,
            prepared_by=prepared_by,
        )

    def create_sar_from_case(
        self,
        case: Case,
        *,
        subjects: list[ReportSubject] | None = None,
        additional_narrative: str | None = None,
        prepared_by: str | None = None,
    ) -> SARReport:
        """Create a SAR from an investigation case.

        Args:
            case: Source case.
            subjects: Report subjects (extracted from case if not provided).
            additional_narrative: Additional narrative text.
            prepared_by: Preparer identifier.

        Returns:
            Created SARReport.
        """
        # Build narrative from case
        narrative_parts = [
            f"Case ID: {case.id}",
            f"Case Title: {case.title}",
            "",
            "Investigation Summary:",
            case.description or "No description provided.",
            "",
        ]

        if case.findings:
            narrative_parts.append("Findings:")
            narrative_parts.append(case.findings)
            narrative_parts.append("")

        if case.recommendation:
            narrative_parts.append("Recommendation:")
            narrative_parts.append(case.recommendation)
            narrative_parts.append("")

        if additional_narrative:
            narrative_parts.append("Additional Information:")
            narrative_parts.append(additional_narrative)

        narrative = "\n".join(narrative_parts)

        # Create activity description
        activity = SuspiciousActivity(
            activity_type="investigation_finding",
            start_date=case.created_at.date(),
            end_date=case.updated_at.date(),
            description=case.title,
        )

        return SARReport(
            filing_institution=self.institution_name,
            filing_institution_id=self.institution_id,
            subjects=subjects or [],
            suspicious_activity=activity,
            narrative=narrative,
            transaction_ids=case.transaction_ids,
            case_id=case.id,
            prepared_by=prepared_by,
        )

    def generate_batch_report(
        self,
        reports: list[SARReport],
        *,
        output_format: str = "xml",
    ) -> str:
        """Generate a batch submission file.

        Args:
            reports: Reports to include.
            output_format: Output format (xml, json).

        Returns:
            Formatted batch submission.
        """
        if output_format == "xml":
            xml_parts = [
                '<?xml version="1.0" encoding="UTF-8"?>',
                "<BatchSubmission>",
                f"  <BatchId>BATCH-{uuid4().hex[:8].upper()}</BatchId>",
                f"  <ReportCount>{len(reports)}</ReportCount>",
                "  <Reports>",
            ]

            for report in reports:
                xml_parts.append(f"    <ReportRef>{report.id}</ReportRef>")

            xml_parts.append("  </Reports>")
            xml_parts.append("</BatchSubmission>")

            return "\n".join(xml_parts)

        # JSON format
        import json

        batch_data = {
            "batch_id": f"BATCH-{uuid4().hex[:8].upper()}",
            "report_count": len(reports),
            "reports": [r.model_dump(mode="json") for r in reports],
        }
        return json.dumps(batch_data, indent=2, default=str)
