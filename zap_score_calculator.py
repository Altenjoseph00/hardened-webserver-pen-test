
import json
import sys

def calculate_score(zap_report_path):
    try:
        with open(zap_report_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Report file not found.")
        sys.exit(1)

    alerts = data.get("site", [])[0].get("alerts", []) if "site" in data else []
    total = len(alerts)
    risk_levels = {"High": 5, "Medium": 3, "Low": 1}
    score = sum(risk_levels.get(a.get("riskdesc", "").split(" ")[0], 0) for a in alerts)
    avg_score = score / total if total else 0

    print(f"Total Alerts: {total}")
    print(f"Average Risk Score: {avg_score:.2f}")

    if avg_score >= 4:
        print("⚠️  High Risk - Immediate attention required!")
    elif avg_score >= 2:
        print("🟡  Moderate Risk - Needs improvement.")
    else:
        print("✅  Low Risk - Webserver is hardened well.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 zap_score_calculator.py <zap_report.json>")
        sys.exit(1)
    calculate_score(sys.argv[1])
>>>>>>> Initial commit: setup webserver project and ZAP configuration
