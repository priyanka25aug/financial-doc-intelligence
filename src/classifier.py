"""
Document type classifier for financial documents.
Uses keyword scoring — no LLM required.
"""
from .schemas import ClassificationResult

DOC_TYPE_PATTERNS = {
    "earnings_call": {
        "keywords": ["earnings", "revenue", "eps", "guidance", "quarterly", "fiscal", "beat", "outlook", "cfo", "ceo"],
        "weight": 1.0,
    },
    "risk_filing": {
        "keywords": ["risk factor", "material adverse", "forward-looking", "uncertainty", "litigation",
                     "sec filing", "10-k", "10-q", "annual report"],
        "weight": 1.0,
    },
    "trade_confirmation": {
        "keywords": ["trade date", "settlement", "cusip", "isin", "notional", "counterparty",
                     "execution", "t+2", "t+1", "otc"],
        "weight": 1.0,
    },
    "compliance_report": {
        "keywords": ["compliance", "violation", "regulatory", "enforcement", "remediation",
                     "finra", "sec", "audit", "breach", "corrective action"],
        "weight": 1.0,
    },
}


class DocumentClassifier:
    def classify(self, text: str) -> ClassificationResult:
        text_lower = text.lower()
        scores = {}
        for doc_type, config in DOC_TYPE_PATTERNS.items():
            hits = sum(1 for kw in config["keywords"] if kw in text_lower)
            scores[doc_type] = hits / len(config["keywords"])

        best = max(scores, key=scores.get)
        confidence = min(0.5 + scores[best], 0.99)

        return ClassificationResult(
            doc_type=best,
            confidence=confidence,
            reasoning=(
                f"Keyword match: {best} scored {scores[best]:.2f}. "
                f"All scores: { {k: round(v, 2) for k, v in scores.items()} }"
            ),
            all_scores=scores,
        )
