"""Pydantic data models and contracts for Banking Agentic Workflows."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class WorkflowStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    ANALYZING = "ANALYZING"
    REQUIRES_HUMAN_APPROVAL = "REQUIRES_HUMAN_APPROVAL"
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


# --- Scenario 1: Fraud Triage Schemas ---

class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    currency: str = "USD"
    merchant: str
    location: str
    timestamp: str
    device_id: str


class FraudAssessmentResult(BaseModel):
    transaction_id: str
    account_id: str
    risk_level: RiskLevel
    risk_score: float = Field(ge=0.0, le=1.0)
    anomalies_detected: List[str]
    recommended_action: str
    requires_hitl_approval: bool


# --- Scenario 2: Commercial Loan Underwriting Schemas ---

class CommercialLoanApplication(BaseModel):
    application_id: str
    company_name: str
    tax_id: str
    requested_amount: float
    annual_revenue: float
    existing_debt: float
    operating_net_income: float
    credit_score: int


class ComplianceAuditResult(BaseModel):
    application_id: str
    company_name: str
    sanctions_check_passed: bool
    dscr_ratio: float
    dscr_compliant: bool
    credit_score_compliant: bool
    final_underwriting_decision: str
    audit_notes: List[str]


# --- Scenario 3: Ledger Reconciliation Schemas ---

class LedgerEntry(BaseModel):
    entry_id: str
    system_source: str  # e.g., "CORE_BANKING" or "SWIFT_CLEARING"
    account_number: str
    amount: float
    currency: str = "USD"
    transaction_type: str
    timestamp: str


class ReconciliationResult(BaseModel):
    reconciliation_id: str
    core_ledger_amount: float
    swift_clearing_amount: float
    discrepancy_amount: float
    root_cause_explanation: str
    proposed_adjusting_entry: str
    status: WorkflowStatus


class HITLApprovalToken(BaseModel):
    token_id: str
    approver_role: str
    approver_id: str
    is_valid: bool
