"""
Task 5 – External Automation Module
AI Financial Analyst Agent

Provides a real automated action:
  Streamlit Agent → Zapier Webhook → Google Sheets

No financial figures are invented here.
Only pushes results that have already been calculated by the agent.
"""

import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any


def build_payload(
    company: str,
    ticker: str,
    ratios: Dict[str, Any],
    strengths: list,
    weaknesses: list,
    validation_status: str,
) -> dict:
    """Build a clean JSON payload from already-calculated results."""
    ratio_summary = {}
    for name, r in ratios.items():
        ratio_summary[name] = {
            "category": r.get("category"),
            "result_2025": r.get("2025_result"),
            "result_2024": r.get("2024_result"),
            "format": r.get("format"),
        }

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "AI Financial Analyst Agent",
        "company": company,
        "ticker": ticker,
        "validation_status": validation_status,
        "ratios": ratio_summary,
        "strengths_count": len(strengths),
        "weaknesses_count": len(weaknesses),
        "strengths": strengths[:5],
        "weaknesses": weaknesses[:5],
        "note": "Automated push from Streamlit AI Financial Analyst Agent (Task 5)",
    }


def push_to_zapier_webhook(webhook_url: str, payload: dict) -> Dict[str, Any]:
    """
    Real external automated action.
    POSTs the analysis payload to a Zapier Catch Hook.
    Zapier then writes a row into Google Sheets (or creates a Google Doc).

    Returns a result dict with success/failure info.
    """
    if not webhook_url or not webhook_url.startswith("https://hooks.zapier.com/"):
        return {
            "success": False,
            "error": "Invalid or missing Zapier webhook URL. It must start with https://hooks.zapier.com/",
        }

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15,
        )
        if response.status_code in (200, 201):
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "Payload successfully sent to Zapier. Check your Google Sheet for the new row.",
                "response_text": response.text[:300],
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"Zapier returned status {response.status_code}: {response.text[:300]}",
            }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Check your internet connection."}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Network error: {str(e)}"}


def format_result_for_display(val, fmt: str) -> str:
    if val is None:
        return "N/A"
    if fmt == "%":
        return f"{val * 100:.2f}%"
    return f"{val:.2f}x"
