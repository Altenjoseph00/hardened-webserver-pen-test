import json
import sys

def calculate_score(zap_report_path, threshold=2.0):
    try:
        with open(zap_report_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Report file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Invalid JSON file.")
        sys.exit(1)

    # Extract alerts
    sites = data.get("site", [])
    alerts = []
    for site in sites:
        alerts.extend(site.get("alerts", []))

    total_alerts = len(alerts)
    risk_levels = {"High": 5, "Medium": 3, "Low": 1}
    score = sum(risk_levels.get(a.get("riskdesc", "").split(" ")[0], 0) for a in alerts)
    avg_score = score / total_alerts if total_alerts else 0

    print(f"Total Alerts: {total_alerts}")
    print(f"Average Risk Score: {avg_score:.2f}")

    if avg_score >= 4:
        print("⚠️  High Risk - Immediate attention required!")
    elif avg_score >= 2:
        print("🟡  Moderate Risk - Needs improvement.")
    else:
        print("✅  Low Risk - Webserver is hardened well.")

    # Exit with non-zero code if above threshold
    if avg_score >= threshold:
        print(f"❌ CI/CD check failed: Average risk score ({avg_score:.2f}) exceeds threshold ({threshold})")
        sys.exit(1)
    else:
        print(f"✅ CI/CD check passed: Average risk score ({avg_score:.2f}) is below threshold ({threshold})")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 zap_score_calculator.py <zap_report.json> [threshold]")
        sys.exit(1)

    zap_file = sys.argv[1]
    threshold_val = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    calculate_score(zap_file, threshold_val)

