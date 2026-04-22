"""
Entity extractor for financial documents.
Uses regex patterns — no LLM required.
"""
import re
from .schemas import ExtractionResult

PATTERNS = {
    "dates": r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}|\b\d{1,2}/\d{1,2}/\d{2,4}\b|Q[1-4]\s*\d{4}',
    "amounts": r'\$[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|M|B|K))?\b',
    "companies": r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc\.|Corp\.|LLC|Ltd\.|plc|Group)\b',
    "cusip": r'\b[0-9]{6}[0-9A-Z]{2}[0-9]\b',
    "isin": r'\b[A-Z]{2}[0-9]{10}\b',
    "risk_statements": r'(?:risk|exposure|adverse|uncertainty|default|breach|violation)[^.]{10,100}\.',
    "percentages": r'\b\d+(?:\.\d+)?%',
}


class EntityExtractor:
    def extract(self, text: str, doc_type: str) -> ExtractionResult:
        entities = {}
        for entity_type, pattern in PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                entities[entity_type] = list(set(matches))[:5]

        return ExtractionResult(
            doc_type=doc_type,
            entities=entities,
            raw_text_length=len(text),
        )
