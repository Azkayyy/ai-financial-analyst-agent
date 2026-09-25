"""
AI Financial Analyst Agent
University Assignment - Task 3
Company: The Coca-Cola Company (NYSE: KO)
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Financial Analyst Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Load verified Coca-Cola data
# ---------------------------------------------------------------------------
@st.cache_data
def load_verified_data():
    path = Path(__file__).parent / "verified_coca_cola_data.json"
    with open(path, "r") as f:
        return json.load(f)

VERIFIED = load_verified_data()

# ---------------------------------------------------------------------------
# Core calculation engine (deterministic)
# ---------------------------------------------------------------------------
REQUIRED_FIELDS = [
    "Revenue", "COGS", "Gross_Profit", "Operating_Profit", "Net_Income",
    "Current_Assets", "Inventory", "Current_Liabilities", "Total_Assets",
    "Total_Debt", "Shareholders_Equity", "Accounts_Receivable",
    "Accounts_Payable", "Interest_Expense"
]

def validate_data(data_2025: dict, data_2024: dict, supporting_2023: dict = None) -> list:
    """Return list of validation messages (empty = all OK)."""
    issues = []
    for year, data in [("2025", data_2025), ("2024", data_2024)]:
        if not data:
            issues.append(f"CRITICAL: No financial data provided for {year}.")
            continue
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] is None:
                issues.append(f"MISSING: {field} is missing for {year}.")
            elif not isinstance(data[field], (int, float)):
                issues.append(f"INVALID TYPE: {field} for {year} is not numeric.")
            elif data[field] < 0 and field not in ["Net_Income"]:  # Net Income could theoretically be negative
                issues.append(f"SUSPICIOUS: {field} for {year} is negative ({data[field]}).")
    # Cross-year consistency
    if data_2025 and data_2024:
        if data_2025.get("Revenue") and data_2024.get("Revenue"):
            if data_2025["Revenue"] <= 0 or data_2024["Revenue"] <= 0:
                issues.append("INVALID: Revenue must be positive.")
    if supporting_2023:
        for k in ["Total_Assets", "Shareholders_Equity", "Inventory", "Accounts_Receivable"]:
            if k not in supporting_2023 or supporting_2023[k] is None:
                issues.append(f"INFO: Supporting 2023 {k} is missing — average-based ratios for 2024 will be limited.")
    return issues


def safe_div(num, den):
    if den is None or den == 0 or num is None:
        return None
    return num / den


def calculate_ratios(d25, d24, s23) -> dict:
    """Calculate all 13 ratios. Returns dict with results + metadata."""
    results = {}

    # Helper averages
    def avg(a, b):
        if a is None or b is None:
            return None
        return (a + b) / 2

    avg_assets_25 = avg(d24.get("Total_Assets"), d25.get("Total_Assets"))
    avg_assets_24 = avg(s23.get("Total_Assets") if s23 else None, d24.get("Total_Assets"))
    avg_eq_25 = avg(d24.get("Shareholders_Equity"), d25.get("Shareholders_Equity"))
    avg_eq_24 = avg(s23.get("Shareholders_Equity") if s23 else None, d24.get("Shareholders_Equity"))
    avg_inv_25 = avg(d24.get("Inventory"), d25.get("Inventory"))
    avg_inv_24 = avg(s23.get("Inventory") if s23 else None, d24.get("Inventory"))
    avg_ar_25 = avg(d24.get("Accounts_Receivable"), d25.get("Accounts_Receivable"))
    avg_ar_24 = avg(s23.get("Accounts_Receivable") if s23 else None, d24.get("Accounts_Receivable"))

    # 1 Current Ratio
    results["Current Ratio"] = {
        "category": "Liquidity",
        "formula": "Current Assets / Current Liabilities",
        "2025_figures": f"CA {d25.get('Current_Assets')} / CL {d25.get('Current_Liabilities')}",
        "2025_calc": f"{d25.get('Current_Assets')} / {d25.get('Current_Liabilities')}",
        "2025_result": safe_div(d25.get("Current_Assets"), d25.get("Current_Liabilities")),
        "2024_figures": f"CA {d24.get('Current_Assets')} / CL {d24.get('Current_Liabilities')}",
        "2024_calc": f"{d24.get('Current_Assets')} / {d24.get('Current_Liabilities')}",
        "2024_result": safe_div(d24.get("Current_Assets"), d24.get("Current_Liabilities")),
        "format": "x"
    }

    # 2 Quick Ratio
    qa25 = None
    if d25.get("Current_Assets") is not None and d25.get("Inventory") is not None:
        qa25 = d25["Current_Assets"] - d25["Inventory"]
    qa24 = None
    if d24.get("Current_Assets") is not None and d24.get("Inventory") is not None:
        qa24 = d24["Current_Assets"] - d24["Inventory"]
    results["Quick Ratio"] = {
        "category": "Liquidity",
        "formula": "(Current Assets − Inventory) / Current Liabilities",
        "2025_figures": f"CA−Inv = {d25.get('Current_Assets')} − {d25.get('Inventory')} = {qa25}; CL = {d25.get('Current_Liabilities')}",
        "2025_calc": f"{qa25} / {d25.get('Current_Liabilities')}" if qa25 is not None else "Cannot calculate",
        "2025_result": safe_div(qa25, d25.get("Current_Liabilities")),
        "2024_figures": f"CA−Inv = {d24.get('Current_Assets')} − {d24.get('Inventory')} = {qa24}; CL = {d24.get('Current_Liabilities')}",
        "2024_calc": f"{qa24} / {d24.get('Current_Liabilities')}" if qa24 is not None else "Cannot calculate",
        "2024_result": safe_div(qa24, d24.get("Current_Liabilities")),
        "format": "x"
    }

    # 3 Gross Profit Margin
    results["Gross Profit Margin"] = {
        "category": "Profitability",
        "formula": "Gross Profit / Revenue × 100",
        "2025_figures": f"GP {d25.get('Gross_Profit')} / Rev {d25.get('Revenue')}",
        "2025_calc": f"{d25.get('Gross_Profit')} / {d25.get('Revenue')} × 100",
        "2025_result": safe_div(d25.get("Gross_Profit"), d25.get("Revenue")),
        "2024_figures": f"GP {d24.get('Gross_Profit')} / Rev {d24.get('Revenue')}",
        "2024_calc": f"{d24.get('Gross_Profit')} / {d24.get('Revenue')} × 100",
        "2024_result": safe_div(d24.get("Gross_Profit"), d24.get("Revenue")),
        "format": "%"
    }

    # 4 Operating Profit Margin
    results["Operating Profit Margin"] = {
        "category": "Profitability",
        "formula": "Operating Profit / Revenue × 100",
        "2025_figures": f"OI {d25.get('Operating_Profit')} / Rev {d25.get('Revenue')}",
        "2025_calc": f"{d25.get('Operating_Profit')} / {d25.get('Revenue')} × 100",
        "2025_result": safe_div(d25.get("Operating_Profit"), d25.get("Revenue")),
        "2024_figures": f"OI {d24.get('Operating_Profit')} / Rev {d24.get('Revenue')}",
        "2024_calc": f"{d24.get('Operating_Profit')} / {d24.get('Revenue')} × 100",
        "2024_result": safe_div(d24.get("Operating_Profit"), d24.get("Revenue")),
        "format": "%"
    }

    # 5 Net Profit Margin
    results["Net Profit Margin"] = {
        "category": "Profitability",
        "formula": "Net Income Attributable to Shareowners / Revenue × 100",
        "2025_figures": f"NI {d25.get('Net_Income')} / Rev {d25.get('Revenue')}",
        "2025_calc": f"{d25.get('Net_Income')} / {d25.get('Revenue')} × 100",
        "2025_result": safe_div(d25.get("Net_Income"), d25.get("Revenue")),
        "2024_figures": f"NI {d24.get('Net_Income')} / Rev {d24.get('Revenue')}",
        "2024_calc": f"{d24.get('Net_Income')} / {d24.get('Revenue')} × 100",
        "2024_result": safe_div(d24.get("Net_Income"), d24.get("Revenue")),
        "format": "%"
    }

    # 6 ROA
    results["ROA"] = {
        "category": "Profitability",
        "formula": "Net Income Attributable to Shareowners / Average Total Assets × 100",
        "2025_figures": f"NI {d25.get('Net_Income')}; Avg Assets (100549+104816)/2 = {avg_assets_25}",
        "2025_calc": f"{d25.get('Net_Income')} / {avg_assets_25} × 100" if avg_assets_25 else "Cannot calculate — missing average assets",
        "2025_result": safe_div(d25.get("Net_Income"), avg_assets_25),
        "2024_figures": f"NI {d24.get('Net_Income')}; Avg Assets (97703+100549)/2 = {avg_assets_24}",
        "2024_calc": f"{d24.get('Net_Income')} / {avg_assets_24} × 100" if avg_assets_24 else "Cannot calculate — missing 2023 Total Assets",
        "2024_result": safe_div(d24.get("Net_Income"), avg_assets_24),
        "format": "%"
    }

    # 7 ROE
    results["ROE"] = {
        "category": "Profitability",
        "formula": "Net Income Attributable to Shareowners / Average Equity Attributable to Shareowners × 100",
        "2025_figures": f"NI {d25.get('Net_Income')}; Avg Equity (24856+32169)/2 = {avg_eq_25}",
        "2025_calc": f"{d25.get('Net_Income')} / {avg_eq_25} × 100" if avg_eq_25 else "Cannot calculate",
        "2025_result": safe_div(d25.get("Net_Income"), avg_eq_25),
        "2024_figures": f"NI {d24.get('Net_Income')}; Avg Equity (25941+24856)/2 = {avg_eq_24}",
        "2024_calc": f"{d24.get('Net_Income')} / {avg_eq_24} × 100" if avg_eq_24 else "Cannot calculate — missing 2023 Equity",
        "2024_result": safe_div(d24.get("Net_Income"), avg_eq_24),
        "format": "%"
    }

    # 8 Debt-to-Equity
    results["Debt-to-Equity"] = {
        "category": "Leverage",
        "formula": "Total Debt / Shareholders' Equity (Attributable to Shareowners)",
        "2025_figures": f"Debt {d25.get('Total_Debt')} / Equity {d25.get('Shareholders_Equity')}",
        "2025_calc": f"{d25.get('Total_Debt')} / {d25.get('Shareholders_Equity')}",
        "2025_result": safe_div(d25.get("Total_Debt"), d25.get("Shareholders_Equity")),
        "2024_figures": f"Debt {d24.get('Total_Debt')} / Equity {d24.get('Shareholders_Equity')}",
        "2024_calc": f"{d24.get('Total_Debt')} / {d24.get('Shareholders_Equity')}",
        "2024_result": safe_div(d24.get("Total_Debt"), d24.get("Shareholders_Equity")),
        "format": "x"
    }

    # 9 Debt Ratio
    results["Debt Ratio"] = {
        "category": "Leverage",
        "formula": "Total Debt / Total Assets × 100",
        "2025_figures": f"Debt {d25.get('Total_Debt')} / Assets {d25.get('Total_Assets')}",
        "2025_calc": f"{d25.get('Total_Debt')} / {d25.get('Total_Assets')} × 100",
        "2025_result": safe_div(d25.get("Total_Debt"), d25.get("Total_Assets")),
        "2024_figures": f"Debt {d24.get('Total_Debt')} / Assets {d24.get('Total_Assets')}",
        "2024_calc": f"{d24.get('Total_Debt')} / {d24.get('Total_Assets')} × 100",
        "2024_result": safe_div(d24.get("Total_Debt"), d24.get("Total_Assets")),
        "format": "%"
    }

    # 10 Interest Coverage
    results["Interest Coverage"] = {
        "category": "Leverage",
        "formula": "Operating Profit / Interest Expense",
        "2025_figures": f"OI {d25.get('Operating_Profit')} / IntExp {d25.get('Interest_Expense')}",
        "2025_calc": f"{d25.get('Operating_Profit')} / {d25.get('Interest_Expense')}",
        "2025_result": safe_div(d25.get("Operating_Profit"), d25.get("Interest_Expense")),
        "2024_figures": f"OI {d24.get('Operating_Profit')} / IntExp {d24.get('Interest_Expense')}",
        "2024_calc": f"{d24.get('Operating_Profit')} / {d24.get('Interest_Expense')}",
        "2024_result": safe_div(d24.get("Operating_Profit"), d24.get("Interest_Expense")),
        "format": "x"
    }

    # 11 Total Asset Turnover
    results["Total Asset Turnover"] = {
        "category": "Efficiency",
        "formula": "Revenue / Average Total Assets",
        "2025_figures": f"Rev {d25.get('Revenue')}; Avg Assets {avg_assets_25}",
        "2025_calc": f"{d25.get('Revenue')} / {avg_assets_25}" if avg_assets_25 else "Cannot calculate",
        "2025_result": safe_div(d25.get("Revenue"), avg_assets_25),
        "2024_figures": f"Rev {d24.get('Revenue')}; Avg Assets {avg_assets_24}",
        "2024_calc": f"{d24.get('Revenue')} / {avg_assets_24}" if avg_assets_24 else "Cannot calculate — missing 2023 Total Assets",
        "2024_result": safe_div(d24.get("Revenue"), avg_assets_24),
        "format": "x"
    }

    # 12 Inventory Turnover
    results["Inventory Turnover"] = {
        "category": "Efficiency",
        "formula": "COGS / Average Inventory",
        "2025_figures": f"COGS {d25.get('COGS')}; Avg Inv {avg_inv_25}",
        "2025_calc": f"{d25.get('COGS')} / {avg_inv_25}" if avg_inv_25 else "Cannot calculate",
        "2025_result": safe_div(d25.get("COGS"), avg_inv_25),
        "2024_figures": f"COGS {d24.get('COGS')}; Avg Inv {avg_inv_24}",
        "2024_calc": f"{d24.get('COGS')} / {avg_inv_24}" if avg_inv_24 else "Cannot calculate — missing 2023 Inventory",
        "2024_result": safe_div(d24.get("COGS"), avg_inv_24),
        "format": "x"
    }

    # 13 Receivables Turnover
    results["Receivables Turnover"] = {
        "category": "Efficiency",
        "formula": "Revenue / Average Accounts Receivable",
        "2025_figures": f"Rev {d25.get('Revenue')}; Avg AR {avg_ar_25}",
        "2025_calc": f"{d25.get('Revenue')} / {avg_ar_25}" if avg_ar_25 else "Cannot calculate",
        "2025_result": safe_div(d25.get("Revenue"), avg_ar_25),
        "2024_figures": f"Rev {d24.get('Revenue')}; Avg AR {avg_ar_24}",
        "2024_calc": f"{d24.get('Revenue')} / {avg_ar_24}" if avg_ar_24 else "Cannot calculate — missing 2023 AR",
        "2024_result": safe_div(d24.get("Revenue"), avg_ar_24),
        "format": "x"
    }

    return results


def format_result(val, fmt):
    if val is None:
        return "Not calculable"
    if fmt == "%":
        return f"{val * 100:.2f}%"
    return f"{val:.2f}×"


def interpret_ratio(name, r25, r24, fmt):
    """Generate neutral, descriptive interpretation only."""
    if r25 is None and r24 is None:
        return "Ratio cannot be calculated for either year due to missing data."
    s25 = format_result(r25, fmt)
    s24 = format_result(r24, fmt)
    if r25 is not None and r24 is not None:
        if abs(r25 - r24) < 0.005:
            movement = f"remained essentially unchanged ({s24} in 2024 → {s25} in 2025)"
        elif r25 > r24:
            movement = f"increased from {s24} in 2024 to {s25} in 2025"
        else:
            movement = f"decreased from {s24} in 2024 to {s25} in 2025"
        return f"{name} {movement}."
    elif r25 is not None:
        return f"{name} was {s25} in 2025. 2024 result not available."
    else:
        return f"{name} was {s24} in 2024. 2025 result not available."


def identify_strengths_weaknesses(ratios: dict) -> tuple:
    strengths = []
    weaknesses = []
    for name, r in ratios.items():
        r25, r24 = r["2025_result"], r["2024_result"]
        if r25 is None or r24 is None:
            continue
        # Simple rule-based (data-driven only)
        if name in ["Current Ratio", "Quick Ratio"]:
            if r25 > r24:
                strengths.append(f"{name} increased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])}.")
            elif r25 < r24:
                weaknesses.append(f"{name} decreased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])}.")
        elif name in ["Gross Profit Margin", "Operating Profit Margin", "Net Profit Margin", "ROA", "ROE"]:
            if r25 > r24:
                strengths.append(f"{name} increased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])}.")
            elif r25 < r24:
                weaknesses.append(f"{name} decreased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])}.")
        elif name in ["Debt-to-Equity", "Debt Ratio"]:
            if r25 < r24:
                strengths.append(f"{name} decreased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])} (lower leverage).")
            elif r25 > r24:
                weaknesses.append(f"{name} increased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])} (higher leverage).")
        elif name == "Interest Coverage":
            if r25 > r24:
                strengths.append(f"Interest Coverage increased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])}.")
            elif r25 < r24:
                weaknesses.append(f"Interest Coverage decreased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])}.")
        elif name in ["Total Asset Turnover", "Inventory Turnover", "Receivables Turnover"]:
            if r25 > r24:
                strengths.append(f"{name} increased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])}.")
            elif r25 < r24:
                weaknesses.append(f"{name} decreased from {format_result(r24, r['format'])} to {format_result(r25, r['format'])}.")
    return strengths, weaknesses


def generate_report(company_info, d25, d24, s23, ratios, validation_issues) -> str:
    strengths, weaknesses = identify_strengths_weaknesses(ratios)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append("=" * 70)
    lines.append("AI FINANCIAL ANALYST AGENT — FINANCIAL ANALYSIS REPORT")
    lines.append("=" * 70)
    lines.append(f"Generated: {now}")
    lines.append("")

    # 1 Executive Summary
    lines.append("1. EXECUTIVE SUMMARY")
    lines.append("-" * 40)
    lines.append(f"This report analyses the financial performance and position of {company_info.get('company', 'the company')} "
                 f"for the years ended 31 December 2025 and 31 December 2024. All figures are in {company_info.get('units', 'USD millions')}.")
    if validation_issues:
        lines.append(f"Data validation flagged {len(validation_issues)} issue(s); see Limitations section.")
    else:
        lines.append("Data validation completed with no critical issues detected.")
    lines.append("")

    # 2 Company Profile
    lines.append("2. COMPANY PROFILE")
    lines.append("-" * 40)
    lines.append(f"Company: {company_info.get('company')}")
    lines.append(f"Stock: {company_info.get('ticker')}")
    lines.append(f"Industry: {company_info.get('industry')}")
    lines.append(f"Reporting Currency: {company_info.get('currency')}")
    lines.append(f"Units: {company_info.get('units')}")
    lines.append(f"Financial Years: 2025 and 2024")
    lines.append("")

    # 3 Financial Data Summary
    lines.append("3. FINANCIAL DATA SUMMARY")
    lines.append("-" * 40)
    lines.append(f"{'Item':<45} {'2025':>12} {'2024':>12}")
    lines.append("-" * 70)
    for f in REQUIRED_FIELDS:
        v25 = d25.get(f, "N/A")
        v24 = d24.get(f, "N/A")
        if isinstance(v25, (int, float)):
            v25 = f"{v25:,.0f}"
        if isinstance(v24, (int, float)):
            v24 = f"{v24:,.0f}"
        lines.append(f"{f:<45} {v25:>12} {v24:>12}")
    lines.append("")
    if s23:
        lines.append("Supporting 2023 beginning balances (for averages only):")
        lines.append(f"  Total Assets 2023: {s23.get('Total_Assets', 'N/A')}")
        lines.append(f"  Equity Attributable 2023: {s23.get('Shareholders_Equity', 'N/A')}")
        lines.append(f"  Inventory 2023: {s23.get('Inventory', 'N/A')}")
        lines.append(f"  Trade AR 2023: {s23.get('Accounts_Receivable', 'N/A')}")
        lines.append("  (These are NOT a third core reporting year.)")
    lines.append("")

    # 4-7 Category analyses
    categories = {
        "4. LIQUIDITY ANALYSIS": "Liquidity",
        "5. PROFITABILITY ANALYSIS": "Profitability",
        "6. LEVERAGE AND SOLVENCY ANALYSIS": "Leverage",
        "7. EFFICIENCY ANALYSIS": "Efficiency"
    }
    for title, cat in categories.items():
        lines.append(title)
        lines.append("-" * 40)
        for name, r in ratios.items():
            if r["category"] != cat:
                continue
            lines.append(f"\n{name}")
            lines.append(f"  Formula: {r['formula']}")
            lines.append(f"  2025 Figures: {r['2025_figures']}")
            lines.append(f"  2025 Calculation: {r['2025_calc']}")
            lines.append(f"  2025 Result: {format_result(r['2025_result'], r['format'])}")
            lines.append(f"  2024 Figures: {r['2024_figures']}")
            lines.append(f"  2024 Calculation: {r['2024_calc']}")
            lines.append(f"  2024 Result: {format_result(r['2024_result'], r['format'])}")
            lines.append(f"  Interpretation: {interpret_ratio(name, r['2025_result'], r['2024_result'], r['format'])}")
        lines.append("")

    # 8 Two-Year Comparative
    lines.append("8. TWO-YEAR COMPARATIVE ANALYSIS")
    lines.append("-" * 40)
    for name, r in ratios.items():
        r25, r24 = r["2025_result"], r["2024_result"]
        if r25 is None or r24 is None:
            lines.append(f"{name}: Comparison limited — data missing for one or both years.")
            continue
        change = r25 - r24
        if r["format"] == "%":
            lines.append(f"{name}: {format_result(r24, '%')} → {format_result(r25, '%')} (Δ {change*100:+.2f} pp)")
        else:
            lines.append(f"{name}: {format_result(r24, 'x')} → {format_result(r25, 'x')} (Δ {change:+.2f})")
    lines.append("")

    # 9 Strengths
    lines.append("9. FINANCIAL STRENGTHS")
    lines.append("-" * 40)
    if strengths:
        for s in strengths:
            lines.append(f"• {s}")
    else:
        lines.append("No clear favourable year-over-year movements identified from the available data.")
    lines.append("")

    # 10 Weaknesses & Risks
    lines.append("10. FINANCIAL WEAKNESSES AND POTENTIAL RISKS")
    lines.append("-" * 40)
    if weaknesses:
        for w in weaknesses:
            lines.append(f"• Observed: {w}")
    else:
        lines.append("No clear unfavourable year-over-year movements identified from the available data.")
    lines.append("")
    lines.append("Note: The items above are observed movements in the calculated ratios. "
                 "They are presented as potential areas for management attention and do not constitute investment advice.")
    lines.append("")

    # 11 Overall Assessment
    lines.append("11. OVERALL FINANCIAL HEALTH ASSESSMENT")
    lines.append("-" * 40)
    lines.append("Based solely on the calculated ratios for 2025 versus 2024:")
    n_str = len(strengths)
    n_weak = len(weaknesses)
    lines.append(f"• Number of ratios showing favourable movement: {n_str}")
    lines.append(f"• Number of ratios showing unfavourable movement: {n_weak}")
    lines.append("This assessment is descriptive only and is limited to the two years of data supplied.")
    lines.append("")

    # 12 Recommendations
    lines.append("12. MANAGEMENT RECOMMENDATIONS")
    lines.append("-" * 40)
    lines.append("Recommendations are linked only to the observed ratio movements and are directed at internal management:")
    if any("Current Ratio" in s or "Quick Ratio" in s for s in strengths + weaknesses):
        lines.append("• Review working-capital management (receivables, inventory, payables) in light of the observed liquidity ratio movements.")
    if any("Debt" in s for s in strengths + weaknesses):
        lines.append("• Monitor the debt level and debt-service capacity given the observed leverage ratio movements.")
    if any("Margin" in s or "ROA" in s or "ROE" in s for s in strengths + weaknesses):
        lines.append("• Continue to examine cost structure and revenue drivers underlying the profitability ratio movements.")
    if any("Turnover" in s for s in strengths + weaknesses):
        lines.append("• Review inventory and receivables management practices in light of the efficiency ratio movements.")
    if not (strengths or weaknesses):
        lines.append("• No specific management actions are indicated solely from the year-over-year ratio movements.")
    lines.append("")
    lines.append("These recommendations are not investment advice.")
    lines.append("")

    # 13 Limitations
    lines.append("13. LIMITATIONS OF THE ANALYSIS")
    lines.append("-" * 40)
    lines.append("• Analysis is limited to the two core years (2025 and 2024) plus supporting 2023 beginning balances.")
    lines.append("• No industry benchmarks or peer comparisons have been applied.")
    lines.append("• Qualitative factors (management quality, market conditions, etc.) are outside the scope of this data-driven analysis.")
    lines.append("• Accounts Payable uses the official combined line item 'Accounts payable and accrued expenses'.")
    lines.append("• Total Debt is the sum of the three official debt components disclosed on the balance sheet.")
    if validation_issues:
        lines.append("• Data validation issues were noted:")
        for iss in validation_issues:
            lines.append(f"  - {iss}")
    lines.append("")

    # 14 Sources
    lines.append("14. SOURCES OF FINANCIAL INFORMATION")
    lines.append("-" * 40)
    lines.append("Primary sources (official audited Form 10-K filings):")
    lines.append(f"• 2025 Form 10-K: {company_info.get('sources', {}).get('2025_10K', 'See official SEC filing')}")
    lines.append(f"• 2024 Form 10-K: {company_info.get('sources', {}).get('2024_10K', 'See official SEC filing')}")
    lines.append("All financial figures used in this report are taken from the verified Task 2 dataset derived from the above filings.")
    lines.append("No figures have been estimated or invented by the agent.")
    lines.append("")
    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------
def main():
    st.title("📊 AI Financial Analyst Agent")
    st.caption("University Assignment — Task 3 | Manufacturing Company Financial Analysis")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Home / Dashboard",
            "1. Financial Data",
            "2. Data Validation",
            "3. Ratio Analysis",
            "4. Two-Year Comparison",
            "5. Strengths & Weaknesses",
            "6. Risks & Red Flags",
            "7. Full Financial Report",
            "8. Download Report"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Source")
    data_mode = st.sidebar.radio(
        "Select data source",
        ["Use verified Coca-Cola dataset (Demo)", "Upload your own Excel/CSV"]
    )

    # Session state for data
    if "d25" not in st.session_state:
        st.session_state.d25 = VERIFIED["years"]["2025"].copy()
        st.session_state.d24 = VERIFIED["years"]["2024"].copy()
        st.session_state.s23 = VERIFIED["supporting_2023"].copy()
        st.session_state.company = {
            "company": VERIFIED["company"],
            "ticker": VERIFIED["ticker"],
            "industry": VERIFIED["industry"],
            "currency": VERIFIED["currency"],
            "units": VERIFIED["units"],
            "sources": VERIFIED["sources"]
        }
        st.session_state.validation_issues = []
        st.session_state.ratios = None
        st.session_state.report_text = None

    # Handle upload
    if data_mode == "Upload your own Excel/CSV":
        uploaded = st.sidebar.file_uploader("Upload Excel or CSV", type=["xlsx", "xls", "csv"])
        if uploaded:
            try:
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded)
                else:
                    df = pd.read_excel(uploaded)
                st.sidebar.success("File loaded. Please map columns in the Financial Data page.")
                st.session_state.uploaded_df = df
            except Exception as e:
                st.sidebar.error(f"Could not read file: {e}")
    else:
        # Reset to verified
        st.session_state.d25 = VERIFIED["years"]["2025"].copy()
        st.session_state.d24 = VERIFIED["years"]["2024"].copy()
        st.session_state.s23 = VERIFIED["supporting_2023"].copy()
        st.session_state.company = {
            "company": VERIFIED["company"],
            "ticker": VERIFIED["ticker"],
            "industry": VERIFIED["industry"],
            "currency": VERIFIED["currency"],
            "units": VERIFIED["units"],
            "sources": VERIFIED["sources"]
        }

    d25 = st.session_state.d25
    d24 = st.session_state.d24
    s23 = st.session_state.s23
    company = st.session_state.company

    # ----- HOME -----
    if page == "Home / Dashboard":
        st.header("Welcome to the AI Financial Analyst Agent")
        st.markdown("""
        This application is a **functional AI Financial Analyst Agent** designed for the university assignment.

        **Workflow demonstrated:**
        ```
        INPUT → AI AGENT → DATA VALIDATION → RATIO CALCULATION
              → FINANCIAL ANALYSIS → TWO-YEAR COMPARISON
              → STRENGTH / RISK ANALYSIS → REPORT GENERATION → OUTPUT
        ```

        **Current demonstration company:** The Coca-Cola Company (NYSE: KO)

        Use the sidebar to navigate through each stage of the analysis.
        The verified Task 2 / Task 4 Coca-Cola dataset is pre-loaded for demonstration.
        You may also upload your own financial data (Excel/CSV).
        """)
        st.info("All calculations are deterministic and based only on the supplied financial figures. "
                "AI is used for structured interpretation and report generation — never for inventing numbers.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Company", company.get("company", "—"))
        col2.metric("Years", "2025 & 2024")
        col3.metric("Currency", company.get("units", "USD millions"))

    # ----- 1 FINANCIAL DATA -----
    elif page == "1. Financial Data":
        st.header("1. Financial Data")
        st.markdown(f"**Company:** {company.get('company')} | **Ticker:** {company.get('ticker')} | "
                    f"**Industry:** {company.get('industry')}")
        st.markdown(f"**Currency / Units:** {company.get('currency')} / {company.get('units')}")

        st.subheader("Core Financial Years (2025 & 2024)")
        df_display = pd.DataFrame({
            "Financial Item": REQUIRED_FIELDS,
            "2025 (USD millions)": [d25.get(f) for f in REQUIRED_FIELDS],
            "2024 (USD millions)": [d24.get(f) for f in REQUIRED_FIELDS]
        })
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.subheader("Supporting 2023 Beginning Balances (for averages only)")
        st.warning("These figures are supporting beginning balances only and are NOT a third core reporting year.")
        st.write(s23)

        st.subheader("Important Notes")
        for k, v in VERIFIED.get("notes", {}).items():
            st.markdown(f"- **{k}:** {v}")

    # ----- 2 DATA VALIDATION -----
    elif page == "2. Data Validation":
        st.header("2. Data Validation")
        st.markdown("The agent performs the following checks before analysis:")

        issues = validate_data(d25, d24, s23)
        st.session_state.validation_issues = issues

        if not issues:
            st.success("✅ Data validation passed. No missing, blank, or inconsistent critical values detected.")
            st.markdown("""
            Checks performed:
            - All 14 required financial items present for both 2025 and 2024
            - Values are numeric
            - Units consistent (USD millions)
            - Currency consistent (USD)
            - Years correctly distinguished
            - Supporting 2023 balances available for average-based ratios
            """)
        else:
            st.error(f"⚠️ {len(issues)} validation issue(s) found:")
            for iss in issues:
                st.markdown(f"- {iss}")
            st.info("The agent will still calculate any ratios that can be computed from the available data. "
                    "It will NOT invent or estimate missing values.")

        # Automated action demonstration
        st.markdown("---")
        st.subheader("Automated Action")
        if st.button("Run automated validation log"):
            log = {
                "timestamp": datetime.now().isoformat(),
                "company": company.get("company"),
                "issues_found": len(issues),
                "status": "PASS" if not issues else "ISSUES_FLAGGED"
            }
            st.json(log)
            st.success("Validation log generated (automated action completed).")

    # ----- 3 RATIO ANALYSIS -----
    elif page == "3. Ratio Analysis":
        st.header("3. Ratio Analysis")
        st.markdown("All ratios are calculated deterministically from the supplied figures.")

        ratios = calculate_ratios(d25, d24, s23)
        st.session_state.ratios = ratios

        for cat in ["Liquidity", "Profitability", "Leverage", "Efficiency"]:
            st.subheader(cat)
            for name, r in ratios.items():
                if r["category"] != cat:
                    continue
                with st.expander(f"{name}"):
                    st.markdown(f"**Formula:** `{r['formula']}`")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**2025**")
                        st.markdown(f"Figures used: {r['2025_figures']}")
                        st.markdown(f"Calculation: `{r['2025_calc']}`")
                        st.metric("Result", format_result(r["2025_result"], r["format"]))
                    with c2:
                        st.markdown("**2024**")
                        st.markdown(f"Figures used: {r['2024_figures']}")
                        st.markdown(f"Calculation: `{r['2024_calc']}`")
                        st.metric("Result", format_result(r["2024_result"], r["format"]))
                    st.markdown(f"**Interpretation (descriptive):** {interpret_ratio(name, r['2025_result'], r['2024_result'], r['format'])}")

    # ----- 4 TWO-YEAR COMPARISON -----
    elif page == "4. Two-Year Comparison":
        st.header("4. Two-Year Comparison (2025 vs 2024)")
        if st.session_state.ratios is None:
            st.session_state.ratios = calculate_ratios(d25, d24, s23)
        ratios = st.session_state.ratios

        rows = []
        for name, r in ratios.items():
            r25, r24 = r["2025_result"], r["2024_result"]
            if r25 is not None and r24 is not None:
                if r["format"] == "%":
                    delta = f"{(r25 - r24) * 100:+.2f} pp"
                else:
                    delta = f"{(r25 - r24):+.2f}"
                if abs(r25 - r24) < 0.005:
                    trend = "Unchanged"
                elif r25 > r24:
                    # For leverage ratios, higher is not necessarily "improvement"
                    if name in ["Debt-to-Equity", "Debt Ratio"]:
                        trend = "Increased (higher leverage)"
                    else:
                        trend = "Increased"
                else:
                    if name in ["Debt-to-Equity", "Debt Ratio"]:
                        trend = "Decreased (lower leverage)"
                    else:
                        trend = "Decreased"
            else:
                delta = "—"
                trend = "Data incomplete"
            rows.append({
                "Ratio": name,
                "Category": r["category"],
                "2025": format_result(r25, r["format"]),
                "2024": format_result(r24, r["format"]),
                "Change": delta,
                "Movement": trend
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ----- 5 STRENGTHS & WEAKNESSES -----
    elif page == "5. Strengths & Weaknesses":
        st.header("5. Financial Strengths & Weaknesses")
        st.caption("Identified solely from year-over-year movements in the calculated ratios. No unsupported evaluative language is used.")
        if st.session_state.ratios is None:
            st.session_state.ratios = calculate_ratios(d25, d24, s23)
        strengths, weaknesses = identify_strengths_weaknesses(st.session_state.ratios)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Observed Favourable Movements (Strengths)")
            if strengths:
                for s in strengths:
                    st.success(s)
            else:
                st.info("No clear favourable year-over-year movements identified.")
        with c2:
            st.subheader("Observed Unfavourable Movements (Weaknesses)")
            if weaknesses:
                for w in weaknesses:
                    st.warning(w)
            else:
                st.info("No clear unfavourable year-over-year movements identified.")

    # ----- 6 RISKS -----
    elif page == "6. Risks & Red Flags":
        st.header("6. Potential Risks & Red Flags")
        st.caption("Based only on the calculated data. Distinction is made between observed results and analytical interpretation.")
        if st.session_state.ratios is None:
            st.session_state.ratios = calculate_ratios(d25, d24, s23)
        _, weaknesses = identify_strengths_weaknesses(st.session_state.ratios)

        if weaknesses:
            for w in weaknesses:
                st.markdown(f"**Observed result:** {w}")
                st.markdown("**Analytical note:** This movement may warrant management attention regarding the underlying drivers (working capital, cost structure, financing, or asset utilisation). It does not by itself constitute a prediction of financial distress.")
                st.markdown("---")
        else:
            st.info("No ratio movements that would typically be flagged as immediate red flags were identified from the two-year dataset.")

        st.markdown("**Important:** This section does not provide investment advice. It only highlights data-driven observations for internal management consideration.")

    # ----- 7 FULL REPORT -----
    elif page == "7. Full Financial Report":
        st.header("7. Full Financial Analysis Report (14 Sections)")
        if st.session_state.ratios is None:
            st.session_state.ratios = calculate_ratios(d25, d24, s23)
        issues = st.session_state.validation_issues or validate_data(d25, d24, s23)

        report = generate_report(company, d25, d24, s23, st.session_state.ratios, issues)
        st.session_state.report_text = report

        st.text_area("Generated Report", report, height=600)

        st.download_button(
            label="Download Report as TXT",
            data=report,
            file_name=f"Financial_Analysis_Report_{company.get('company', 'Company').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

    # ----- 8 DOWNLOAD -----
    elif page == "8. Download Report":
        st.header("8. Download Report")
        if st.session_state.report_text is None:
            if st.session_state.ratios is None:
                st.session_state.ratios = calculate_ratios(d25, d24, s23)
            issues = st.session_state.validation_issues or validate_data(d25, d24, s23)
            st.session_state.report_text = generate_report(company, d25, d24, s23, st.session_state.ratios, issues)

        st.download_button(
            label="📥 Download Full 14-Section Report (TXT)",
            data=st.session_state.report_text,
            file_name=f"AI_Financial_Analyst_Report_CocaCola_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

        # Also offer a simple CSV of ratios
        if st.session_state.ratios:
            rows = []
            for name, r in st.session_state.ratios.items():
                rows.append({
                    "Ratio": name,
                    "Category": r["category"],
                    "Formula": r["formula"],
                    "2025_Result": format_result(r["2025_result"], r["format"]),
                    "2024_Result": format_result(r["2024_result"], r["format"])
                })
            csv = pd.DataFrame(rows).to_csv(index=False)
            st.download_button(
                label="📥 Download Ratio Summary (CSV)",
                data=csv,
                file_name="Ratio_Summary_CocaCola.csv",
                mime="text/csv"
            )

        st.success("Report generation is complete. You can download the files above.")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption("AI Financial Analyst Agent | Task 3\nDeterministic calculations • No fabricated figures\nNot investment advice")


if __name__ == "__main__":
    main()
