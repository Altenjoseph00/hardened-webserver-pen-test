#!/usr/bin/env python3
import json, sys

def calculate_security_score(report_path):
    with open(report_path, 'r') as f:
        data = json.load(f)

    alerts = []
    sites = data.get("site", [])
    if isinstance(sites, list) and len(sites) > 0:
        for s in sites:
            alerts.extend(s.get("alerts", []))
    else:
        alerts = data.get("alerts", [])

    severity_count = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}
    for a in alerts:
        r = a.get("riskdesc") or a.get("risk") or ""
        sev = r.split()[0] if isinstance(r, str) and r else "Informational"
        severity_count[sev] = severity_count.get(sev, 0) + 1

    weights = {"High":5, "Medium":3, "Low":1, "Informational":0}
    total_weighted = sum(severity_count[s]*weights[s] for s in severity_count)
    total_issues = sum(severity_count.values())
    max_score = total_issues*5 if total_issues > 0 else 1
    security_score = 100 - (total_weighted/max_score*100)

    print("ZAP Vulnerability Summary:")
    for k,v in severity_count.items():
        print(f"  {k}: {v}")
    print(f"Overall Security Score: {security_score:.2f}%")
    return security_score

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "zap_report.json"
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
    score = calculate_security_score(path)
    if score < threshold:
        print(f"Security score {score:.2f}% < threshold {threshold} -> FAIL")
        sys.exit(2)
    else:
        print(f"Security score {score:.2f}% >= threshold {threshold} -> PASS")
        sys.exit(0)
