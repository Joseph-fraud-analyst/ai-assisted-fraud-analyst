# AI-Assisted Fraud Analysis Agent - Demonstration Project

## Purpose
A small, local portfolio prototype showing how an AI-assisted workflow could structure a synthetic fraud investigation while keeping evidence, uncertainty, and human review explicit.

**This is a demonstration only.** It does not connect to real banking systems, make live fraud decisions, contact customers, or autonomously block transactions. The included "analysis engine" is deterministic and rule-based so that the project can run without paid AI services. A future model adapter could be added behind the same interface, but any model-generated output would still need validation and human review.

## Features
- Loads synthetic transaction/case data from CSV.
- Separates observed indicators from confirmed facts.
- Generates a structured case summary and proportionate next-step suggestions.
- Flags missing evidence and conflicting indicators.
- Uses a fixed schema and validation checks.
- Requires human review before any consequential action.
- Writes a JSON case report to `output/`.

## Run
Requires Python 3.10+; no third-party dependencies.

```bash
python src/run_agent.py
python -m unittest discover -s tests -v
```

## Example workflow
1. Read a synthetic case.
2. Validate required fields.
3. Summarise only the supplied evidence.
4. Apply transparent indicators (e.g., new device plus unusual amount) as signals, not proof.
5. Record uncertainty and missing evidence.
6. Suggest review steps, not automated customer-impacting action.
7. Mark the report `HUMAN_REVIEW_REQUIRED`.

## Data and privacy
All records are fictional and generated for this portfolio project. Do not use real customer data.
