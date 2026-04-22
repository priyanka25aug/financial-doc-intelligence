import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.extractor import EntityExtractor


@pytest.fixture
def extractor():
    return EntityExtractor()


def test_extracts_amounts(extractor):
    text = "Revenue was $4.2 billion, up from $3.8 billion last year. EPS of $1.87."
    result = extractor.extract(text, "earnings_call")
    assert "amounts" in result.entities
    assert len(result.entities["amounts"]) > 0


def test_extracts_percentages(extractor):
    text = "Revenue grew by 12%. Operating margin improved to 34%."
    result = extractor.extract(text, "earnings_call")
    assert "percentages" in result.entities


def test_extracts_cusip(extractor):
    text = "Trade details: CUSIP 459200101, settlement T+2."
    result = extractor.extract(text, "trade_confirmation")
    assert "cusip" in result.entities
    assert "459200101" in result.entities["cusip"]


def test_extracts_risk_statements(extractor):
    text = "The risk of default by counterparty could result in material losses exceeding $100M."
    result = extractor.extract(text, "risk_filing")
    assert "risk_statements" in result.entities
    assert len(result.entities["risk_statements"]) > 0


def test_records_text_length(extractor):
    text = "Some financial document text here."
    result = extractor.extract(text, "general")
    assert result.raw_text_length == len(text)


def test_no_false_entities_on_empty_text(extractor):
    result = extractor.extract("", "general")
    assert result.entities == {}
