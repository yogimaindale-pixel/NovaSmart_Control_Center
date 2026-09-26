"""Core Banking Integration Tools & Governance Gates."""

from typing import List, Optional
from banking_agents.models import Transaction, LedgerEntry, HITLApprovalToken


class CoreBankingDBTool:
    """Mock Tool simulating Core Banking SQL/REST API integration."""

    def __init__(self):
        self.transactions = [
            Transaction(
                transaction_id="TXN-9001",
                account_id="ACC-4410",
                amount=4500.00,
                merchant="CryptoExchange Ltd",
                location="Foreign-Offshore",
                timestamp="2026-09-26T12:00:00Z",
                device_id="DEV-UNKNOWN-88"
            ),
            Transaction(
                transaction_id="TXN-9002",
                account_id="ACC-4410",
                amount=12.50,
                merchant="Coffee Shop",
                location="New York, US",
                timestamp="2026-09-26T11:30:00Z",
                device_id="DEV-IPHONE-01"
            )
        ]

    def get_transaction_history(self, account_id: str) -> List[Transaction]:
        return [t for t in self.transactions if t.account_id == account_id]

    def block_card(self, account_id: str) -> bool:
        """Mutating Tool Action: Blocks card for account."""
        return True


class SanctionsCheckerTool:
    """Mock Tool simulating OFAC and International Sanctions List Screening."""

    def __init__(self):
        self.blocked_entities = ["SANCTIONED_CORP_X", "OFAC_BLOCKED_LIMITED"]

    def run_sanctions_check(self, company_name: str, tax_id: str) -> bool:
        """Returns True if CLEAN (passed sanctions check), False if BLOCKED."""
        if company_name in self.blocked_entities:
            return False
        return True


class LedgerQueryTool:
    """Mock Tool simulating Interbank Ledger Comparison Engine."""

    def get_core_ledger_entry(self, entry_id: str) -> LedgerEntry:
        return LedgerEntry(
            entry_id=entry_id,
            system_source="CORE_BANKING",
            account_number="NOSTRO-88102",
            amount=1000000.00,
            transaction_type="WIRE_TRANSFER",
            timestamp="2026-09-26T10:00:00Z"
        )

    def get_swift_clearing_entry(self, entry_id: str) -> LedgerEntry:
        # Simulates a $150 clearing fee discrepancy
        return LedgerEntry(
            entry_id=entry_id,
            system_source="SWIFT_CLEARING",
            account_number="NOSTRO-88102",
            amount=999850.00,
            transaction_type="WIRE_TRANSFER",
            timestamp="2026-09-26T10:01:00Z"
        )


class HITLGovernanceGate:
    """Human-in-the-Loop Governance Gate for Mutating Banking Actions."""

    @staticmethod
    def verify_token(token: Optional[HITLApprovalToken], required_role: str) -> bool:
        if not token:
            return False
        if not token.is_valid:
            return False
        if token.approver_role != required_role:
            return False
        return True
