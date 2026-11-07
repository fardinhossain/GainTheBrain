# 🛡️ LeakLogic AI: Intelligent PII & Secret Discovery in Design-to-Dev Handover Assets

## Category / Domain
Cybersecurity / Developer Tools

## Date
2026-11-07

## Short Description
LeakLogic AI is an automated security auditor designed to scan design files, documentation, and handover assets (like Figma exports, PDFs, and Markdown docs) for Personally Identifiable Information (PII) and hardcoded secrets before they reach the development phase.

## Problem Statement
During the design-to-development handover, designers often use "realistic" data to populate UI mockups. This frequently leads to the accidental inclusion of real user data, internal employee PII, or even active API keys and staging credentials within design tools like Figma, Sketch, or Adobe XD. When these assets are exported as PDFs, shared via public links, or attached to Jira tickets, they create a significant security leak that often goes unnoticed by traditional code-scanning tools (SAST/DAST).

## Proposed Solution
LeakLogic AI acts as a "pre-commit" gate for design assets. It uses Multi-Modal AI (OCR + NLP) to analyze images, PDFs, and design-tool exports. It identifies sensitive patterns—such as credit card numbers, social security numbers, and private keys—embedded in UI mocks. It provides a dashboard for security teams and a CLI/Plugin for designers and developers to scrub or redact sensitive information before the assets are finalized in documentation or code repositories.

## Target Users
- **Security Engineers:** To prevent data leaks in non-code assets.
- **Product Designers:** To ensure mockups are compliant with privacy standards (GDPR/HIPAA).
- **DevOps/Frontend Engineers:** To audit assets before importing them into frontend projects.

## Core Features
- **Multi-Format Scanner:** Supports PDF, PNG, JPG, and Markdown files.
- **Figma API Integration:** Directly scan Figma frames and components via the Figma API.
- **PII Detection:** Identifies names, addresses, emails, phone numbers, and SSNs within UI text.
- **Secret Detection:** Scans for high-entropy strings and known patterns (AWS keys, Stripe keys, JWTs) often used in "example" documentation.
- **Redaction Preview:** Generates a version of the asset with sensitive data blurred or replaced with synthetic data.
- **Jira/Slack Integration:** Alerts teams when a shared link or attachment contains sensitive data.

## Advanced Features
- **Contextual Risk Scoring:** Uses NLP to determine if a string is likely a real secret or just a dummy placeholder (e.g., "sk_live_..." vs "example_key").
- **Custom Regex Engine:** Allows organizations to define their own sensitive patterns (e.g., internal project codenames).
- **CI/CD Integration:** A GitHub Action that fails builds if assets in the `assets/` or `docs/` folders contain unencrypted secrets.
- **Privacy Compliance Reporting:** Generates reports showing the reduction of PII exposure over time.

## AI/ML Integration
- **Tesseract/EasyOCR:** For extracting text from image-based mockups and PDF exports.
- **Named Entity Recognition (NER):** Using models like SpaCy or Transformers to identify PII in a contextual manner (distinguishing between a person's name and a brand name).
- **Pattern Classification:** An LLM or Random Forest classifier to distinguish between "dummy data" and "potential real data leaks" based on the surrounding UI context (e.g., if the text is inside a field labeled "API Key").

## Suggested Tech Stack
- **Backend:** Python (FastAPI) for high-performance OCR and NLP processing.
- **OCR Engine:** EasyOCR or Tesseract.
- **NLP:** SpaCy for NER and HuggingFace Transformers for context analysis.
- **Frontend:** React with Tailwind CSS for the audit dashboard.
- **Task Queue:** Celery with Redis for handling large file batch processing.
- **Storage:** AWS S3 for temporary asset analysis and storage.

## Database Design
- **Users/Orgs:** Standard auth and multi-tenancy.
- **ScanJobs:** Track file metadata, timestamp, status, and overall risk score.
- **Findings:** Store individual PII/Secret hits (location in file, type, confidence score, and redaction status).
- **Integrations:** Store API tokens for Figma, Jira, and Slack.

## API Route Ideas
- `POST /api/v1/scan/upload`: Upload a file for immediate scanning.
- `POST /api/v1/scan/figma`: Trigger a scan for a specific Figma file URL.
- `GET /api/v1/findings/{job_id}`: Retrieve detailed results of a scan.
- `PATCH /api/v1/findings/{finding_id}/ignore`: Mark a finding as a false positive.
- `POST /api/v1/redact`: Return a redacted version of a previously scanned image.

## UI Pages
- **Dashboard:** Overview of recent scans, top leaking assets, and security trends.
- **Scan Detail View:** Interactive image/PDF viewer highlighting detected PII with options to redact.
- **Integrations Page:** Configuration for Figma, Slack, and CI/CD webhooks.
- **Policy Editor:** Interface to toggle specific PII types (e.g., "Only alert on Credit Cards and SSNs").

## MVP Plan
1.  Build the core Python engine using EasyOCR and Regex for basic secret/PII detection.
2.  Create a simple CLI tool that accepts a file path and prints findings to the console.
3.  Develop the FastAPI wrapper and a basic React frontend to display highlighted findings in an uploaded image.
4.  Implement the Figma API integration to pull text from frames.

## Future Scope
- **Browser Extension:** Alert designers in real-time as they edit files in Figma/Canva web apps.
- **Video Scanning:** Scan product demo videos or screen recordings for accidental PII exposure.
- **Auto-Synthetic Replacement:** Instead of just blurring, use AI to replace real PII with realistic synthetic data that maintains the UI's aesthetic.

## Difficulty Level
Intermediate

## Portfolio Value
- Demonstrates expertise in **Cybersecurity** and **Data Privacy**.
- Showcases ability to handle **Multi-Modal AI** (OCR + NLP).
- Highlights understanding of the **Developer/Designer Workflow** and DevSecOps.

## Possible Monetization
- **SaaS Subscription:** Tiered pricing based on the number of scans or users.
- **Enterprise License:** Self-hosted version for companies with strict data residency requirements.
- **Marketplace App:** Premium plugin for Figma or Jira.

## Learning Outcomes
- Mastering **OCR (Optical Character Recognition)** and image processing.
- Implementing **Named Entity Recognition (NER)** for privacy-focused use cases.
- Understanding **API-first security tools** and third-party integrations (Figma/Jira).
- Learning how to build **redaction logic** for images and documents.
