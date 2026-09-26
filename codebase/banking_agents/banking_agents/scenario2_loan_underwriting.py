"""Scenario 2: Commercial Loan Underwriting & Regulatory Compliance Auditor Agent.

Business Context:
Evaluates commercial credit applications against regulatory standards (DSCR >= 1.25,
OFAC/Sanctions list screening, Credit Score >= 680). Generates an auditable Underwriting Brief.
"""

from banking_agents.models import CommercialLoanApplication, ComplianceAuditResult
from banking_agents.tools import SanctionsCheckerTool


class CommercialLoanUnderwritingAgent:
    def __init__(self):
        self.sanctions_tool = SanctionsCheckerTool()

    def calculate_dscr(self, application: CommercialLoanApplication) -> float:
        """Calculates Debt-Service Coverage Ratio (DSCR).

        DSCR = Operating Net Income / Total Debt Service
        """
        total_debt_service = application.existing_debt + (application.requested_amount * 0.10)  # 10% annual debt service
        if total_debt_service == 0:
            return 999.0
        return round(application.operating_net_income / total_debt_service, 2)

    def evaluate_application(self, application: CommercialLoanApplication) -> ComplianceAuditResult:
        """Runs compliance audit and underwriting evaluation."""
        audit_notes = []

        # Step 1: Sanctions Check
        sanctions_clean = self.sanctions_tool.run_sanctions_check(
            company_name=application.company_name,
            tax_id=application.tax_id
        )
        if not sanctions_clean:
            audit_notes.append("CRITICAL: Entity matched OFAC / Sanctions watchlist.")
        else:
            audit_notes.append("Sanctions screening passed clean.")

        # Step 2: DSCR Compliance (Regulatory standard DSCR >= 1.25)
        dscr = self.calculate_dscr(application)
        dscr_compliant = dscr >= 1.25
        if dscr_compliant:
            audit_notes.append(f"DSCR of {dscr} meets regulatory threshold (>= 1.25).")
        else:
            audit_notes.append(f"DSCR of {dscr} failed regulatory threshold (>= 1.25).")

        # Step 3: Credit Score Compliance
        credit_compliant = application.credit_score >= 680
        if credit_compliant:
            audit_notes.append(f"Credit score of {application.credit_score} meets threshold (>= 680).")
        else:
            audit_notes.append(f"Credit score of {application.credit_score} below minimum threshold (680).")

        # Step 4: Final Underwriting Decision
        if not sanctions_clean:
            decision = "REJECTED_SANCTIONS_MATCH"
        elif dscr_compliant and credit_compliant:
            decision = "APPROVED_COMMERCIAL_CREDIT"
        elif dscr >= 1.0 and credit_compliant:
            decision = "REFER_TO_SENIOR_CREDIT_COMMITTEE"
        else:
            decision = "REJECTED_INSUFFICIENT_COVERAGE"

        return ComplianceAuditResult(
            application_id=application.application_id,
            company_name=application.company_name,
            sanctions_check_passed=sanctions_clean,
            dscr_ratio=dscr,
            dscr_compliant=dscr_compliant,
            credit_score_compliant=credit_compliant,
            final_underwriting_decision=decision,
            audit_notes=audit_notes
        )
