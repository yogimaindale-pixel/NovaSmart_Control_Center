"""Scenario 1: Automated Payment Fraud Investigation & Dispute Triage Agent.

Business Context:
Processes real-time transaction dispute alerts. Analyzes transaction velocity, location anomalies,
and device fingerprints. Automatically issues temporary refunds for Low Risk transactions.
Enforces a Human-in-the-Loop (HITL) gate before executing mutating card blocks on High Risk cases.
"""

from typing import Optional
from banking_agents.models import (
    Transaction, FraudAssessmentResult, RiskLevel,
    HITLApprovalToken, WorkflowStatus
)
from banking_agents.tools import CoreBankingDBTool, HITLGovernanceGate


class PaymentFraudTriageAgent:
    def __init__(self):
        self.banking_db = CoreBankingDBTool()

    def analyze_transaction_risk(self, transaction: Transaction) -> FraudAssessmentResult:
        """Evaluates transaction risk against baseline velocity and location tools."""
        anomalies = []
        score = 0.10  # Baseline low risk

        # Rule 1: High value offshore transaction
        if transaction.amount > 3000.0 and "Offshore" in transaction.location:
            score += 0.50
            anomalies.append(f"High amount (${transaction.amount}) in offshore location ({transaction.location})")

        # Rule 2: Device anomaly
        if "UNKNOWN" in transaction.device_id:
            score += 0.30
            anomalies.append("Unrecognized device fingerprint")

        # Determine Risk Tier
        if score >= 0.70:
            risk_level = RiskLevel.HIGH
            recommended_action = "BLOCK_CARD_AND_INITIATE_FRAUD_HOLD"
            requires_hitl = True
        elif score >= 0.40:
            risk_level = RiskLevel.MEDIUM
            recommended_action = "REQUEST_TWO_FACTOR_VERIFICATION"
            requires_hitl = False
        else:
            risk_level = RiskLevel.LOW
            recommended_action = "AUTO_PROCESS_TEMPORARY_DISPUTE_CREDIT"
            requires_hitl = False

        return FraudAssessmentResult(
            transaction_id=transaction.transaction_id,
            account_id=transaction.account_id,
            risk_level=risk_level,
            risk_score=round(score, 2),
            anomalies_detected=anomalies,
            recommended_action=recommended_action,
            requires_hitl_approval=requires_hitl
        )

    def execute_dispute_workflow(
        self,
        transaction: Transaction,
        approval_token: Optional[HITLApprovalToken] = None
    ) -> dict:
        """Runs end-to-end fraud triage workflow with HITL approval gate for card blocks."""
        assessment = self.analyze_transaction_risk(transaction)

        if not assessment.requires_hitl_approval:
            return {
                "status": WorkflowStatus.COMPLETED,
                "assessment": assessment,
                "action_executed": assessment.recommended_action,
                "message": f"Processed low/medium risk action automatically: {assessment.recommended_action}"
            }

        # High Risk Branch: Verify HITL Approval Token for Mutating Card Block
        is_approved = HITLGovernanceGate.verify_token(approval_token, required_role="FRAUD_MANAGER")

        if not is_approved:
            return {
                "status": WorkflowStatus.REQUIRES_HUMAN_APPROVAL,
                "assessment": assessment,
                "action_executed": "NONE",
                "message": "[HITL GATE INTERCEPT] Mutating action 'BLOCK_CARD' requires signed FRAUD_MANAGER token. Workflow paused."
            }

        # Token valid: Execute card block
        self.banking_db.block_card(transaction.account_id)
        return {
            "status": WorkflowStatus.APPROVED,
            "assessment": assessment,
            "action_executed": "CARD_BLOCKED_AND_HOLD_PLACED",
            "message": "Fraud Manager approved action. Card successfully blocked in Core Banking DB."
        }
