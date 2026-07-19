# 🛡️ API-Guard AI: Automated Shadow API Discovery & Security Auditor

## Category / Domain
Cybersecurity / Web Security

## Date
2026-07-19

## Short Description
API-Guard AI is a sophisticated security tool designed to passively monitor network traffic to discover "shadow APIs" (undocumented or forgotten endpoints) and use machine learning to detect logic-based vulnerabilities like BOLA (Broken Object Level Authorization) and sensitive data exposure.

## Problem Statement
Modern microservices architectures lead to "API sprawl." Developers often deploy new endpoints for testing or legacy support that are never documented or officially retired. These "shadow APIs" are invisible to security teams but highly visible to attackers. Traditional scanners often miss logic flaws where a user can access another user's data by simply changing an ID in a URL (BOLA/IDOR), as these don't follow standard signature-based attack patterns.

## Proposed Solution
API-Guard AI acts as a transparent proxy or eBPF-based listener that captures API traffic in a staging or production environment. It reconstructs the API's schema (OpenAPI/Swagger) in real-time. It then applies AI models to identify patterns of PII (Personally Identifiable Information) leakage and uses an LLM-based agent to analyze request sequences to predict where authorization checks might be missing, flagging them for human review or automated penetration testing.

## Target Users
- **Security Engineers:** Who need to maintain an accurate inventory of the attack surface.
- **DevOps/SREs:** Who want to ensure documentation matches reality.
- **Penetration Testers:** Looking for a tool to automate the discovery phase of an engagement.

## Core Features
- **Passive Discovery:** Monitor HTTP/HTTPS traffic to map all active endpoints, methods, and parameters.
- **Schema Reconstruction:** Automatically generate OpenAPI 3.0 specifications from observed traffic.
- **Shadow API Alerts:** Compare discovered endpoints against a "Golden Specification" and alert on discrepancies.
- **PII Detection:** Scan request/response bodies for sensitive data (credit cards, SSNs, API keys) using regex and NLP.
- **Traffic Dashboard:** Visualize the API map, showing data flow and dependency between services.

## Advanced Features
- **BOLA Prediction:** Analyze sequential requests to identify parameters that likely represent user-owned resources and flag potential IDOR vulnerabilities.
- **eBPF Integration:** Implement high-performance, kernel-level packet capture for Linux environments without requiring a proxy.
- **Automated Fuzzing:** Generate targeted test cases for discovered shadow endpoints using the reconstructed schema.
- **CI/CD Integration:** Fail builds if a PR introduces an undocumented API endpoint.

## AI/ML Integration
- **NLP for Classification:** Use Transformer-based models to classify the "intent" of an endpoint based on its path and payload, helping to identify high-risk areas (e.g., `/v1/internal/debug`).
- **Anomaly Detection:** Train an Isolation Forest or Autoencoder on "normal" API usage patterns to detect anomalous spikes or unusual access sequences that suggest a data breach in progress.
- **LLM Security Analyst:** Use an LLM to explain *why* a specific sequence of API calls might be a security risk, providing remediation advice to developers.

## Suggested Tech Stack
- **Language:** Go (for the traffic capture engine) and Python (for the AI/ML analysis).
- **Monitoring:** eBPF (via Cilium/ebpf-go) or Envoy Proxy.
- **Message Broker:** Apache Kafka or RabbitMQ to handle high-volume traffic logs.
- **Frontend:** React with D3.js or React Flow for API topology visualization.
- **LLM:** OpenAI GPT-4o or a local Llama 3 instance for vulnerability analysis.

## Database Design
- **PostgreSQL:** Store endpoint metadata, user accounts, and security alerts.
- **ClickHouse:** Store high-volume traffic logs and request/response telemetry for historical analysis.
- **Redis:** Real-time state management and rate-limiting for the capture engine.

## API Route Ideas
- `GET /api/v1/inventory`: List all discovered endpoints and their documentation status.
- `GET /api/v1/alerts`: Retrieve active security findings (PII leaks, shadow APIs).
- `POST /api/v1/specs/upload`: Upload the "official" OpenAPI spec for comparison.
- `GET /api/v1/topology`: Get a JSON representation of service-to-service dependencies.

## UI Pages
- **Security Overview:** High-level dashboard showing "Shadow vs. Documented" count and risk scores.
- **API Map:** An interactive node-graph visualization of the entire API ecosystem.
- **Endpoint Detail:** Deep dive into a specific endpoint's traffic history, detected PII, and potential vulnerabilities.
- **Settings/Integrations:** Configure Slack/Jira alerts and CI/CD webhooks.

## MVP Plan
1. Build a basic Go-based transparent proxy that logs HTTP requests to a database.
2. Implement a script to group requests by path and generate a basic OpenAPI file.
3. Create a React dashboard to display discovered endpoints.
4. Add simple PII detection using regex for credit card numbers and emails.

## Future Scope
- **GraphQL Support:** Introspection and query depth analysis for GraphQL-based APIs.
- **Auto-Remediation:** Integrate with API Gateways (like Kong or AWS API Gateway) to automatically block or rate-limit suspicious endpoints.
- **Multi-Cloud Support:** Native integrations with AWS VPC Mirroring and Azure vTap.

## Difficulty Level
Advanced

## Portfolio Value
This project demonstrates mastery of networking, systems programming (Go/eBPF), specialized security knowledge (OWASP API Top 10), and the practical application of LLMs in a high-stakes domain. It is an extremely high-value project for anyone targeting Security Engineering or DevSecOps roles.

## Possible Monetization
- **B2B SaaS:** Monthly subscription for small-to-medium tech companies.
- **Open-Core:** Free discovery tool with paid "Advanced Security Auditing" and "Enterprise Integration" tiers.
- **Consulting:** Use the tool as a platform for providing API security audits to clients.

## Learning Outcomes
- Deep understanding of HTTP/S protocols and API security patterns.
- Experience with high-performance data processing and time-series databases.
- Practical skills in using AI to solve complex, non-linear logic problems in cybersecurity.
- Proficiency in building developer-centric security tools.
