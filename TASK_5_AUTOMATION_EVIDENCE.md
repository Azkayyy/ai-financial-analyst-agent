# Task 5 – Automation & Agentic Workflow
## Evidence Document

**Company:** The Coca-Cola Company (NYSE: KO)  
**Agent:** AI Financial Analyst Agent (Streamlit)  
**External tool:** Zapier → Google Sheets  

---

## 1. Requirement (from assignment)

> The agent should be connected to at least one additional application or tool, such as:
> - Google Sheets for storing financial data or analysis results
> - Google Docs for generating the final report
> - Gmail for sending the report
> - Zapier Tables for storing company analyses
>
> Students should demonstrate at least one automated action beyond generating a text response.
>
> Minimum workflow:  
> **Input → AI Agent → Financial Analysis → Report Generation → Output**

---

## 2. Implementation

| Component | Implementation |
|-----------|----------------|
| AI Agent | Existing Streamlit application (`app.py`) |
| External connection | Zapier Catch Hook (Webhook) |
| Target application | Google Sheets (Create Spreadsheet Row) |
| Automated action | After analysis, the agent POSTs calculated ratio results + strengths/weaknesses summary to the Zapier webhook. Zapier automatically writes a new row into the connected Google Sheet. |
| Code module | `automation.py` |
| UI location | Page **“9. Automation (Task 5)”** inside the Streamlit app |

**Important:** No financial figures are invented. Only results that the agent has already calculated from the verified Task 2 data are pushed.

---

## 3. External tool used

- **Zapier** (free account) – Catch Hook trigger  
- **Google Sheets** – action “Create Spreadsheet Row”

---

## 4. Automated action (exactly what happens)

1. User completes analysis inside the Streamlit agent (or uses the pre-loaded Coca-Cola data).
2. User opens page **9. Automation (Task 5)**.
3. User pastes their Zapier Webhook URL.
4. User clicks **“Push Analysis Results to Google Sheet (via Zapier)”**.
5. The agent sends a JSON payload containing:
   - Timestamp
   - Company name & ticker
   - Validation status
   - All 13 ratio results (2025 & 2024)
   - Top strengths and weaknesses
6. Zapier receives the webhook and automatically creates a new row in the linked Google Sheet.
7. The new row is visible in Google Sheets within a few seconds.

This is a **real** external automated action, not a simulated button.

---

## 5. Complete workflow demonstrated

```
INPUT
  (Verified Coca-Cola Task 2 data  OR  user-uploaded Excel/CSV)
        ↓
AI FINANCIAL ANALYST AGENT
  (Streamlit application)
        ↓
DATA VALIDATION
        ↓
FINANCIAL RATIO ANALYSIS  (13 ratios)
        ↓
TWO-YEAR COMPARISON + STRENGTHS / WEAKNESSES
        ↓
REPORT GENERATION  (14-section report)
        ↓
AUTOMATED EXTERNAL ACTION
  Streamlit  →  Zapier Webhook  →  Google Sheets
        ↓
OUTPUT
  • On-screen report + downloadable TXT/CSV
  • New row written into Google Sheet (external)
```

---

## 6. Accounts / credentials required

| Item | Required? | Cost |
|------|-----------|------|
| Google account | Yes | Free |
| Zapier account | Yes | Free |
| Google Cloud / service account / API key | **No** | — |
| Paid plan | **No** | — |
| Streamlit secrets / OAuth | **No** (webhook URL is entered in the UI) | — |

---

## 7. Evidence / screenshots required

Capture and keep these screenshots for submission:

1. **Streamlit app – Page 9 “Automation (Task 5)”** showing the workflow and webhook field  
2. **Zapier Zap editor** showing:  
   - Trigger = Webhooks by Zapier → Catch Hook  
   - Action = Google Sheets → Create Spreadsheet Row  
3. **Zapier webhook URL** visible (you may blur the secret part if desired)  
4. **Streamlit app** after clicking “Push…” – success message  
5. **Google Sheet** showing the new row that appeared after the push (with timestamp / company / ratio values)  
6. **Overall workflow diagram** (from WORKFLOW.md or drawn)

---

## 8. Expected result when correctly configured

- Clicking the button returns a green success message in the Streamlit app.
- Within a few seconds a new row appears in the Google Sheet that is connected in the Zap.
- The row contains the company name, timestamp, validation status and ratio results that match the agent’s calculated numbers.

---

## 9. Files involved in Task 5

| File | Role |
|------|------|
| `app.py` | Added page “9. Automation (Task 5)” |
| `automation.py` | Builds payload and POSTs to Zapier webhook |
| `requirements.txt` | Includes `requests` |
| `TASK_5_AUTOMATION_EVIDENCE.md` | This evidence document |
| `WORKFLOW.md` | Updated to show external tool |

---

## 10. Status

**Task 5 is PARTIALLY complete in code.**  

The integration code and UI are ready.  
**Full completion requires the student to:**

1. Create a free Zapier account and build the Zap (Catch Hook → Google Sheets).  
2. Paste the webhook URL into the Streamlit app.  
3. Click the push button and capture the screenshots listed above.  

Until those configuration steps and screenshots are done, Task 5 cannot be marked fully complete for submission.
