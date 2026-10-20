# -*- coding: utf-8 -*-
"""MCP Server for Mastercard First-Party Fraud & Pre-Arbitration Rebuttal Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import MastercardFirstPartyFraudPreArbitrationArbiter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "compile_mastercard_pre_arbitration_case",
        "description": "Assemble a Mastercard pre-arbitration evidence dossier under Collaboration Dispute Condition 4837/4853 to refute friendly fraud.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dispute_reference_number": {
                    "type": "string"
                },
                "claim_amount_usd": {
                    "type": "number"
                },
                "cardholder_ip_country_match": {
                    "type": "boolean"
                },
                "has_biometric_fido_authentication": {
                    "type": "boolean"
                },
                "prior_same_device_tx_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "digital_goods_download_timestamp": {
                    "type": "string"
                }
            },
            "required": [
                "dispute_reference_number",
                "claim_amount_usd",
                "cardholder_ip_country_match",
                "has_biometric_fido_authentication"
            ]
        }
    },
    {
        "name": "evaluate_arbitration_financial_risk",
        "description": "Assess risk vs reward of filing formal arbitration before Mastercard Arbitration Committee ($500 filing fee penalty risk).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "disputed_amount_usd": {
                    "type": "number"
                },
                "evidence_strength_score_pct": {
                    "type": "number"
                },
                "filing_fee_usd": {
                    "type": "number",
                    "description": "Standard Mastercard fee is $500"
                }
            },
            "required": [
                "disputed_amount_usd",
                "evidence_strength_score_pct"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-mastercard-first-party-fraud-pre-arbitration-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(MastercardFirstPartyFraudPreArbitrationArbiter, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-agentic-commerce-mastercard-first-party-fraud-pre-arbitration-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-mastercard-first-party-fraud-pre-arbitration-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
