# PROMPT ENGINEERING & DESIGN GUIDE: HOME CREDIT LAP VOICE AGENT

## 1. Executive Summary & Design Principles
Building an outbound conversational AI voice agent for financial services—specifically Loan Against Property (LAP) pre-qualification—requires balancing five core tenets:
1. **Low Acoustic & Linguistic Latency**: Spoken dialogue requires snappy responses (< 1.5s end-to-end latency). System instructions are structured with clear markdown hierarchy to optimize KV-cache reuse and reduce token-generation overhead.
2. **Deterministic State Progression with Natural Linguistic Flexibility**: The agent must strictly follow a 7-step qualification checklist, immediate disqualification branches, and transfer logic switches without sounding like an IVR menu.
3. **Multi-Slot & Out-of-Order Extraction**: Real human callers often answer unprompted questions or provide multiple data points in a single turn. The prompt enforces continuous slot extraction.
4. **Gender-Congruent Bilingual Generation**: In Hindi/Hinglish, verb inflections change based on speaker gender. The prompt conditions the LLM to strictly adhere to `agent_gender`.
5. **Zero Financial Hallucination Guardrails**: Financial regulations prohibit AI agents from fabricating interest rates, guaranteeing loan approvals, or misrepresenting product terms.

---

## 2. Dynamic Runtime Variables Schema
The system prompt operates dynamically over the following runtime payload:

```json
{
  "company_name": "Home Credit",
  "customer_name": "Mr. Rajesh Sharma",
  "agent_name": "Priya",
  "agent_gender": "female",
  "current_date": "2026-10-08",
  "current_day": "Thursday",
  "current_time": "04:15 PM",
  "additional_context_from_rag": "Home Credit LAP offers flexible repayment, competitive rates determined post verification, and zero hidden charges.",
  "language_to_speak": "English",
  "conversation_history": [
    {"role": "assistant", "content": "Hello, am I speaking with Mr. Rajesh Sharma?"},
    {"role": "user", "content": "Yes, Rajesh here."}
  ],
  "customer_utterance": "Yes, Rajesh here."
}
```

---

## 3. The 7 Mandatory Eligibility Slots Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               7 MANDATORY ELIGIBILITY SLOTS                             │
├───────────────────────────────┬───────────────────────────────┬─────────────────────────┤
│ Slot Name                     │ Valid / Qualifying Values     │ Disqualifying Values    │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────┤
│ 1. property_type              │ Residential, Commercial,      │ Agricultural            │
│                               │ Industrial                    │ (Immediate Exit)        │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────┤
│ 2. ownership_status           │ Sole Ownership,               │ None (Both are valid)   │
│                               │ Joint Ownership               │                         │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────┤
│ 3. original_documents_avail   │ True (Originals Available)    │ False / No Originals    │
│                               │                               │ (Immediate Exit)        │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────┤
│ 4. loan_amount                │ <= ₹75,00,000 (₹75 Lakhs)     │ > ₹75L with customer    │
│                               │                               │ refusal to cap at 75L   │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────┤
│ 5. occupation & income_mode   │ Salaried / Self-Employed;     │ Cash-only income        │
│                               │ Income received via Bank      │ (Immediate Exit)        │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────┤
│ 6. property_market_value      │ Any positive valuation        │ None (Informational)    │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────┤
│ 7. tenure                     │ 3 to 15 years inclusive       │ <3 or >15 years with    │
│                               │                               │ customer refusal        │
└───────────────────────────────┴───────────────────────────────┴─────────────────────────┘
```

---

## 4. Prompt Engineering Techniques Employed

### 1. Sequential & Opportunistic Slot Filling (Dynamic Checklisting)
Rather than forcing a rigid turn-by-turn script, the prompt instructs the model to maintain an internal state vector. When a caller says:
> *"I have a 3BHK flat in Noida worth 90 lakhs, working at Infosys with salary in ICICI, need 45 lakhs for 7 years."*

The LLM extracts:
- `property_type`: Residential
- `property_market_value`: ₹90,00,000
- `occupation`: Salaried
- `income_mode`: Bank
- `loan_amount`: ₹45,00,000
- `tenure`: 7 years

The LLM determines that only `ownership_status` and `original_documents_available` remain missing, and seamlessly asks for only those two without repeating the other 5 fields.

### 2. Guardrailed Boundary Negotiation
When callers request an out-of-boundary parameter (e.g. ₹1.2 Crore loan or 20-year tenure), the agent avoids immediate hard disqualification. Instead, it offers the maximum compliant boundary (₹75 Lakhs or 15 years) and branches based on caller consent.

### 3. Immediate Branch Disqualification (No Sunk-Cost Interrogation)
If a caller discloses an absolute disqualifier (e.g. Agricultural land, Cash salary, Lost documents), continuing the remaining questions wastes time and frustrates the caller. The prompt triggers immediate graceful exit.

### 4. The Intent-Switch Router (Transfer vs. Fresh LAP)
The agent continuously listens for balance transfer / existing loan / EMI reduction intent. When triggered, it flips the interaction from Fresh Loan Qualification to Specialized Transfer Referral.
