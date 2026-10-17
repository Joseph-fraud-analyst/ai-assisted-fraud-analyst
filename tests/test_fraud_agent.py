import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
from fraud_agent import analyse_case

def valid_case(**overrides):
    case = {
        "case_id": "CASE-TEST",
        "customer_id": "CUST-TEST",
        "transaction_id": "TX-TEST",
        "amount_gbp": "120.00",
        "channel": "ecommerce",
        "device_known": "true",
        "location_consistent": "true",
        "customer_confirmed": "false",
        "chargeback_received": "false",
        "notes": "Synthetic test record"
    }
    case.update(overrides)
    return case

class FraudAgentTests(unittest.TestCase):
    def test_unrecognised_device_is_indicator_not_proof(self):
        result = analyse_case(valid_case(device_known="false"))
        self.assertTrue(any("not recognised" in x for x in result["observed_indicators"]))
        self.assertIn("HUMAN_REVIEW_REQUIRED", result["decision"])
        self.assertFalse(result["automated_action_taken"])

    def test_customer_confirmation_is_recorded_as_fact(self):
        result = analyse_case(valid_case(customer_confirmed="true"))
        self.assertTrue(any("Customer confirmation" in x for x in result["confirmed_facts"]))

    def test_missing_field_returns_incomplete_input(self):
        case = valid_case()
        del case["channel"]
        result = analyse_case(case)
        self.assertEqual(result["status"], "INCOMPLETE_INPUT")
        self.assertIn("HUMAN_REVIEW_REQUIRED", result["decision"])

    def test_high_amount_does_not_establish_fraud(self):
        result = analyse_case(valid_case(amount_gbp="900.00"))
        self.assertTrue(any("does not establish fraud" in x for x in result["observed_indicators"]))

    def test_never_takes_automated_action(self):
        result = analyse_case(valid_case())
        self.assertFalse(result["automated_action_taken"])
        self.assertEqual(result["decision"], "HUMAN_REVIEW_REQUIRED")

if __name__ == "__main__":
    unittest.main()
