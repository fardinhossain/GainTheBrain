# ⚖️ LicenseLogic AI: Intelligent SaaS Contract Compliance & Spend Auditor

## Category / Domain
Finsphere-AI (FinTech / Spend Management / Compliance)

## Date
2026-11-22

## Short Description
LicenseLogic AI is a sophisticated platform that bridges the gap between legal software contracts and real-world system usage. By using LLMs to parse complex Master Service Agreements (MSAs) and Statements of Work (SOWs), it automatically audits SaaS usage data to identify overspending on unused seats and legal risks from contract breaches.

## Problem Statement
Enterprises spend millions on SaaS subscriptions, yet 30% of that spend is estimated to be wasted on unused licenses. More dangerously, legal teams often lack visibility into whether technical implementations violate contract terms (e.g., "No redistribution of data," "Maximum 50 concurrent API callers," or "Internal use only"). Manual auditing of hundreds of contracts against technical logs is impossible to scale, leading to financial waste and massive liability during audits.

## Proposed Solution
LicenseLogic AI ingests PDF/DocuSign contracts and uses NLP to extract structured obligations (seat counts, renewal dates, usage limits, and restrictive clauses). It then integrates with identity providers (Okta/Azure AD) and SaaS APIs (Salesforce, Datadog, etc.) to compare actual usage against contractual rights. The system provides a real-time dashboard showing "Compliance Drift" and "Optimization Opportunities."

## Target Users
- **CFOs & Finance Teams:** To reduce software waste.
- **Procurement Managers:** To gain leverage during renewals based on actual usage data.
- **Legal & Compliance Officers:** To ensure the company isn't violating software terms of service.
- **IT Administrators:** To automate seat reclamation.

## Core Features
- **AI Contract Parser:** Upload PDF contracts to extract metadata: start/end dates, auto-renewal clauses, price-per-seat, and usage quotas.
- **Usage Integration Hub:** Connectors for Okta, Google Workspace, and major SaaS platforms to track active vs. inactive users.
- **Optimization Engine:** Identifies "Zombie Seats" (assigned but not used for 30+ days) and suggests downgrades to cheaper tiers.
- **Renewal Calendar:** Automated alerts 90/60/30 days before "Notice of Non-Renewal" deadlines extracted from contracts.
- **Compliance Auditor:** Flagging technical patterns that might violate "Fair Use" or "Prohibited Use" clauses in the contract text.

## Advanced Features
- **Shadow IT Discovery:** Cross-references expense reports (via Expensify/Ramp integration) with known contracts to find unsanctioned SaaS spend.
- **Negotiation Intelligence:** Benchmarks contract prices against anonymized industry standards to suggest if the user is overpaying.
- **Automated Seat Reclamation:** Integration with Okta to automatically unassign licenses from inactive users after a manager's approval.

## AI/ML Integration
- **NER (Named Entity Recognition):** Custom models to identify specific legal entities, monetary values, and temporal expressions in messy legal PDFs.
- **Semantic Clause Classification:** Using LLMs (GPT-4o or Claude 3.5) to interpret the *intent* of legal clauses and map them to technical metrics (e.g., mapping "unlimited read-only users" to specific role IDs in a system).
- **Anomaly Detection:** Detecting spikes in usage that might trigger "overage fees" before they appear on an invoice.

## Suggested Tech Stack
- **Backend:** Python (FastAPI) for heavy NLP processing and document handling.
- **OCR Engine:** AWS Textract or Azure AI Document Intelligence for high-fidelity PDF-to-text conversion.
- **Frontend:** Next.js with Tailwind CSS and Recharts for spend visualization.
- **Database:** PostgreSQL with pgvector for storing and querying contract embeddings.
- **Workflow:** Temporal.io or Celery for long-running API sync jobs.

## Database Design
- **Organizations Table:** Basic tenant info.
- **Contracts Table:** Stores binary links, parsed JSON terms, and status (Active, Expired, Pending).
- **Obligations Table:** Atomic units of contract terms (e.g., "Max Seats: 500").
- **Usage_Snapshots Table:** Daily/Weekly aggregations of user activity from integrated SaaS tools.
- **Alerts Table:** Compliance violations and optimization suggestions.

## API Route Ideas
- `POST /api/contracts/upload`: Upload contract PDF and initiate AI parsing.
- `GET /api/contracts/:id/audit`: Compare contract terms against current usage metrics.
- `POST /api/integrations/connect`: OAuth flow for Okta/Salesforce/Slack.
- `GET /api/reports/savings`: Summary of potential ROI from license reclamation.

## UI Pages
- **Compliance Dashboard:** High-level view of risk scores and total waste.
- **Contract Repository:** Searchable list of all legal documents with AI-generated summaries.
- **Integration Center:** Status of API connections to external software.
- **Savings Workflow:** Step-by-step UI to approve license removals.

## MVP Plan
1. Build a basic PDF uploader that uses an LLM to extract Start Date, End Date, and Seat Count.
2. Implement a single integration (e.g., Google Workspace) to pull user "last login" dates.
3. Create a dashboard comparing "Contracted Seats" vs. "Active Users."
4. Implement the renewal alert notification system.

## Future Scope
- **Direct Procurement Integration:** Automatically trigger "Intent to Cancel" emails via API.
- **Multi-Currency Support:** For global enterprises managing contracts in different regions.
- **Legal Redlining Assistant:** Suggest changes to new contracts based on previous usage patterns (e.g., "Don't agree to 500 seats; we never used more than 200 last year").

## Difficulty Level
Advanced (Requires handling unstructured legal data, robust API integrations, and high-accuracy data mapping).

## Portfolio Value
- Demonstrates mastery of Document AI and LLM orchestration.
- Shows ability to build complex B2B FinTech solutions that solve high-dollar problems.
- Highlights experience with third-party API ecosystems (OAuth, Rate Limiting, Data Sync).

## Possible Monetization
- **SaaS Subscription:** Monthly fee based on the number of contracts managed.
- **Gain-Share Model:** Taking a percentage (e.g., 10%) of the total audited savings identified.
- **Enterprise Licensing:** On-premise deployment for high-security legal departments.

## Learning Outcomes
- Deep understanding of NLP/OCR for specialized domains (Legal).
- Proficiency in building multi-tenant integration systems.
- Expertise in translating qualitative legal text into quantitative technical constraints.
