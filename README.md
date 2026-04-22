# Financial Document Intelligence

Document classification and extraction for financial documents with interpretability outputs.

## Supported Document Types

| Type | Examples |
|------|---------|
| `earnings_call` | Quarterly earnings transcripts, investor day presentations |
| `risk_filing` | SEC 10-K/10-Q risk factors, annual report disclosures |
| `trade_confirmation` | OTC/exchange trade confirmations, ISDA confirmations |
| `compliance_report` | FINRA/SEC audit reports, remediation summaries |

## Quick Start

```bash
pip install -r requirements.txt
python examples/run_pipeline.py   # processes 3 sample documents
pytest tests/
```

## Pipeline

```
Document Text
      │
      ▼
  Classifier ──→ doc_type + confidence + per-type scores
      │
      ▼
  Extractor ──→ dates, amounts, companies, CUSIP/ISIN, risk statements
      │
      ▼
  Interpreter ──→ plain-English explanation + key findings + risk signals
      │
      ▼
  PipelineOutput (all above combined)
```

## Interpretability

Every classification decision produces a plain-English explanation:
- Why it was classified as this document type
- Which keywords drove the decision
- Confidence score with explanation
- Risk signals (breach/default/violation keywords)

No black box — every output is auditable.

## Sample Output

```
Classified as: earnings_call (confidence: 85%)
Explanation: This document appears to be an earnings call transcript...
             Classification confidence: 85%. The earnings_call pattern
             matched 40% of its indicator keywords.
Key findings:
  - Financial amounts found: $4.2 billion, $1.87, $16.5 billion
  - Dates referenced: Q3 2024, October 15, 2024
```
