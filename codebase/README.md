# 💻 NovaSmart Control Center Codebase Documentation

Welcome to the **`codebase/`** directory. This directory contains the complete, tested source code for NovaSmart's multi-agent services, governance auditing tools, security benchmark suites, and assistant modules.

---

## 📂 Codebase Directory Structure

```text
codebase/
├── price_match_agent/                  # Price Match Agent Service & Security Verification
│   ├── price_match_service.py           # Core Price Match Logic with Hard Margin Floor Guardrail
│   ├── advanced_scenario_benchmark.py   # 12-Case Benchmark Evaluation Suite
│   ├── gateway_screening_test.py        # Agent Gateway Model Armor Filter Config & Test
│   ├── verify_all_attacks.py            # Prompt Injection Attack Verification Suite
│   └── evaluate_price_match_agent.py    # Policy Rule Verification Script
├── novasmart_governance/               # GCP Infrastructure & IAM Governance Audit Tools
│   ├── check_iam_and_access.py          # Service Account Decoupling & Dataset ACL Auditor
│   ├── check_agents.py                  # Agent Engine / Catalog Inventory Auditor
│   ├── get_agent_details.py             # Reasoning Engine Spec & Deployment Config Extractor
│   ├── audit_customer_access.py         # Cross-Dataset PII Access Validator
│   └── agent_details.json               # Extracted Infrastructure Metadata
├── banking_agents/                     # Banking Agent Workloads (Fraud, Underwriting, Ledger)
│   ├── main.py                          # Banking Suite Entrypoint
│   ├── banking_agents/                  # Scenario Agents (Fraud Triage, Underwriting, Ledger)
│   └── tests/                           # Unit Tests for Banking Agents
```

---

## 🛠️ Detailed Module Guide & Execution Instructions

### **1. Price Match Agent (`codebase/price_match_agent/`)**

#### **A. `price_match_service.py`**
* **Purpose**: Implements the production Price Match evaluation service with a **hard code-level margin floor guardrail** preventing negative profit sales.
* **Key Functions**:
  * `evaluate_price_match(sku, competitor_name, competitor_price, shelf_price, wholesale_cost, competitor_stock, local_stock)`
  * Enforces:
    1. **Retailer Whitelist Check**: Only authorized partners (`AlphaStore`, `BetaBuy`).
    2. **Competitor Inventory Check**: Competitor stock must be $> 0$.
    3. **Local Inventory Check**: Local stock must be $> 0$.
    4. **Hard Margin Floor Check**: Programmatically blocks matches below wholesale acquisition cost ($\text{Competitor Price} < \text{Wholesale Cost}$).
    5. **Automated Approval Threshold**: Approves automatically if discount $\le 10.0\%$; escalates to Store Manager if $> 10.0\%$.
* **How to Run**:
  ```bash
  python3 codebase/price_match_agent/price_match_service.py
  ```

#### **B. `advanced_scenario_benchmark.py`**
* **Purpose**: Executes the 12-case benchmark evaluation suite covering boundary conditions (`10.0%` vs `10.1%`), out-of-stock items, currency formatting variants, volume B2B requests, and prompt injection attacks (`"SYSTEM OVERRIDE"`).
* **How to Run**:
  ```bash
  python3 codebase/price_match_agent/advanced_scenario_benchmark.py
  ```
* **Expected Output**: `12 out of 12 cases passed (100% Pass Rate)`.

#### **C. `verify_all_attacks.py`**
* **Purpose**: Verifies that Agent Gateway Model Armor ingress filters block prompt injection attacks (`HTTP 400 Bad Request`) while allowing valid customer price match queries (`HTTP 200 OK`).
* **How to Run**:
  ```bash
  python3 codebase/price_match_agent/verify_all_attacks.py
  ```

---

### **2. NovaSmart Governance (`codebase/novasmart_governance/`)**

#### **A. `check_iam_and_access.py`**
* **Purpose**: Queries Google Cloud IAM and BigQuery API to verify service account decoupling and dataset Access Control Lists (ACLs).
* **Enforces**:
  * `customer-personalization-sa` $\rightarrow$ Access restricted to `customer_data`
  * `price-match-sa` $\rightarrow$ Access restricted to `novasmart_pricing` and `competitor_data`
  * `markdown-strategy-sa` $\rightarrow$ Access restricted to `novasmart_pricing`
* **How to Run**:
  ```bash
  python3 codebase/novasmart_governance/check_iam_and_access.py
  ```

#### **B. `audit_customer_access.py`**
* **Purpose**: Demonstrates cross-dataset security isolation by attempting to query customer PII using `price-match-sa` and confirming BigQuery returns `403 Access Denied`.
* **How to Run**:
  ```bash
  python3 codebase/novasmart_governance/audit_customer_access.py
  ```

---

### **3. Banking Agents (`codebase/banking_agents/`)**
* **Purpose**: Provides financial workflow automation agents for Fraud Triage (`scenario1`), Loan Underwriting (`scenario2`), and Ledger Reconciliation (`scenario3`).
* **How to Run**:
  ```bash
  python3 codebase/banking_agents/main.py
  ```


