# AI Financial Analyst Agent — Workflow

```
┌─────────────────────────────────────┐
│              INPUT                  │
│  • Verified Coca-Cola Task 2 data   │
│  • Optional user Excel/CSV upload   │
│  • Company metadata                 │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│     AI FINANCIAL ANALYST AGENT      │
│  (Streamlit application + rules)    │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         DATA VALIDATION             │
│  • Missing values                   │
│  • Type / unit / currency checks    │
│  • Year consistency                 │
│  • Automated validation log         │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│       RATIO CALCULATION             │
│  • 13 ratios (Liquidity,            │
│    Profitability, Leverage,         │
│    Efficiency)                      │
│  • Exact Task 4 methodology         │
│  • Averages using 2023 supports     │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│      FINANCIAL ANALYSIS             │
│  • Formula + figures + calculation  │
│  • Result + descriptive interpretation │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│      TWO-YEAR COMPARISON            │
│  • 2025 vs 2024 numerical changes   │
│  • Movement classification          │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│   STRENGTH / RISK ANALYSIS          │
│  • Favourable movements             │
│  • Unfavourable movements           │
│  • Potential risks (data-driven)    │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│      REPORT GENERATION              │
│  • 14 required sections             │
│  • Calculated results separated     │
│    from interpretations             │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│              OUTPUT                 │
│  • On-screen 14-section report      │
│  • Downloadable TXT report          │
│  • Downloadable CSV ratio summary   │
└─────────────────────────────────────┘
```

## Automated action included
After validation, the agent can generate a structured validation log (timestamp, company, issues found, status). This satisfies the requirement for at least one automated action beyond simply displaying text.
