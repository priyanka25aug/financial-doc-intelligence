#!/usr/bin/env python3
"""Working demo — processes 3 sample financial documents. No API keys required."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.pipeline import FinancialDocPipeline

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_documents")
pipeline = FinancialDocPipeline()

docs = {
    "earnings_call.txt": "Earnings Call",
    "risk_filing.txt": "Risk Filing",
    "trade_confirmation.txt": "Trade Confirmation",
}

print("=" * 70)
print("Financial Document Intelligence Pipeline — Demo")
print("=" * 70)

for filename, expected_label in docs.items():
    path = os.path.join(SAMPLE_DIR, filename)
    with open(path) as f:
        text = f.read()

    result = pipeline.process(text)
    print(f"\n--- {filename} ---")
    print(f"  Classified as : {result.classification.doc_type} (confidence: {result.classification.confidence:.0%})")
    print(f"  Explanation   : {result.interpretation.explanation[:120]}...")

    if result.extraction.entities:
        for entity_type, values in result.extraction.entities.items():
            print(f"  {entity_type:20s}: {values[:3]}")

    if result.interpretation.key_findings:
        print(f"  Key findings  :")
        for finding in result.interpretation.key_findings:
            print(f"    - {finding}")

    if result.interpretation.risk_signals:
        print(f"  ⚠ Risk signals:")
        for signal in result.interpretation.risk_signals:
            print(f"    - {signal}")

print("\n" + "=" * 70)
print("All documents processed successfully.")
