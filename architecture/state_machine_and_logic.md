# STATE MACHINE & BUSINESS LOGIC ARCHITECTURE

## 1. Overview
The Home Credit Loan Against Property (LAP) Voice Agent operates as an Event-Driven Finite State Machine (FSM) integrated with a dynamic slot-filling entity extractor.

```mermaid
stateDiagram-v2
    [*] --> IDENTITY_VERIFICATION
    
    IDENTITY_VERIFICATION --> WRONG_PERSON_EXIT: Identity Mismatch / Wrong Number
    IDENTITY_VERIFICATION --> CALLBACK_SCHEDULING: Customer Busy / Driving / In Meeting
    IDENTITY_VERIFICATION --> OFFER_PRESENTATION: Customer Identity Confirmed
    
    CALLBACK_SCHEDULING --> ENDED: Callback Time Recorded
    WRONG_PERSON_EXIT --> ENDED: Polite Exit (No info leaked)
    
    OFFER_PRESENTATION --> POLITE_EXIT: Customer Not Interested
    OFFER_PRESENTATION --> TRANSFER_HANDOFF: Has Existing Loan / Wants EMI Reduction
    OFFER_PRESENTATION --> QUALIFICATION_FLOW: Customer Agrees to Check Eligibility
    
    state QUALIFICATION_FLOW {
        [*] --> CHECK_SLOT_1_PROPERTY_TYPE
        CHECK_SLOT_1_PROPERTY_TYPE --> DISQUALIFIED: Agricultural Property
        CHECK_SLOT_1_PROPERTY_TYPE --> CHECK_SLOT_2_OWNERSHIP: Residential / Commercial / Industrial
        
        CHECK_SLOT_2_OWNERSHIP --> CHECK_SLOT_3_DOCUMENTS: Sole or Joint Ownership
        
        CHECK_SLOT_3_DOCUMENTS --> DISQUALIFIED: Original Documents Unavailable
        CHECK_SLOT_3_DOCUMENTS --> CHECK_SLOT_4_LOAN_AMOUNT: Original Documents Available
        
        CHECK_SLOT_4_LOAN_AMOUNT --> CHECK_SLOT_5_OCCUPATION_INCOME: <= 75 Lakhs
        CHECK_SLOT_4_LOAN_AMOUNT --> NEGOTIATE_LOAN_CAP: > 75 Lakhs
        NEGOTIATE_LOAN_CAP --> CHECK_SLOT_5_OCCUPATION_INCOME: Accepts 75L Cap
        NEGOTIATE_LOAN_CAP --> POLITE_EXIT: Refuses 75L Cap
        
        CHECK_SLOT_5_OCCUPATION_INCOME --> DISQUALIFIED: Cash-only Income
        CHECK_SLOT_5_OCCUPATION_INCOME --> CHECK_SLOT_6_MARKET_VALUE: Bank Income (Salaried/Self-Employed)
        
        CHECK_SLOT_6_MARKET_VALUE --> CHECK_SLOT_7_TENURE: Market Value Recorded
        
        CHECK_SLOT_7_TENURE --> QUALIFICATION_GATE_PASSED: 3 to 15 Years
        CHECK_SLOT_7_TENURE --> NEGOTIATE_TENURE: <3 or >15 Years
        NEGOTIATE_TENURE --> QUALIFICATION_GATE_PASSED: Accepts 3-15 Year Tenure
        NEGOTIATE_TENURE --> POLITE_EXIT: Refuses Valid Tenure
    }
    
    QUALIFICATION_FLOW --> TRANSFER_HANDOFF: Mentions Existing Loan / EMI Reduction at any turn
    QUALIFICATION_FLOW --> DISQUALIFIED: Immediate Disqualification Triggered
    
    DISQUALIFIED --> ENDED: Polite Disqualification Script
    POLITE_EXIT --> ENDED: Warm Closing Script
    TRANSFER_HANDOFF --> ENDED: Loan Transfer Specialist Script
    
    QUALIFICATION_GATE_PASSED --> SENIOR_EXPERT_HANDOFF
    SENIOR_EXPERT_HANDOFF --> ENDED: Senior Loan Expert Handoff Script
```

---

## 2. State Transition Table

| Current State | Trigger / Event | Next State | Spoken Action / System Side Effect |
|---|---|---|---|
| `INIT` | Call Connected | `IDENTITY_VERIFICATION` | "Hello, am I speaking with {{customer_name}}?" |
| `IDENTITY_VERIFICATION` | Customer confirms identity ("Yes", "Speaking") | `OFFER_PRESENTATION` | Present pre-approved LAP offer up to ₹75 Lakhs. |
| `IDENTITY_VERIFICATION` | Wrong person / customer unavailable | `WRONG_PERSON_EXIT` | Apologize, do not leak offer, end call. |
| `IDENTITY_VERIFICATION` | Customer busy / meeting / driving | `CALLBACK_SCHEDULING` | Ask for preferred callback time, store `callback_time`. |
| `CALLBACK_SCHEDULING` | Callback time provided | `ENDED` | Confirm callback time, thank customer, end call. |
| `OFFER_PRESENTATION` | Customer interested in checking eligibility | `QUALIFICATION_FLOW` | Initiate 7-slot qualification loop. |
| `OFFER_PRESENTATION` | Not interested | `POLITE_EXIT` | Thank customer for their relationship with Home Credit, end call. |
| `OFFER_PRESENTATION` / `QUALIFICATION_FLOW` | Customer mentions existing loan / EMI reduction | `TRANSFER_HANDOFF` | Explain loan transfer specialist will call shortly, end call. |
| `QUALIFICATION_FLOW` | `property_type == 'Agricultural'` | `DISQUALIFIED` | Explain offer criteria not met, stop immediately, end call. |
| `QUALIFICATION_FLOW` | `original_documents_available == 'No'` | `DISQUALIFIED` | Explain original docs required, stop immediately, end call. |
| `QUALIFICATION_FLOW` | `income_mode == 'Cash'` | `DISQUALIFIED` | Explain bank income required, stop immediately, end call. |
| `QUALIFICATION_FLOW` | Customer asks > ₹75L & agrees to ₹75L cap | `QUALIFICATION_FLOW` | Store `loan_amount = 7500000`, continue to next question. |
| `QUALIFICATION_FLOW` | Customer asks > ₹75L & refuses cap | `POLITE_EXIT` | Politely explain limit constraint and end call. |
| `QUALIFICATION_FLOW` | Customer asks invalid tenure & selects 3-15 yrs | `QUALIFICATION_FLOW` | Store valid tenure, continue to next question. |
| `QUALIFICATION_FLOW` | Customer refuses valid tenure range | `POLITE_EXIT` | Politely explain policy and end call. |
| `QUALIFICATION_FLOW` | All 7 slots filled & valid | `QUALIFICATION_GATE_PASSED` | Trigger final validation check. |
| `QUALIFICATION_GATE_PASSED` | Gate validation successful | `SENIOR_EXPERT_HANDOFF` | Congratulate on preliminary qualification, promise senior expert follow-up. |
| `SENIOR_EXPERT_HANDOFF` | Handoff message delivered | `ENDED` | End call cleanly. |

---

## 3. Slot-Filling Priority & Out-of-Order Extraction
At every turn $T_i$, the slot extraction engine executes:
$$\mathbf{S}_{new} = \mathbf{S}_{current} \cup \text{Extract}(\text{Utterance}_i)$$
$$\text{Next Question} = \min_{k \in \{1..7\}} \{k \mid \mathbf{S}[k] = \text{null}\}$$

If all 7 slots are non-null and pass validation, transition to `QUALIFICATION_GATE_PASSED`.
