# AI Financial Analyst Agent — Complete Workflow

```
INPUT
  (Verified Coca-Cola Task 2 data  OR  user-uploaded Excel/CSV)
        ↓
FINANCIAL DATA
  (14 line items × 2 years + supporting 2023 balances)
        ↓
AI FINANCIAL ANALYST AGENT
  (Streamlit application)
        ↓
DATA VALIDATION
  (Missing / type / unit / currency / year / consistency checks)
        ↓
RATIO CALCULATION
  (13 ratios — Liquidity, Profitability, Leverage, Efficiency)
        ↓
TWO-YEAR COMPARISON
  (2025 vs 2024 numerical changes + movement classification)
        ↓
STRENGTHS / WEAKNESSES
  (Derived only from calculated YoY movements)
        ↓
RISKS / RED FLAGS
  (Observed results + analytical notes; no invented risks)
        ↓
FINANCIAL REPORT GENERATION
  (14 mandatory sections; calculated results vs interpretations)
        ↓
AUTOMATED EXTERNAL ACTION (Task 5)
  Streamlit → Zapier Webhook → Google Sheets
        ↓
OUTPUT
  • On-screen report
  • Downloadable TXT report + CSV ratio summary
  • New row in connected Google Sheet
  • Public URL for teacher demonstration
```

Public application: https://coca-cola-financial-analyst.streamlit.app
