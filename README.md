# 🛡️ NovaSmart Control Center · Govern Your AI Estate

The **NovaSmart Control Center** repository provides an enterprise-grade AI governance, identity isolation, content screening, and telemetry management framework for multi-agent ecosystems deployed on Google Cloud Platform.

---

## 🌟 Key Features & Governance Capabilities

1. **Identity Isolation & IAM Least-Privilege**: Decoupled 4 production agents into dedicated service accounts, strictly restricting BigQuery dataset access (`customer_data`, `novasmart_pricing`, `competitor_data`).
2. **Agent Gateway Ingress Content Screening**: Deployed Model Armor `PromptInjectionAndJailbreakFilter` on Agent Gateways to intercept authority impersonation and system prompt leakage attacks (`HTTP 400`) before model token consumption.
3. **Hard Code-Level Margin Floor Guardrail**: Programmatically enforced wholesale cost floors ($\text{Min Price} = \max(\text{Shelf Price} \times 0.90, \text{Wholesale Cost})$) to prevent negative gross profit sales.
4. **OpenTelemetry Telemetry & Message Content Logging**: Configured OpenTelemetry GenAI semantic conventions across reasoning engines to export span trees and prompt/response payloads to Cloud Trace and Cloud Logging.
5. **12-Case Benchmark Suite**: Comprehensive benchmark test suite covering mathematical boundary conditions, out-of-stock listings, currency parsing, volume B2B requests, and prompt injection attacks.

---

## 📂 Repository Contents

* `README.md` — Project Overview & Key Features
* `INSTRUCTIONS_AND_REFERENCE_GUIDE.md` — Step-by-Step Execution & Reference Manual
* `SESSION_HISTORY_AND_COMMAND_LOGS.md` — Chronological Log of Prompts, Commands, and Results
* `scorecards/` — Governance Scorecards for Mission 1, Mission 3, Mission 4, and Price Match Benchmarks
* `scripts/` — Python Audit Scripts, Verification Suite, and Guardrail Logic

---

## 🏁 Quick Command Summary

```bash
# 1. Audit IAM & BigQuery Dataset Access
python3 scripts/check_iam_and_access.py

# 2. Test Agent Gateway Prompt Injection Ingress Screening
python3 scripts/verify_all_attacks.py

# 3. Execute 12-Case Price Match Evaluation Benchmark Suite
python3 scripts/advanced_scenario_benchmark.py
```
