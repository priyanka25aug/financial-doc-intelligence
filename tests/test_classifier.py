import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.classifier import DocumentClassifier
from src.schemas import ClassificationResult


@pytest.fixture
def classifier():
    return DocumentClassifier()


def test_classifies_earnings_call(classifier):
    text = "Q3 earnings call: revenue beat expectations, EPS guidance raised, fiscal year outlook."
    result = classifier.classify(text)
    assert result.doc_type == "earnings_call"
    assert result.confidence > 0.5


def test_classifies_risk_filing(classifier):
    text = "SEC filing 10-K: risk factor — material adverse uncertainty, litigation, forward-looking."
    result = classifier.classify(text)
    assert result.doc_type == "risk_filing"


def test_classifies_trade_confirmation(classifier):
    text = "Trade date October 15. Settlement T+2. CUSIP 123456789. Counterparty Goldman Sachs. OTC execution."
    result = classifier.classify(text)
    assert result.doc_type == "trade_confirmation"


def test_classifies_compliance_report(classifier):
    text = "Compliance report: FINRA audit found violation. Remediation corrective action required. SEC enforcement."
    result = classifier.classify(text)
    assert result.doc_type == "compliance_report"


def test_result_has_all_scores(classifier):
    result = classifier.classify("some text")
    assert "earnings_call" in result.all_scores
    assert "risk_filing" in result.all_scores
    assert "trade_confirmation" in result.all_scores
    assert "compliance_report" in result.all_scores


def test_confidence_in_range(classifier):
    result = classifier.classify("earnings revenue EPS quarterly beat guidance")
    assert 0.0 <= result.confidence <= 1.0
