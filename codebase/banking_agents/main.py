#!/usr/bin/env python3
"""Main Entrypoint to demonstrate all 3 Production Banking Agentic AI Workflows.

Run: python3 main.py
"""

import json
from banking_agents.models import Transaction, CommercialLoanApplication, HITLApprovalToken
from banking_agents.scenario1_fraud_triage import PaymentFraudTriageAgent
from banking_agents.scenario2_loan_underwriting import CommercialLoanUnderwritingAgent
from banking_agents.scenario3_ledger_reconciliation import LedgerReconciliationAgent


def print_banner(title: str):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def run_scenario_1_fraud_triage():
    print_banner("SCENARIO 1: Automated Payment Fraud Investigation & Dispute Triage Agent")
    agent = PaymentFraudTriageAgent()

    # Case A: Low Risk Transaction (Auto-Process)
    low_risk_txn = Transaction(
        transaction_id="TXN-101",
        account_id="ACC-5521",
        amount=15.00,
        merchant="Local Grocery",
        location="New York, US",
        timestamp="2026-09-26T12:00:00Z",
        device_id="DEV-REGISTERED-01"
    )
    print("\nExecuting Fraud Triage for Low Risk Transaction...")
    res_low = agent.execute_dispute_workflow(low_risk_txn)
    print(f"Status: {res_low['status']}")
    print(f"Message: {res_low['message']}")
    print(f"Assessment: Risk Level={res_low['assessment'].risk_level}, Score={res_low['assessment'].risk_score}")

    # Case B: High Risk Transaction - Without HITL Token (Blocked)
    high_risk_txn = Transaction(
        transaction_id="TXN-9001",
        account_id="ACC-4410",
        amount=5500.00,
        merchant="CryptoExchange Ltd",
        location="Foreign-Offshore",
        timestamp="2026-09-26T12:05:00Z",
        device_id="DEV-UNKNOWN-88"
    )
    print("\nExecuting Fraud Triage for High Risk Transaction (Without HITL Token)...")
    res_high_blocked = agent.execute_dispute_workflow(high_risk_txn)
    print(f"Status: {res_high_blocked['status']}")
    print(f"Message: {res_high_blocked['message']}")

    # Case C: High Risk Transaction - With Valid Fraud Manager HITL Token (Approved)
    valid_token = HITLApprovalToken(
        token_id="TOK-FRAUD-8819",
        approver_role="FRAUD_MANAGER",
        approver_id="MGR-JOHN-DOE",
        is_valid=True
    )
    print("\nExecuting Fraud Triage for High Risk Transaction (With Signed Fraud Manager Token)...")
    res_high_approved = agent.execute_dispute_workflow(high_risk_txn, approval_token=valid_token)
    print(f"Status: {res_high_approved['status']}")
    print(f"Message: {res_high_approved['message']}")


def run_scenario_2_loan_underwriting():
    print_banner("SCENARIO 2: Commercial Loan Underwriting & Compliance Auditor Agent")
    agent = CommercialLoanUnderwritingAgent()

    # Case A: Strong Application (Approved)
    good_app = CommercialLoanApplication(
        application_id="APP-8810",
        company_name="Apex Logistics Inc",
        tax_id="US-9912041",
        requested_amount=500000.0,
        annual_revenue=5000000.0,
        existing_debt=100000.0,
        operating_net_income=300000.0,
        credit_score=750
    )
    print("\nEvaluating Compliant Commercial Loan Application...")
    res_good = agent.evaluate_application(good_app)
    print(f"Application ID: {res_good.application_id} ({res_good.company_name})")
    print(f"Final Decision: {res_good.final_underwriting_decision}")
    print(f"DSCR Ratio: {res_good.dscr_ratio} (Compliant: {res_good.dscr_compliant})")
    print("Audit Notes:", json.dumps(res_good.audit_notes, indent=2))

    # Case B: Sanctions Blocked Entity (Rejected)
    sanctioned_app = CommercialLoanApplication(
        application_id="APP-9999",
        company_name="SANCTIONED_CORP_X",
        tax_id="US-0000001",
        requested_amount=1000000.0,
        annual_revenue=10000000.0,
        existing_debt=0.0,
        operating_net_income=1000000.0,
        credit_score=800
    )
    print("\nEvaluating Sanctions Blocked Entity...")
    res_sanctioned = agent.evaluate_application(sanctioned_app)
    print(f"Final Decision: {res_sanctioned.final_underwriting_decision}")
    print("Audit Notes:", json.dumps(res_sanctioned.audit_notes, indent=2))


def run_scenario_3_ledger_reconciliation():
    print_banner("SCENARIO 3: Real-Time Interbank Ledger Reconciliation Agent")
    agent = LedgerReconciliationAgent()

    # Case A: Execute Discrepancy Reconciliation Without Token (Paused)
    print("\nRunning Interbank Ledger Reconciliation (Without Treasury Token)...")
    res_paused = agent.execute_adjusting_entry("ENTRY-SWIFT-9910")
    print(f"Status: {res_paused['status']}")
    print(f"Message: {res_paused['message']}")

    # Case B: Execute Discrepancy Reconciliation With Treasury Manager Token (Approved)
    treasury_token = HITLApprovalToken(
        token_id="TOK-TREASURY-1102",
        approver_role="TREASURY_MANAGER",
        approver_id="TREASURY-VP-ALICE",
        is_valid=True
    )
    print("\nRunning Interbank Ledger Reconciliation (With Signed Treasury Manager Token)...")
    res_approved = agent.execute_adjusting_entry("ENTRY-SWIFT-9910", approval_token=treasury_token)
    print(f"Status: {res_approved['status']}")
    print(f"Message: {res_approved['message']}")


def main():
    print("Initializing Enterprise Banking Agentic AI Suite...")
    run_scenario_1_fraud_triage()
    run_scenario_2_loan_underwriting()
    run_scenario_3_ledger_reconciliation()
    print("\n" + "=" * 80)
    print(" ALL 3 BANKING AGENTIC SCENARIOS EXECUTED SUCCESSFULLY.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
