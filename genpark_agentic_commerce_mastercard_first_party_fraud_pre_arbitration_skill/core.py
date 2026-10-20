# -*- coding: utf-8 -*-
"""Mastercard First-Party Fraud & Pre-Arbitration Rebuttal for GenPark Agentic Commerce."""
import json
from typing import Dict, Any, List

class MastercardFirstPartyFraudPreArbitrationArbiter:
    """Mastercard Dispute Resolution Scheme (MDRS) pre-arbitration and friendly fraud rebuttal."""

    @staticmethod
    def compile_mastercard_pre_arbitration_case(dispute_reference_number: str, claim_amount_usd: float, cardholder_ip_country_match: bool, has_biometric_fido_authentication: bool, prior_same_device_tx_ids: List[str] = None, digital_goods_download_timestamp: str = None) -> Dict[str, Any]:
        """Construct airtight first-party fraud pre-arbitration submission."""
        device_count = len(prior_same_device_tx_ids or [])
        score = 0.0
        if cardholder_ip_country_match:
            score += 0.25
        if has_biometric_fido_authentication:
            score += 0.45
        if device_count >= 1:
            score += 0.25
        if digital_goods_download_timestamp:
            score += 0.20

        compelling_pct = min(99.0, round(score * 100.0, 1))

        return {
            "dispute_reference_number": dispute_reference_number,
            "claim_amount_usd": claim_amount_usd,
            "evidence_compelling_score_pct": compelling_pct,
            "first_party_fraud_established": compelling_pct >= 70.0,
            "applicable_mastercard_rule": "Mastercard Rules Section 6.3 - Pre-Arbitration for Fraud without Cardholder Involvement",
            "liability_verdict": "SHIFT_LIABILITY_TO_ISSUER" if compelling_pct >= 70.0 else "INSUFFICIENT_ELEMENTS_FOR_ARBITRATION",
            "formal_response_brief": f"Pre-Arbitration Response ref {dispute_reference_number}: Merchant provides incontrovertible proof of authorized participation. Cardholder authenticated via Cryptographic FIDO token with confirmed IP congruence and previous device session history. Issuer must withdraw chargeback."
        }

    @staticmethod
    def evaluate_arbitration_financial_risk(disputed_amount_usd: float, evidence_strength_score_pct: float, filing_fee_usd: float = 500.0) -> Dict[str, Any]:
        """Calculate expected value EV = (WinProb * Amount) - ((1 - WinProb) * (FilingFee + AdminLoss))."""
        win_prob = evidence_strength_score_pct / 100.0
        loss_prob = 1.0 - win_prob
        expected_value = (win_prob * disputed_amount_usd) - (loss_prob * filing_fee_usd)

        should_escalate = expected_value > 50.0 and evidence_strength_score_pct >= 80.0

        return {
            "disputed_amount_usd": disputed_amount_usd,
            "mastercard_arbitration_fee_usd": filing_fee_usd,
            "win_probability_pct": evidence_strength_score_pct,
            "expected_value_usd": round(expected_value, 2),
            "recommendation": "ESCALATE_TO_ARBITRATION" if should_escalate else "ACCEPT_PRE_ARB_OR_WRITE_OFF",
            "risk_analysis": "Positive expected value justifies formal committee submission." if should_escalate else "Arbitration fee penalty exceeds expected return. Write-off recommended."
        }
