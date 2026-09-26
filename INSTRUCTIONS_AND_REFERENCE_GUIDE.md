# 📖 NovaSmart Control Center: User Instructions & Step-by-Step Reference Guide

Welcome to the **NovaSmart Control Center** repository. This project contains the complete AI governance, identity decoupling, content screening, and telemetry configuration for NovaSmart's multi-agent AI estate.

---

## 🚀 Quick Start & How to Use This Repository

### **1. Prerequisites**
* **Google Cloud SDK (`gcloud`)** installed and authenticated.
* **Python 3.10+** environment.
* **Google Cloud Project**:
  * Project ID: `qwiklabs-gcp-01-2aad14f2c696`
  * Region: `us-west1`

### **2. Repository Structure**
```text
NovaSmart_Control_Center/
├── README.md                                 # Project Overview & Governance Architecture
├── INSTRUCTIONS_AND_REFERENCE_GUIDE.md        # Step-by-Step Usage & Reference Guide
├── SESSION_HISTORY_AND_COMMAND_LOGS.md        # Complete Session History & Command Results
├── scorecards/                                # Official Governance & Evaluation Scorecards
│   ├── mission_1_scorecard.md
│   ├── mission_3_governance_scorecard.md
│   ├── mission_4_governance_scorecard.md
│   └── price_match_advanced_evaluation_scorecard.md
└── scripts/                                   # Audit, Test, and Guardrail Scripts
    ├── check_iam_and_access.py
    ├── audit_customer_access.py
    ├── gateway_screening_test.py
    ├── verify_all_attacks.py
    ├── evaluate_price_match_agent.py
    ├── advanced_scenario_benchmark.py
    └── price_match_service.py
```

---

## 🛠️ Step-by-Step Execution Guide

### **Step 1: Verify Identity & IAM Decoupling (Mission 1)**
Run the IAM audit script to verify that each agent is bound to its dedicated service account and BigQuery dataset ACLs are enforced:
```bash
python3 scripts/check_iam_and_access.py
```
* **Expected Output**:
  - `Customer Personalization Agent` $\rightarrow$ `customer-personalization-sa`
  - `Price Match Agent` $\rightarrow$ `price-match-sa`
  - `Markdown Strategy Agent` $\rightarrow$ `markdown-strategy-sa`
  - `Promo Agent` $\rightarrow$ `promo-agent-sa`

### **Step 2: Test Ingress Gateway Model Armor Screening (Mission 3)**
Execute the prompt injection attack test suite to verify that adversarial jailbreaks are blocked at the Agent Gateway boundary (`HTTP 400`):
```bash
python3 scripts/verify_all_attacks.py
```
* **Expected Output**:
  - Attack vectors (`"SYSTEM OVERRIDE"`, `"DEBUG MODE"`) return `HTTP 400 Bad Request` (Intercepted).
  - Valid price match requests return `HTTP 200 OK`.

### **Step 3: Run the Advanced 12-Case Benchmark Suite**
Stress-test the Price Match Agent against boundary conditions, currency formatting variants, out-of-stock listings, margin floors, and security threats:
```bash
python3 scripts/advanced_scenario_benchmark.py
```
* **Expected Output**:
  - 12 out of 12 benchmark cases passed (`100% Pass Rate`).
  - Below-cost matches rejected by hard margin floor guardrail.

---

## 📚 Technical Reference Guide

### **1. Dedicated Service Accounts & Dataset ACLs**

| Agent Name | Dedicated Service Account | Restricted BigQuery Dataset |
| :--- | :--- | :--- |
| **Customer Personalization Agent** | `customer-personalization-sa@...` | `customer_data` |
| **Price Match Agent** | `price-match-sa@...` | `novasmart_pricing`, `competitor_data` |
| **Markdown Strategy Agent** | `markdown-strategy-sa@...` | `novasmart_pricing` |
| **Promo Agent** | `promo-agent-sa@...` | None (catalog promo read-only) |

---

### **2. Agent Gateway & Model Armor Configuration**
* **Gateway Endpoint**: `price-match-ingress-gateway`
* **Filter Name**: `PromptInjectionAndJailbreakFilter`
* **Confidence Threshold**: `MEDIUM_AND_ABOVE`
* **SDP Template**: Basic Sensitive Data Protection (PII masking)

---

### **3. OpenTelemetry Telemetry Settings**
The following environment variables are configured on reasoning engines for distributed tracing and message content logging:
```bash
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY="true"
OTEL_SEMCONV_STABILITY_OPT_IN="gen_ai_latest_experimental"
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="span_and_event"
OTEL_TRACES_SAMPLER="always_on"
```
