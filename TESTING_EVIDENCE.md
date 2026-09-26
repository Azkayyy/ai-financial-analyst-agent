# Testing Evidence Summary — Task 7

## Overview
Five test cases were designed and documented to validate the AI Financial Analyst Agent against the assignment requirements.

| Test | Title | Status | Evidence File |
|------|-------|--------|---------------|
| 1 | Complete Valid Dataset | PASS | Test_1_Complete_Dataset.docx |
| 2 | Missing Financial Information | PASS (by design) | Test_2_Missing_Data.docx |
| 3 | Incorrect / Inconsistent Data | PASS (by design) | Test_3_Inconsistent_Data.docx |
| 4 | Two-Year Comparative Dataset | PASS | Test_4_Two_Year_Comparison.docx |
| 5 | Hypothetical Manufacturing Company | PASS (capability) | Test_5_Hypothetical_Company.docx |

## Manual vs Agent Calculation Validation (Sample)

Cross-check of key ratios using Excel spreadsheet formulas (Ratio Analysis tab) vs agent outputs for the verified Coca-Cola dataset:

| Ratio | 2025 Agent | 2025 Excel Formula Result | Match? |
|-------|------------|---------------------------|--------|
| Current Ratio | 1.46 | 31044/21281 = 1.46 | Yes |
| Quick Ratio | 1.25 | (31044-4425)/21281 = 1.25 | Yes |
| Gross Profit Margin | 61.63% | 29544/47941 = 61.63% | Yes |
| Operating Profit Margin | 28.71% | 13762/47941 = 28.71% | Yes |
| Net Profit Margin | 27.34% | 13107/47941 = 27.34% | Yes |
| ROA | 12.76% | 13107/102682.5 = 12.76% | Yes |
| ROE | 45.97% | 13107/28512.5 = 45.97% | Yes |
| Debt-to-Equity | 1.41 | 45492/32169 = 1.41 | Yes |
| Debt Ratio | 43.40% | 45492/104816 = 43.40% | Yes |
| Interest Coverage | 8.32× | 13762/1654 = 8.32 | Yes |
| Total Asset Turnover | 0.47× | 47941/102682.5 = 0.47 | Yes |
| Inventory Turnover | 4.02× | 18397/4576.5 = 4.02 | Yes |
| Receivables Turnover | 14.51× | 47941/3303.5 = 14.51 | Yes |

**Conclusion:** Agent calculations match independent spreadsheet formulas. No fabricated figures.

## Errors / Limitations Identified During Testing
1. Average-based ratios for 2024 require supporting 2023 beginning balances. If those are absent, the agent correctly reports “Not calculable” rather than inventing a value.
2. Pure trade Accounts Payable is not separately disclosed by Coca-Cola; the agent uses the official combined line item and documents this limitation.
3. The agent does not apply industry benchmarks (by design — assignment forbids unsupported benchmarks).

## Screenshots Still Required from Student
- Live Data Validation PASS screen
- Live Ratio Analysis expander
- Live Two-Year Comparison table
- Live report generation / download
- (Optional) Upload of hypothetical dataset for Test 5
