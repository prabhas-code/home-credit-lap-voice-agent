# VAPI.AI FREE DEPLOYMENT & TESTING GUIDE (NO CREDIT CARD REQUIRED)
## Home Credit Loan Against Property (LAP) AI Voice Agent

If Retell AI requires payment or credit card verification, **Vapi (https://vapi.ai)** is the recommended alternative:
- **Free Trial**: Grants **$10 in free call credits** immediately upon signing in with Google/Email (No credit card required).
- **Features**: Live microphone browser testing, automated audio recording, full transcript logging, and shareable call links.

---

## 🛠️ Step 1: Create a Free Account
1. Open [https://vapi.ai](https://vapi.ai) and click **"Get Started"** or **"Sign In with Google"**.
2. Go to the **Dashboard** -> click on **"Assistants"** in the left sidebar.
3. Click **"Create Assistant"** -> choose **"Blank Template"**.
4. Name: `Home Credit LAP Voice Advisor`.

---

## ⚙️ Step 2: Configure Assistant Settings

### A. Model Tab
- **Provider**: `OpenAI`
- **Model**: `gpt-4o` (or `gpt-4o-mini`)
- **Temperature**: `0.2`
- **First Message**:
  - English: `Hello, am I speaking with Mr. Rajesh Sharma?`
  - Hindi: `Namaste! Kya meri baat Rajesh ji se ho rahi hai?`
- **System Prompt**: Copy and paste from [`vapi/VAPI_SYSTEM_PROMPT.txt`](file:///d:/Voice_Agent/vapi/VAPI_SYSTEM_PROMPT.txt).

### B. Transcriber Tab (Speech-to-Text)
- **Provider**: `Deepgram`
- **Model**: `Nova-2`
- **Language**: `en-IN` (Indian English) or `hi` (Hindi)

### C. Voice Tab (Text-to-Speech)
- **Provider**: `11labs` (or `Cartesia` / `PlayHT` / `Azure`)
- **Voice**: `Sarah` or `Adrian` (or any natural Indian accent voice)

---

## 📞 Step 3: Test with Your Microphone (Web Call)
1. In the top right corner of the Vapi assistant page, click **"Talk to Assistant"** (the green phone/microphone icon).
2. Allow browser microphone access.
3. Speak naturally following the conversation flow:
   - Confirm identity.
   - Say property is residential flat in Noida worth 1.2 crore and you need 50 lakhs.
   - Say sole owner and original documents available.
   - Say salaried in IT with bank salary.
   - Say 10 years tenure.
4. Listen as the agent guides you to the Senior Loan Expert handoff.

---

## 🔗 Step 4: Get Your Call Recording & Transcript Link
1. Go to **"Call Logs"** on the left menu.
2. Click on your completed test call.
3. You will see:
   - 🎧 **Audio Player** with full call playback.
   - 📝 **Full Timestamped Transcript**.
   - ⏱️ **Latency & Cost Breakdown**.
4. Click **"Share"** (or copy the Call Log URL from your browser address bar) to submit.
