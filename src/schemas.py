from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EarningsCallSchema:
    doc_type: str = "earnings_call"
    company: Optional[str] = None
    quarter: Optional[str] = None
    fiscal_year: Optional[str] = None
    revenue: Optional[str] = None
    eps: Optional[str] = None
    guidance: Optional[str] = None
    key_statements: List[str] = field(default_factory=list)


@dataclass
class RiskFilingSchema:
    doc_type: str = "risk_filing"
    company: Optional[str] = None
    filing_date: Optional[str] = None
    risk_factors: List[str] = field(default_factory=list)
    regulatory_bodies: List[str] = field(default_factory=list)
    material_events: List[str] = field(default_factory=list)


@dataclass
class TradeConfirmationSchema:
    doc_type: str = "trade_confirmation"
    trade_date: Optional[str] = None
    settlement_date: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    notional: Optional[str] = None
    counterparty: Optional[str] = None
    instrument_type: Optional[str] = None


@dataclass
class ComplianceReportSchema:
    doc_type: str = "compliance_report"
    report_date: Optional[str] = None
    regulatory_body: Optional[str] = None
    violations: List[str] = field(default_factory=list)
    remediation_actions: List[str] = field(default_factory=list)
    status: Optional[str] = None


@dataclass
class ClassificationResult:
    doc_type: str
    confidence: float
    reasoning: str
    all_scores: dict


@dataclass
class ExtractionResult:
    doc_type: str
    entities: dict
    raw_text_length: int


@dataclass
class InterpretationResult:
    explanation: str
    key_findings: List[str]
    risk_signals: List[str]
    confidence_explanation: str


@dataclass
class PipelineOutput:
    classification: ClassificationResult
    extraction: ExtractionResult
    interpretation: InterpretationResult
    text_preview: str
