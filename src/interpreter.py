"""
Plain-English interpreter: generates human-readable explanations of every
classification decision. No black box — every output is explainable.
"""
from .schemas import ClassificationResult, ExtractionResult, InterpretationResult

RISK_SIGNALS = {
    "breach": "Breach keyword detected — may indicate limit or regulatory violation.",
    "default": "Default keyword detected — counterparty or credit default risk.",
    "violation": "Violation keyword detected — potential regulatory non-compliance.",
    "material adverse": "Material adverse event keyword — may impact financial statements.",
    "enforcement": "Enforcement keyword detected — regulatory action may be in progress.",
    "limit exceeded": "Limit exceeded — position or exposure threshold may be breached.",
}

DOC_TYPE_EXPLANATIONS = {
    "earnings_call": "This document appears to be an earnings call transcript or earnings-related communication, containing performance metrics and forward guidance.",
    "risk_filing": "This document appears to be a risk disclosure or regulatory filing, containing material risk factors and compliance-related information.",
    "trade_confirmation": "This document appears to be a trade confirmation, recording the details of a completed financial transaction.",
    "compliance_report": "This document appears to be a compliance or audit report, documenting regulatory status and remediation activities.",
}


class DocumentInterpreter:
    def interpret(
        self,
        text: str,
        classification: ClassificationResult,
        extraction: ExtractionResult,
    ) -> InterpretationResult:
        text_lower = text.lower()
        doc_explanation = DOC_TYPE_EXPLANATIONS.get(
            classification.doc_type, "Document type could not be determined with high confidence."
        )

        confidence_explanation = (
            f"Classification confidence: {classification.confidence:.0%}. "
            f"The {classification.doc_type} pattern matched {classification.all_scores.get(classification.doc_type, 0):.0%} "
            f"of its indicator keywords."
        )

        key_findings = []
        if extraction.entities.get("amounts"):
            key_findings.append(f"Financial amounts found: {', '.join(extraction.entities['amounts'][:3])}")
        if extraction.entities.get("dates"):
            key_findings.append(f"Dates referenced: {', '.join(extraction.entities['dates'][:3])}")
        if extraction.entities.get("companies"):
            key_findings.append(f"Companies mentioned: {', '.join(extraction.entities['companies'][:3])}")
        if extraction.entities.get("risk_statements"):
            key_findings.append(f"Risk statements found: {len(extraction.entities['risk_statements'])}")

        risk_signals = [
            explanation
            for keyword, explanation in RISK_SIGNALS.items()
            if keyword in text_lower
        ]

        explanation = f"{doc_explanation} {confidence_explanation}"

        return InterpretationResult(
            explanation=explanation,
            key_findings=key_findings,
            risk_signals=risk_signals,
            confidence_explanation=confidence_explanation,
        )
