"""Unit Tests for Banking Agentic Workflows using Standard Library unittest."""

import unittest
from banking_agents.models import Transaction, CommercialLoanApplication, HITLApprovalToken, RiskLevel, WorkflowStatus
from banking_agents.scenario1_fraud_triage import PaymentFraudTriageAgent
from banking_agents.scenario2_loan_underwriting import CommercialLoanUnderwritingAgent
from banking_agents.scenario3_ledger_reconciliation import LedgerReconciliationAgent


class TestBankingAgents(unittest.TestCase):

    def test_fraud_triage_low_risk(self):
        agent = PaymentFraudTriageAgent()
        txn = Transaction(
            transaction_id="T1",
            account_id="ACC1",
            amount=20.0,
            merchant="Store",
            location="NY",
            timestamp="2026-09-26T12:00:00Z",
            device_id="DEV1"
        )
        res = agent.execute_dispute_workflow(txn)
        self.assertEqual(res["status"], WorkflowStatus.COMPLETED)
        self.assertEqual(res["assessment"].risk_level, RiskLevel.LOW)

    def test_fraud_triage_high_risk_hitl(self):
        agent = PaymentFraudTriageAgent()
        high_txn = Transaction(
            transaction_id="T2",
            account_id="ACC2",
            amount=6000.0,
            merchant="Crypto",
            location="Foreign-Offshore",
            timestamp="2026-09-26T12:00:00Z",
            device_id="DEV-UNKNOWN"
        )
        # Without Token -> Blocked
        res_blocked = agent.execute_dispute_workflow(high_txn)
        self.assertEqual(res_blocked["status"], WorkflowStatus.REQUIRES_HUMAN_APPROVAL)

        # With Token -> Approved
        token = HITLApprovalToken(
            token_id="TOK1",
            approver_role="FRAUD_MANAGER",
            approver_id="MGR1",
            is_valid=True
        )
        res_approved = agent.execute_dispute_workflow(high_txn, approval_token=token)
        self.assertEqual(res_approved["status"], WorkflowStatus.APPROVED)

    def test_loan_underwriting_compliant(self):
        agent = CommercialLoanUnderwritingAgent()
        app = CommercialLoanApplication(
            application_id="APP1",
            company_name="Good Corp",
            tax_id="US-12345",
            requested_amount=100000.0,
            annual_revenue=1000000.0,
            existing_debt=10000.0,
            operating_net_income=200000.0,
            credit_score=720
        )
        res = agent.evaluate_application(app)
        self.assertTrue(res.sanctions_check_passed)
        self.assertTrue(res.dscr_compliant)
        self.assertEqual(res.final_underwriting_decision, "APPROVED_COMMERCIAL_CREDIT")

    def test_ledger_reconciliation_hitl(self):
        agent = LedgerReconciliationAgent()
        # Without Token -> Intercepted
        res_paused = agent.execute_adjusting_entry("ENTRY-SWIFT-9910")
        self.assertEqual(res_paused["status"], WorkflowStatus.REQUIRES_HUMAN_APPROVAL)

        # With Token -> Approved
        token = HITLApprovalToken(
            token_id="TOK2",
            approver_role="TREASURY_MANAGER",
            approver_id="VP1",
            is_valid=True
        )
        res_approved = agent.execute_adjusting_entry("ENTRY-SWIFT-9910", approval_token=token)
        self.assertEqual(res_approved["status"], WorkflowStatus.APPROVED)


if __name__ == "__main__":
    unittest.main()
