
# Hardened Webserver Penetration Testing Framework (DevSecOps Integration)

This project integrates automated webserver security testing using **OWASP ZAP** into a CI/CD pipeline (GitHub Actions).

### Features
- Automated ZAP vulnerability scans.
- Security scoring from ZAP reports.
- CI/CD integration via GitHub Actions.

### Usage (Local)
1. Build the Docker image:
   ```bash
   docker build -t myapp:test .
   docker run -d --name myapp -p 8080:80 myapp:test
>>>>>>> Initial commit: setup webserver project and ZAP configuration
