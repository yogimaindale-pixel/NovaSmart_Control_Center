# Production-Ready Banking Agentic AI Suite

## Executive Summary
This suite implements 3 production-ready, runnable banking Agentic AI scenarios designed to demonstrate enterprise agent architecture, Human-in-the-Loop (HITL) governance gates, regulatory compliance auditing, and stateful interbank ledger reconciliation.

---

## 🏦 The 3 Banking Scenarios

### 1. Payment Fraud Investigation & Dispute Triage Agent (`scenario1_fraud_triage.py`)
- **Business Pain Point**: High volume of card dispute alerts overloading operational fraud teams.
- **Agentic Workflow**:
  - Ingests real-time transaction alerts.
  - Queries transaction history for velocity, amount, location, and device anomalies.
  - Computes risk score ($0.0 \to 1.0$) and categorizes risk into `LOW`, `MEDIUM`, or `HIGH`.
  - **Low Risk**: Automatically issues temporary dispute credit.
  - **High Risk**: Triggers **HITL Governance Gate** requiring a signed `FRAUD_MANAGER` authorization token before executing mutating card block operations.

### 2. Commercial Loan Underwriting & Compliance Auditor Agent (`scenario2_loan_underwriting.py`)
- **Business Pain Point**: Slow manual credit underwriting and regulatory compliance checking (OFAC sanctions, debt coverage).
- **Agentic Workflow**:
  - Analyzes commercial borrower financial metrics (revenue, net income, existing debt).
  - Calculates Debt-Service Coverage Ratio ($DSCR = \frac{\text{Net Operating Income}}{\text{Total Debt Service}}$).
  - Executes real-time OFAC / Sanctions watchlist screening.
  - Evaluates regulatory compliance thresholds ($DSCR \ge 1.25$, Credit Score $\ge 680$).
  - Issues an auditable Underwriting Brief (`APPROVED`, `REFER_TO_COMMITTEE`, or `REJECTED_SANCTIONS_MATCH`).

### 3. Interbank Ledger Reconciliation & Exception Agent (`scenario3_ledger_reconciliation.py`)
- **Business Pain Point**: End-of-day interbank Nostro account settlement mismatches between Core Banking and SWIFT Clearing logs.
- **Agentic Workflow**:
  - Ingests settlement discrepancy alerts.
  - Compares Core Banking Ledger entries against SWIFT Clearing Engine records.
  - Identifies root-cause fee deductions (e.g., intermediary relay bank wire transfer fees).
  - Formulates balancing adjusting entries (`DEBIT_CORRESPONDENT_BANK_FEE_EXPENSE / CREDIT_NOSTRO_ACCOUNT`).
  - Triggers **HITL Governance Gate** requiring signed `TREASURY_MANAGER` token before executing ledger adjustments.

---

## 🚀 Running the Project & Tests

### Quick Start
```bash
# Run all 3 banking scenarios end-to-end
python3 main.py

# Run unit test suite
python3 -m unittest discover tests
```

---

## 🔒 Enterprise Security & Governance Highlights
- **Zero Hardcoded Secrets**: All data structures validate input parameters via Pydantic v2 schemas.
- **Deterministic HITL Intercepts**: Mutating tool actions (card blocking, ledger adjustments) are hard-blocked unless verified by signed role-based authorization tokens outside the LLM context.
- **Auditable Execution Logs**: Every agent step generates structured execution status outputs for SIEM/Splunk ingestion.
