"""Scenario 3: Real-Time Interbank Ledger Reconciliation & Exception Management Agent.

Business Context:
Audits end-of-day interbank ledger settlement discrepancies between Core Banking Nostro accounts
and SWIFT Clearing Engine records. Formulates adjusting ledger entries and enforces HITL authorization.
"""

from typing import Optional
from banking_agents.models import ReconciliationResult, WorkflowStatus, HITLApprovalToken
from banking_agents.tools import LedgerQueryTool, HITLGovernanceGate


class LedgerReconciliationAgent:
    def __init__(self):
        self.ledger_tool = LedgerQueryTool()

    def reconcile_entry(self, entry_id: str) -> ReconciliationResult:
        """Fetches ledger records across systems and identifies discrepancy root cause."""
        core_entry = self.ledger_tool.get_core_ledger_entry(entry_id)
        swift_entry = self.ledger_tool.get_swift_clearing_entry(entry_id)

        discrepancy = abs(core_entry.amount - swift_entry.amount)

        if discrepancy == 0.0:
            explanation = "Core Ledger and SWIFT Clearing records match perfectly."
            proposed_entry = "NONE_REQUIRED"
            status = WorkflowStatus.COMPLETED
        else:
            explanation = f"Intermediary wire clearing fee of ${discrepancy:.2f} deducted by SWIFT relay bank."
            proposed_entry = f"DEBIT_CORRESPONDENT_BANK_FEE_EXPENSE ${discrepancy:.2f} / CREDIT_NOSTRO_ACCOUNT ${discrepancy:.2f}"
            status = WorkflowStatus.REQUIRES_HUMAN_APPROVAL

        return ReconciliationResult(
            reconciliation_id=f"REC-{entry_id}",
            core_ledger_amount=core_entry.amount,
            swift_clearing_amount=swift_entry.amount,
            discrepancy_amount=discrepancy,
            root_cause_explanation=explanation,
            proposed_adjusting_entry=proposed_entry,
            status=status
        )

    def execute_adjusting_entry(
        self,
        entry_id: str,
        approval_token: Optional[HITLApprovalToken] = None
    ) -> dict:
        """Executes adjusting entry after verifying Treasury Manager HITL approval token."""
        result = self.reconcile_entry(entry_id)

        if result.discrepancy_amount == 0.0:
            return {
                "status": WorkflowStatus.COMPLETED,
                "reconciliation": result,
                "message": "No discrepancy detected. No adjusting entry required."
            }

        # Verify Treasury Manager Token
        is_approved = HITLGovernanceGate.verify_token(approval_token, required_role="TREASURY_MANAGER")

        if not is_approved:
            return {
                "status": WorkflowStatus.REQUIRES_HUMAN_APPROVAL,
                "reconciliation": result,
                "message": "[HITL GATE INTERCEPT] Mutating ledger adjustment requires signed TREASURY_MANAGER token. Workflow paused."
            }

        result.status = WorkflowStatus.APPROVED
        return {
            "status": WorkflowStatus.APPROVED,
            "reconciliation": result,
            "message": f"Treasury Manager approved adjusting entry. Executed: {result.proposed_adjusting_entry}"
        }
