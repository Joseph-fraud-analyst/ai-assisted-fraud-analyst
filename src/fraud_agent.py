import csv
import json
from pathlib import Path

REQUIRED_FIELDS = {
    "case_id", "customer_id", "transaction_id", "amount_gbp", "channel",
    "device_known", "location_consistent", "customer_confirmed",
    "chargeback_received", "notes"
}

def as_bool(value):
    return str(value).strip().lower() == "true"

def analyse_case(case):
    missing = sorted(k for k in REQUIRED_FIELDS if k not in case or str(case[k]).strip() == "")
    if missing:
        return {
            "case_id": case.get("case_id", "UNKNOWN"),
            "status": "INCOMPLETE_INPUT",
            "observed_indicators": [],
            "confirmed_facts": [],
            "uncertainties": [f"Missing required field: {field}" for field in missing],
            "recommended_next_steps": ["Obtain missing information and re-run validation."],
            "decision": "HUMAN_REVIEW_REQUIRED",
        }

    indicators = []
    facts = []
    uncertainties = []

    device_known = as_bool(case["device_known"])
    location_consistent = as_bool(case["location_consistent"])
    customer_confirmed = as_bool(case["customer_confirmed"])
    chargeback_received = as_bool(case["chargeback_received"])

    if not device_known:
        indicators.append("Device is not recognised in the supplied record.")
    if not location_consistent:
        indicators.append("Location differs from the customer's usual pattern in the supplied record.")
    if float(case["amount_gbp"]) >= 500:
        indicators.append("Transaction amount is at least GBP 500; amount alone does not establish fraud.")
    if chargeback_received:
        facts.append("A chargeback is recorded as received in the supplied case data.")
    if customer_confirmed:
        facts.append("Customer confirmation is recorded as positive in the supplied case data.")

    if not customer_confirmed and not chargeback_received:
        uncertainties.append("Customer confirmation and chargeback evidence do not establish the transaction outcome.")
    if not device_known or not location_consistent:
        uncertainties.append("One or more risk indicators are present, but indicators are not proof of fraud.")
    if not case.get("notes", "").strip():
        uncertainties.append("No investigation notes were supplied.")

    steps = []
    if not customer_confirmed:
        steps.append("Review the approved customer-contact and authentication process; do not contact automatically.")
    if not device_known or not location_consistent:
        steps.append("Review supporting device, authentication, and transaction history evidence.")
    if chargeback_received:
        steps.append("Check the chargeback record and relevant dispute evidence.")
    if not steps:
        steps.append("Record the evidence reviewed and close only in line with authorised procedures.")

    return {
        "case_id": case["case_id"],
        "transaction_id": case["transaction_id"],
        "amount_gbp": round(float(case["amount_gbp"]), 2),
        "channel": case["channel"],
        "observed_indicators": indicators,
        "confirmed_facts": facts,
        "uncertainties": uncertainties,
        "case_notes_as_supplied": case["notes"],
        "recommended_next_steps": steps,
        "decision": "HUMAN_REVIEW_REQUIRED",
        "automated_action_taken": False,
        "disclaimer": "Synthetic demonstration only; indicators are not a fraud determination."
    }

def load_cases(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def run(input_csv, output_json):
    cases = load_cases(input_csv)
    reports = [analyse_case(case) for case in cases]
    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(output_json).write_text(json.dumps(reports, indent=2), encoding="utf-8")
    return reports
