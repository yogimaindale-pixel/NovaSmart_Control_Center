import json

class PriceMatchService:
    def __init__(self, project_id="qwiklabs-gcp-01-2aad14f2c696"):
        self.project_id = project_id
        self.max_automated_discount_pct = 10.0
        self.authorized_retailers = ["AlphaStore", "BetaBuy"]

    def evaluate_price_match(self, sku, competitor_name, competitor_price, shelf_price, wholesale_cost, competitor_stock, local_stock):
        discount_amount = shelf_price - competitor_price
        discount_pct = round((discount_amount / shelf_price) * 100.0, 1)

        # 1. Check Retailer Whitelist
        if competitor_name not in self.authorized_retailers:
            return {
                "status": "REJECTED",
                "reason": "UNAUTHORIZED_RETAILER",
                "message": f"Price match rejected: Retailer '{competitor_name}' is not an authorized partner.",
                "action": "DENIED_UNAUTHORIZED_RETAILER"
            }

        # 2. Check Competitor Inventory
        if competitor_stock <= 0:
            return {
                "status": "REJECTED",
                "reason": "COMPETITOR_OUT_OF_STOCK",
                "message": f"Price match rejected: Competitor item is out of stock.",
                "action": "DENIED_OUT_OF_STOCK"
            }

        # 3. Check Local Inventory
        if local_stock <= 0:
            return {
                "status": "REJECTED",
                "reason": "LOCAL_OUT_OF_STOCK",
                "message": f"Price match rejected: Local inventory is 0 or item is discontinued.",
                "action": "DENIED_LOCAL_OUT_OF_STOCK"
            }

        # 4. HARD MARGIN FLOOR GUARDRAIL (PREVENTS NEGATIVE MARGIN PROFIT LOSS)
        if competitor_price < wholesale_cost:
            margin_loss = wholesale_cost - competitor_price
            return {
                "status": "REJECTED_HARD_FLOOR",
                "reason": "BELOW_WHOLESALE_COST_FLOOR",
                "message": f"HARD MARGIN FLOOR VIOLATION: Competitor price (${competitor_price:.2f}) is below wholesale cost (${wholesale_cost:.2f}). Incurs -${margin_loss:.2f} profit loss.",
                "action": "DENIED_BELOW_COST",
                "wholesale_cost": wholesale_cost,
                "competitor_price": competitor_price,
                "margin_loss": margin_loss,
                "requires_escalation": False  # Hard block: Cannot be overridden below cost floor
            }

        # 5. Check Automated Approval Cap (10.0%)
        if discount_pct > self.max_automated_discount_pct:
            return {
                "status": "REQUIRES_MANAGER_ESCALATION",
                "reason": "EXCEEDS_AUTOMATED_DISCOUNT_CAP",
                "message": f"Requested discount ({discount_pct}%) exceeds automated cap ({self.max_automated_discount_pct}%). Escalated to Store Manager.",
                "action": "MANAGER_ESCALATION",
                "discount_pct": discount_pct
            }

        # 6. Approved
        return {
            "status": "APPROVED",
            "reason": "WITHIN_POLICY_LIMITS",
            "message": f"Price match approved at ${competitor_price:.2f} ({discount_pct}% discount).",
            "action": "AUTOMATED_APPROVAL",
            "approved_price": competitor_price,
            "discount_pct": discount_pct
        }

if __name__ == "__main__":
    service = PriceMatchService()
    # Test SC-04 / TC-05
    res = service.evaluate_price_match("SKU-LPT-1005", "BetaBuy", 400.00, 899.00, 650.00, 5, 10)
    print("Test TC-05 (Below Cost Match) Result:")
    print(json.dumps(res, indent=2))
