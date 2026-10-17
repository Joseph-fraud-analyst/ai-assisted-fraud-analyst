from pathlib import Path
from fraud_agent import run

ROOT = Path(__file__).resolve().parents[1]
input_csv = ROOT / "data" / "cases.csv"
output_json = ROOT / "output" / "case_reports.json"
reports = run(input_csv, output_json)
print(f"Processed {len(reports)} synthetic cases.")
print(f"Output written to: {output_json}")
for report in reports:
    print(f"{report['case_id']}: {report['decision']} — {len(report.get('observed_indicators', []))} indicator(s)")
