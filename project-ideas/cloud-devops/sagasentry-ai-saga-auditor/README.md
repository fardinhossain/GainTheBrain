# 🛡️ SagaSentry AI: Distributed Transaction Consistency & Saga Pattern Auditor

## Category / Domain
Cloud-DevOps / Software Engineering / Observability

## Date
2026-10-27

## Short Description
SagaSentry AI is an intelligent observability tool designed to audit distributed transactions in microservices. It analyzes OpenTelemetry traces and application logs to detect inconsistencies in the "Saga Pattern," identifying instances where transactions failed, rollbacks (compensations) didn't execute correctly, or data remains in a "zombie" state across different services.

## Problem Statement
In microservices architectures, ensuring data consistency across multiple databases is a major challenge. Since traditional 2-Phase Commit (2PC) is rarely used due to scalability issues, developers implement the Saga Pattern (a sequence of local transactions with compensating actions for failures). However, if a compensation step fails or isn't triggered correctly due to a bug or network partition, the system enters an inconsistent state (e.g., a customer is charged, but the inventory is never updated, and the order is marked as failed). Finding these "broken sagas" manually across millions of logs and traces is nearly impossible.

## Proposed Solution
SagaSentry AI acts as a specialized auditor for distributed logic. By ingesting distributed traces (Jaeger/Zipkin) and structured logs, it reconstructs the lifecycle of a business transaction across multiple services. It uses a graph-based analysis to compare the actual flow against the expected Saga state machine. If it detects a missing compensation step or an orphaned transaction that never reached a terminal state (Success or Compensated), it flags the inconsistency and uses AI to explain the root cause and suggest remediation steps.

## Target Users
- **DevOps Engineers**: To monitor the health of distributed business processes.
- **Backend Architects**: To validate the reliability of their Saga implementations.
- **SREs (Site Reliability Engineers)**: To debug complex data inconsistency incidents in production.

## Core Features
- **Trace Ingestion**: Seamlessly integrate with OpenTelemetry collectors to ingest spans and traces.
- **Saga Mapping**: Define Saga flows using a simple DSL or JSON schema (e.g., OrderService -> PaymentService -> ShippingService).
- **Inconsistency Detection**: Automatically flag "incomplete" sagas where a failure occurred but no corresponding compensation span was detected.
- **Visual Saga Graph**: A dashboard showing the health of business transactions as they move through different nodes.
- **Alerting Engine**: Notify teams via Slack/PagerDuty when a high-value transaction enters a persistent inconsistent state.

## Advanced Features
- **Shadow Auditing**: Replay historical traces to find long-tail consistency bugs that occurred months ago.
- **Automated Compensation Suggestions**: AI analyzes the code/logs to suggest the exact SQL or API call needed to manually reconcile the data.
- **Drift Detection**: Identify when the actual implementation of a Saga in code deviates from the architectural design.

## AI/ML Integration
- **Logic Reasoning (LLM)**: An LLM analyzes the sequence of logs and spans to understand the *intent* of the developer. It interprets error messages (e.g., "Insufficient Funds" vs "Timeout") to determine if a compensation *should* have been triggered.
- **Anomaly Detection**: Uses unsupervised learning to detect "stuck" transactions that are taking significantly longer than the P99 latency for that specific saga step.
- **Root Cause Synthesis**: Generates a natural language summary explaining why a specific transaction failed to roll back (e.g., "Service B failed to acknowledge the rollback request due to an unhandled 500 error in the /cancel endpoint").

## Suggested Tech Stack
- **Backend**: Go or Rust (for high-performance trace processing).
- **Orchestration**: OpenTelemetry SDKs.
- **Database**: PostgreSQL (for metadata) and ClickHouse (for high-volume trace/log storage).
- **AI Logic**: OpenAI API (GPT-4o) or LangChain with a local Llama 3 instance for log analysis.
- **Frontend**: Next.js with React Flow (for visualizing the transaction graphs).

## Database Design
- **SagaDefinitions**: ID, Name, Steps (JSON), CompensationSteps (JSON).
- **TransactionInstances**: SagaID, CorrelationID, StartTime, EndTime, CurrentStatus (Pending, Success, Failed, Inconsistent).
- **AuditLogs**: InstanceID, StepName, SpanID, Result, ErrorContext.
- **Inconsistencies**: InstanceID, DetectedAt, RootCauseSummary, Severity.

## API Route Ideas
- `POST /api/v1/definitions`: Register a new Saga state machine.
- `GET /api/v1/sagas/inconsistent`: List all currently broken distributed transactions.
- `GET /api/v1/sagas/:correlationId/graph`: Get the visual path of a specific transaction instance.
- `POST /api/v1/sagas/analyze-failure`: Send a trace ID to get an AI-generated explanation of the failure.

## UI Pages
- **Main Dashboard**: Overview of Saga health (Success rate, Inconsistency rate, Active transactions).
- **Saga Explorer**: Searchable list of all business transactions by Correlation ID or Customer ID.
- **Visual Trace View**: A node-based graph showing the flow of a single saga, highlighting where it broke.
- **Configuration**: Editor for defining Saga flows and mapping them to specific trace attributes.

## MVP Plan
1. Build the trace ingestion pipeline using an OpenTelemetry receiver.
2. Implement a basic state-machine matcher that flags transactions that stop midway without a success or failure signal.
3. Create a CLI tool to report inconsistent Trace IDs from a local Jaeger instance.
4. Add a basic web UI to visualize the sequence of spans for a single transaction.

## Future Scope
- **Auto-Remediation**: Integrate with workflow engines (like Temporal or Camunda) to automatically trigger manual reconciliation tasks.
- **Infrastructure correlation**: Link saga failures to infrastructure events (e.g., "Saga failed because Kubernetes node X restarted during Step 2").
- **Multi-Cloud Auditing**: Track transactions that span across AWS, Azure, and on-premise environments.

## Difficulty Level
Advanced (Requires deep knowledge of distributed systems, observability standards, and complex data modeling).

## Portfolio Value
This project demonstrates a sophisticated understanding of the most difficult problem in cloud computing: distributed state management. It shows proficiency in modern observability (Otel), high-scale data processing (ClickHouse), and the practical application of LLMs in debugging.

## Possible Monetization
- **SaaS Platform**: Monthly subscription for cloud-native companies using microservices.
- **Enterprise Self-Hosted**: Licensed version for financial institutions where data consistency is a regulatory requirement.
- **Consulting**: Audit services for companies migrating from monoliths to microservices.

## Learning Outcomes
- Mastery of OpenTelemetry and distributed tracing.
- Deep understanding of the Saga Pattern and its failure modes.
- Experience with high-performance OLAP databases (ClickHouse).
- Practical application of LLMs for structural logic analysis rather than just text generation.
