# Task 3 — Assignment Checklist

## A. Task 3 Requirements — Completion Status

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| 1 | Receive / access financial data | ✅ Done | Verified Coca-Cola data pre-loaded + Excel/CSV upload |
| 2 | Identify missing financial information | ✅ Done | Validation page + report Limitations section |
| 3 | Identify incorrect / inconsistent / invalid data | ✅ Done | Type, unit, currency, year checks |
| 4 | Check financial year, currency, units | ✅ Done | Explicitly validated |
| 5 | Calculate relevant financial ratios | ✅ Done | All 13 ratios with exact Task 4 methodology |
| 6 | Explain the meaning of each ratio | ✅ Done | Formula, figures, calculation, result, interpretation |
| 7 | Compare performance across two years | ✅ Done | Dedicated Two-Year Comparison page + report section |
| 8 | Identify financial strengths & weaknesses | ✅ Done | Data-driven from YoY movements only |
| 9 | Highlight potential risks and red flags | ✅ Done | Observed movements + analytical notes |
| 10 | Generate structured financial analysis report | ✅ Done | Full 14-section report + download |
| 11 | Handle missing data without fabricating | ✅ Done | Agent states “Not calculable” when data missing |
| 12 | At least one automated action | ✅ Done | Validation log generation |
| 13 | Suitable for teacher demonstration | ✅ Ready | After Streamlit Community Cloud deploy |

## B. Deliverables Created

| File | Description | Status |
|------|-------------|--------|
| `app.py` | Complete Streamlit application | ✅ Created |
| `verified_coca_cola_data.json` | Verified Task 2 financial data | ✅ Created |
| `requirements.txt` | Python dependencies | ✅ Created |
| `README.md` | Setup + deployment instructions | ✅ Created |
| `WORKFLOW.md` | Workflow diagram (text) | ✅ Created |
| `ASSIGNMENT_CHECKLIST.md` | This checklist | ✅ Created |

## C. Still Pending (your actions)

| Item | What you need to do |
|------|---------------------|
| Local test | Run `streamlit run app.py` and verify all pages |
| Deploy to Streamlit Community Cloud | Follow README.md steps → obtain public URL |
| Public shareable link | Send the `https://….streamlit.app` URL to your teacher |
| Screenshots | Capture the 9 pages listed in README.md |
| Final submission package | Source code + public URL + screenshots + earlier Task 2/4 Excel files |

## D. Screenshots you should capture

1. Home / Dashboard  
2. Financial Data (showing all 14 items)  
3. Data Validation (pass result + automated log)  
4. Ratio Analysis (at least one expander open showing formula + calculation)  
5. Two-Year Comparison table  
6. Strengths & Weaknesses  
7. Risks & Red Flags  
8. Full Financial Report (scroll or key sections)  
9. Download Report page  

## E. Exact next steps for you

1. Download the entire `ai_financial_analyst_agent` folder.
2. Test locally:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. Deploy to Streamlit Community Cloud (see README.md).
4. Copy the public URL.
5. Capture screenshots.
6. Submit to your teacher:
   - Public URL
   - Screenshots
   - Source code folder
   - Previously verified Task 2 & Task 4 Excel files
