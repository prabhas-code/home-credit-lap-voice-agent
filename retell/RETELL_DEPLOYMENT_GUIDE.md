# RETELL AI DEPLOYMENT & TESTING GUIDE (STEP-BY-STEP)
## Home Credit Loan Against Property (LAP) AI Voice Agent

Follow this exact guide to set up, configure, test, and generate the **Public Call Recording & Transcript Link** on **Retell AI** for your assignment submission.

---

## 📋 PRE-FLIGHT CHECKLIST
- Platform: [https://retellai.com](https://retellai.com) (Sign up for a free trial).
- Recommended LLM: **GPT-4o** (Default) or **Claude 3.5 Sonnet**.
- Recommended Voice: **ElevenLabs - Adrian** / **Sarah** / **Arya** / **Deepika** (Indian English / Hindi).
- Ready-to-paste Prompt File: [`retell/RETELL_SYSTEM_PROMPT.txt`](file:///d:/Voice_Agent/retell/RETELL_SYSTEM_PROMPT.txt).

---

## 🛠️ STEP 1: CREATE A NEW AGENT IN RETELL AI

1. Log in to [Retell AI Dashboard](https://dashboard.retellai.com).
2. On the left navigation bar, click on **"Agents"** -> **"Create New Agent"**.
3. Choose **"Single Prompt Agent"** (or Retell LLM).
4. Give your agent a name: `Home Credit LAP Voice Advisor`.

---

## ⚙️ STEP 2: CONFIGURE THE AGENT SETTINGS

### A. Model & Core Parameters
- **Model**: `gpt-4o` (or `gpt-4o-mini` / `claude-3-5-sonnet`)
- **Temperature**: `0.2` (Low temperature ensures strict compliance to business rules)
- **Responsiveness**: `0.9` (Fast turn-taking without awkward silence)
- **Interruption Sensitivity**: `0.8` (Allows caller to interrupt naturally)
- **Voice Speed**: `1.02` to `1.05` (Natural human cadence)
- **Ambient Sound**: `Call Center` or `Office` (Volume: `0.08` for authentic call center realism)

### B. Voice Selection
In the **Voice** dropdown:
- For **English (Indian)**: Select `ElevenLabs - Adrian` (Male) or `ElevenLabs - Sarah` / `Arya` (Female).
- For **Hindi / Hinglish**: Select `ElevenLabs - Arya` / `Deepika` or Cartesia Indian English/Hindi voice.
- Set **Agent Gender** accordingly:
  - If selecting a female voice -> set `agent_gender = female` and `agent_name = Priya`.
  - If selecting a male voice -> set `agent_gender = male` and `agent_name = Aarav`.

### C. Begin Message (First Spoken Message)
- **English**:
  ```text
  Hello, am I speaking with {{customer_name}}?
  ```
- **Hindi**:
  ```text
  Namaste! Kya meri baat {{customer_name}} ji se ho rahi hai?
  ```

---

## 📝 STEP 3: PASTE THE SYSTEM PROMPT

Copy the entire text from [`retell/RETELL_SYSTEM_PROMPT.txt`](file:///d:/Voice_Agent/retell/RETELL_SYSTEM_PROMPT.txt) and paste it into the **"General Prompt"** box in the Retell Agent Editor.

*(Note: Retell natively supports variables like `{{customer_name}}` and `{{company_name}}`).*

---

## 🎛️ STEP 4: SET UP DYNAMIC TEST VARIABLES

In Retell Agent Settings under **"Dynamic Variables"** (or Test Call Payload), add the following default key-value pairs:

```json
{
  "company_name": "Home Credit",
  "customer_name": "Mr. Rajesh Sharma",
  "agent_name": "Priya",
  "agent_gender": "female",
  "current_date": "2026-10-08",
  "current_day": "Thursday",
  "current_time": "04:30 PM",
  "language_to_speak": "English",
  "additional_context_from_rag": "Home Credit LAP offers up to 75 Lakhs, tenures 3-15 years, zero hidden charges, and customized rates provided post verification by senior loan experts."
}
```

*(For Hindi testing, change `language_to_speak` to `Hindi` and `customer_name` to `Rajesh`).*

---

## 🔌 STEP 5: ADD TOOLS / FUNCTIONS (OPTIONAL BUT RECOMMENDED)

In the **Tools** section:
1. Enable **"End Call"** tool (Retell built-in):
   - Trigger when the final handoff or exit script is spoken.
2. Set **End Call Phrases**:
   - `"Have a wonderful day"`
   - `"Have a great day"`
   - `"Aapka din shubh ho"`

---

## 📞 STEP 6: MAKE A LIVE TEST WEB CALL

1. In the top-right corner of the Retell agent page, click **"Test Call"** or **"Web Call"**.
2. Allow microphone access in your browser.
3. Speak naturally as a customer. Follow the scripts in [`retell/RETELL_TEST_CHEATSHEET.md`](file:///d:/Voice_Agent/retell/RETELL_TEST_CHEATSHEET.md).

---

## 🔗 STEP 7: OBTAIN THE PUBLIC RECORDING & TRANSCRIPT LINK

1. After the call finishes, navigate to **"Call History"** or **"Call Logs"** on the left menu of the Retell dashboard.
2. Click on the call you just completed.
3. You will see the **Audio Player** with waveform, along with the **Full Transcript** and **Latency Breakdown**.
4. Click the **"Share"** button (or **"Make Public"** toggle) at the top right of the call log.
5. Copy the generated **Public Call Link** (e.g. `https://dashboard.retellai.com/call/call_xxxxxxxxxxxx`).
6. Paste this link into your assignment submission.

---

## 🏆 SUBMISSION TEMPLATE

```markdown
### Home Credit LAP AI Voice Agent Submission
- **Voice Platform**: Retell AI
- **LLM Model**: GPT-4o
- **Voice ID**: ElevenLabs - Adrian / Sarah
- **Public Call Recording & Log URL**: [Insert your Retell Public Call Link here]
- **System Prompt**: (Available in prompts/system_prompt_english.txt and retell/RETELL_SYSTEM_PROMPT.txt)
- **Test Scenarios Verified**: 22 Baseline + 33 Adversarial (55/55 Passed, 100%)
```
