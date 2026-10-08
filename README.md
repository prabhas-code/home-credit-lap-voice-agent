# Home Credit Loan Against Property (LAP) AI Voice Qualification Agent

An enterprise-grade, conversational AI Voice Agent designed to conduct outbound preliminary qualification for **Home Credit's** pre-approved **Loan Against Property (LAP)** offer (up to ₹75,00,000 / 75 Lakhs).

---

## 🌟 Key Capabilities & Features
- **7-Point Qualification Gate**: Evaluates Property Type, Ownership Status, Original Document Availability, Loan Amount (capped at ₹75L), Occupation & Bank Income Mode, Property Market Value, and Repayment Tenure (3–15 years).
- **Immediate Disqualification Engine**: Instantly ceases qualification and exits politely on fatal ineligibility (Agricultural land, Cash-only income, Missing original documents, or refused parameters) without interrogation fatigue.
- **Dynamic Slot-Filling & Deduplication**: Intelligently extracts out-of-order and compound multi-slot answers without asking redundant questions.
- **Transfer / EMI Reduction Switch**: Automatically routes existing borrowers and EMI-reduction seekers to dedicated Loan Transfer Specialists.
- **Bilingual & Gender-Congruent**: Seamlessly operates in Indian English and Hindi/Hinglish with strict grammatical alignment for agent gender (`agent_gender`).
- **Zero Hallucination Guardrails**: Defers interest rates, processing fees, and final approvals to human Senior Loan Experts.

---

## 📂 Repository Structure
```
Voice_Agent/
├── SYSTEM_PROMPT.md                      # Master Production System Prompt
├── SUBMISSION_REPORT.md                  # Comprehensive Hiring Assignment Deliverables Report
├── README.md                             # Project Overview & Execution Guide
├── prompts/
│   ├── system_prompt_english.txt          # Production English Prompt for Retell/Bolna/Vapi
│   ├── system_prompt_hindi.txt            # Production Hindi Prompt (Gender-congruent)
│   ├── system_prompt_bilingual_unified.txt# Unified dynamic multi-language prompt
│   └── prompt_engineering_guide.md        # In-depth prompt design & engineering documentation
├── architecture/
│   ├── state_machine_and_logic.md        # State Machine Flowcharts & State Transition Tables
│   └── qualification_schema.json          # Complete JSON State & Slot Schema
├── test_suite/
│   ├── test_matrix.md                    # 20+ Test Scenarios Matrix
│   └── scenarios.json                     # Machine-readable test suite
├── simulator/
│   ├── agent_engine.py                   # Python State Machine & Slot Extractor Simulation Engine
│   ├── test_runner.py                    # Automated Test Runner with Assertion Validation
│   └── generate_transcripts.py           # Generates markdown dialogue transcripts
├── platform_configs/
│   ├── retell_agent_config.json           # Retell AI Agent JSON payload
│   ├── bolna_agent_config.json            # Bolna Pipeline & Webhook configuration
│   └── vapi_assistant_config.json         # Vapi Assistant JSON payload
└── transcripts/
    └── all_scenario_transcripts.md        # Full turn-by-turn transcripts for all 20+ scenarios
```

---

## 🚀 Quick Start & Automated Testing

### 1. Run Automated Test Suite (All 20+ Scenarios)
```powershell
python simulator/test_runner.py
```

### 2. Generate Full Turn-by-Turn Call Logs
```powershell
python simulator/generate_transcripts.py
```

---

## 🎙️ Voice Platform Deployment
To deploy to **Retell AI**, **Bolna**, or **Vapi**:
1. Copy the system prompt from `prompts/system_prompt_english.txt` or `prompts/system_prompt_hindi.txt`.
2. Import the respective platform config JSON from `platform_configs/`.
3. Set your telephony SIP/Twilio credentials and connect your live outbound campaign.
