# CALL LOGS & COMPLETE CONVERSATION TRANSCRIPTS

This document contains the exact turn-by-turn conversation transcripts, runtime state transitions, and slot updates across all 20 verified test scenarios for the **Home Credit Loan Against Property (LAP) AI Voice Agent**.

---

## [TC-01] Fully Eligible Golden Path (Residential + Salaried)
**Objective**: Standard sequential flow where customer qualifies on all 7 criteria and is handed off to senior loan expert.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, Rajesh here. Who is calling?
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Sure, I have a few minutes. Go ahead.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: It is a residential 3BHK apartment.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: I am the sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, I have all the original property deeds and registry papers ready.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: I am looking for around 50 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 7)]: I work as a software manager, salaried, and my salary is credited directly to my ICICI bank account.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 8)]: Current market value is approximately 1.2 crore.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 9)]: I would prefer a tenure of 10 years.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 5000000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "1.2 Crore",
    "tenure": 10
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 9
  }
}
```

---

## [TC-02] Agricultural Property Immediate Disqualification
**Objective**: Customer specifies property is agricultural land; agent must immediately disqualify and end call without asking further questions.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `DISQUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Okay, tell me about it.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: It is 4 acres of agricultural farmland in Punjab.
[AGENT (State: DISQUALIFIED)]: I understand, Mr. Rajesh Sharma. Based on the criteria for this specific pre-approved offer, agricultural property is not eligible. We truly appreciate your time and thank you for being a valued customer of Home Credit. Have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "DISQUALIFIED",
  "disposition": "DISQUALIFIED",
  "slots": {
    "property_type": "Agricultural",
    "ownership_status": null,
    "original_documents_available": null,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": "Agricultural property not eligible",
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "property_type",
    "asked_questions": [],
    "turn_count": 3
  }
}
```

---

## [TC-03] Cash-Only Income Immediate Disqualification
**Objective**: Customer receives income purely in cash; agent must immediately disqualify and end call.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `DISQUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, this is Rajesh.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Sure, check my eligibility.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Residential house.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole ownership.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, original papers are with me.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: I need 30 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 7)]: I run a small business and all my earnings are strictly in cash, no bank account.
[AGENT (State: DISQUALIFIED)]: I understand, Mr. Rajesh Sharma. Bank-credited income is mandatory for this specific offer, so we cannot proceed with cash-only income at this time. Thank you for your time with Home Credit. Have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "DISQUALIFIED",
  "disposition": "DISQUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 3000000,
    "occupation": "Self-Employed",
    "income_mode": "Cash",
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": "Cash-only income not eligible",
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "occupation_and_income",
    "asked_questions": [],
    "turn_count": 7
  }
}
```

---

## [TC-04] No Original Property Documents Immediate Disqualification
**Objective**: Customer does not have original property documents; agent must immediately disqualify and end call.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `DISQUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, Rajesh speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Sure, go ahead.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Commercial shop.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: No, original documents are missing, I only have Xerox photocopies.
[AGENT (State: DISQUALIFIED)]: I understand, Mr. Rajesh Sharma. Physical verification of original property documents is mandatory for this offer, so we are unable to proceed at this time. Thank you for your time with Home Credit. Have a great day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "DISQUALIFIED",
  "disposition": "DISQUALIFIED",
  "slots": {
    "property_type": "Commercial",
    "ownership_status": "Sole",
    "original_documents_available": false,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": "Original property documents unavailable",
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "original_documents_available",
    "asked_questions": [],
    "turn_count": 5
  }
}
```

---

## [TC-05A] Loan Amount Above ₹75L - Customer Accepts ₹75L Cap
**Objective**: Customer requests ₹80L; agent offers ₹75L max cap; customer agrees and qualification continues.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Yes, please.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Residential villa.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, original papers are available.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: I need 80 lakhs for my business.
[AGENT (State: QUALIFICATION_FLOW)]: I understand, Mr. Rajesh Sharma. This special pre-approved offer is available up to a maximum of ₹75 Lakhs. Would you like to proceed with the maximum eligible amount of ₹75 Lakhs?
[CUSTOMER (Turn 7)]: Yes, 75 lakhs works for me, let's proceed.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 8)]: Salaried with bank income.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 9)]: Market value is 2 crore.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 10)]: 12 years tenure.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 7500000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "2 Crore",
    "tenure": 12
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 10
  }
}
```

---

## [TC-05B] Loan Amount Above ₹75L - Customer Refuses Cap
**Objective**: Customer requests ₹1.5 Cr; agent offers ₹75L cap; customer declines and agent exits politely.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `EXITED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Sure.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Commercial building.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, have original registry.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: I strictly need 1.5 crore.
[AGENT (State: QUALIFICATION_FLOW)]: I understand, Mr. Rajesh Sharma. This special pre-approved offer is available up to a maximum of ₹75 Lakhs. Would you like to proceed with the maximum eligible amount of ₹75 Lakhs?
[CUSTOMER (Turn 7)]: No, 75 lakhs is too low for my project, I cannot proceed with that.
[AGENT (State: POLITE_EXIT)]: I understand, Mr. Rajesh Sharma. Since this specific offer is capped at ₹75 Lakhs, we are unable to proceed at this time. Thank you for your time with Home Credit!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "POLITE_EXIT",
  "disposition": "EXITED",
  "slots": {
    "property_type": "Commercial",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "loan_amount",
    "asked_questions": [],
    "turn_count": 7
  }
}
```

---

## [TC-06A] Invalid Tenure - Customer Accepts 3-15 Years Range
**Objective**: Customer asks for 20 years; agent explains 3-15 years limit; customer chooses 15 years and qualifies.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, Rajesh here.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Okay.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Residential.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, original papers ready.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: 40 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 7)]: Salaried in bank.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 8)]: 1 crore.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 9)]: I want 20 years.
[AGENT (State: QUALIFICATION_FLOW)]: The available repayment tenure for this offer is between 3 and 15 years. Would you like to proceed with a tenure within 3 to 15 years?
[CUSTOMER (Turn 10)]: Alright, let's keep it 15 years then.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 4000000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "1 Crore",
    "tenure": 15
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 10
  }
}
```

---

## [TC-06B] Invalid Tenure - Customer Refuses Range
**Objective**: Customer insists on 25 years; declines 3-15 years; agent politely exits.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `EXITED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, Rajesh here.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Okay.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Residential.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, original papers ready.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: 40 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 7)]: Salaried in bank.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 8)]: 1 crore.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 9)]: I need 25 years.
[AGENT (State: QUALIFICATION_FLOW)]: The available repayment tenure for this offer is between 3 and 15 years. Would you like to proceed with a tenure within 3 to 15 years?
[CUSTOMER (Turn 10)]: No, I cannot pay high EMI, I won't proceed with 15 years.
[AGENT (State: POLITE_EXIT)]: I understand, Mr. Rajesh Sharma. Since we can only offer tenures between 3 and 15 years for this scheme, we cannot proceed right now. Thank you for your time!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "POLITE_EXIT",
  "disposition": "EXITED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 4000000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "1 Crore",
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 10
  }
}
```

---

## [TC-07] Joint Ownership Verification
**Objective**: Customer has jointly owned property with spouse; verified as 100% eligible.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Go ahead.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Residential flat.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: It is jointly owned by me and my wife.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, we have all original papers.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: 35 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 7)]: Salaried, bank transfer.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 8)]: 85 lakhs market value.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 9)]: 7 years tenure.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Joint",
    "original_documents_available": true,
    "loan_amount": 3500000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "85 Lakhs",
    "tenure": 7
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 9
  }
}
```

---

## [TC-08] Self-Employed with Bank Income Verification
**Objective**: Customer is self-employed businessman with bank revenues; verified as eligible.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Sure, tell me.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Commercial shop in market.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, original deed available.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: 60 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 7)]: I am self-employed running a wholesale textile business, all turnover in current bank account.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 8)]: Market value is 1.5 crore.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 9)]: 5 years.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Commercial",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 6000000,
    "occupation": "Self-Employed",
    "income_mode": "Bank",
    "property_market_value": "1.5 Crore",
    "tenure": 5
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 9
  }
}
```

---

## [TC-09] Existing Loan on Property - Loan Transfer Switch
**Objective**: Customer mentions active loan on property; agent immediately switches to loan transfer specialist flow.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `TRANSFER_SPECIALIST`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Actually, I already have an existing loan running on this property with another bank.
[AGENT (State: TRANSFER_HANDOFF)]: I completely understand, Mr. Rajesh Sharma. Since you already have an existing loan and are looking for a loan transfer or EMI reduction, this is handled by our specialized Loan Transfer Team. A specialist will contact you shortly to review your existing loan details and help lower your EMIs. Thank you for choosing Home Credit!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "TRANSFER_HANDOFF",
  "disposition": "TRANSFER_SPECIALIST",
  "slots": {
    "property_type": null,
    "ownership_status": null,
    "original_documents_available": null,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": "Existing loan / EMI reduction transfer request",
    "pending_boundary_negotiation": null,
    "active_question_slot": "offer_presentation",
    "asked_questions": [],
    "turn_count": 2
  }
}
```

---

## [TC-10] EMI Reduction Request - Loan Transfer Switch
**Objective**: Customer asks to reduce existing monthly EMI; agent switches to loan transfer flow.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `TRANSFER_SPECIALIST`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, Rajesh here.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Can you help me reduce my current monthly EMI on my existing property loan?
[AGENT (State: TRANSFER_HANDOFF)]: I completely understand, Mr. Rajesh Sharma. Since you already have an existing loan and are looking for a loan transfer or EMI reduction, this is handled by our specialized Loan Transfer Team. A specialist will contact you shortly to review your existing loan details and help lower your EMIs. Thank you for choosing Home Credit!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "TRANSFER_HANDOFF",
  "disposition": "TRANSFER_SPECIALIST",
  "slots": {
    "property_type": null,
    "ownership_status": null,
    "original_documents_available": null,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": "Existing loan / EMI reduction transfer request",
    "pending_boundary_negotiation": null,
    "active_question_slot": "offer_presentation",
    "asked_questions": [],
    "turn_count": 2
  }
}
```

---

## [TC-11] Customer Busy / Meeting / Driving Flow
**Objective**: Customer is driving / busy; agent captures preferred callback time and exits without pitching.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `CALLBACK_REQUESTED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: I am driving in heavy traffic right now, please call me later today at 6:30 PM.
[AGENT (State: CALLBACK_SCHEDULING)]: I completely understand. We will schedule a callback for you at 6:30 pm. Thank you for your time with Home Credit, and have a great day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "CALLBACK_SCHEDULING",
  "disposition": "CALLBACK_REQUESTED",
  "slots": {
    "property_type": null,
    "ownership_status": null,
    "original_documents_available": null,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": "6:30 pm",
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "identity_verification",
    "asked_questions": [],
    "turn_count": 1
  }
}
```

---

## [TC-12] Information Provided Out of Order
**Objective**: Customer volunteers loan amount and bank income early; agent extracts both and skips asking them later.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: I am interested. By the way, I need 50 lakhs and my salary comes directly to my bank account.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: It is a residential house.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole ownership.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, original papers are ready.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 6)]: Market value is 1.1 crore.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 7)]: 8 years tenure.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 5000000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "1.1 Crore",
    "tenure": 8
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 7
  }
}
```

---

## [TC-13] Compound Multi-Slot Extraction in One Sentence
**Objective**: Customer delivers 4 data points in single utterance; agent extracts all 4 and asks only remaining 3 fields.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, Rajesh here.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Sure.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: I have a residential house in Pune, jointly owned with my wife, worth around 1.2 crore, and I need 60 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 4)]: Yes, we have all original property deeds ready.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 5)]: I am salaried in an IT firm with direct bank transfer.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 6)]: Tenure of 10 years.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Joint",
    "original_documents_available": true,
    "loan_amount": 6000000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "1.2 Crore",
    "tenure": 10
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 6
  }
}
```

---

## [TC-14] Identity Mismatch / Wrong Person
**Objective**: Wrong person answers phone; agent does not reveal sensitive pre-approved loan offer and exits.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `WRONG_PERSON`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: No, you have the wrong number. Rajesh does not live here.
[AGENT (State: WRONG_PERSON_EXIT)]: I apologize for the disturbance. We will reach out to Mr. Rajesh Sharma directly at a later time. Thank you and have a good day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "WRONG_PERSON_EXIT",
  "disposition": "WRONG_PERSON",
  "slots": {
    "property_type": null,
    "ownership_status": null,
    "original_documents_available": null,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "identity_verification",
    "asked_questions": [],
    "turn_count": 1
  }
}
```

---

## [TC-15] Customer Interrupts with Product FAQ Mid-Flow
**Objective**: Customer asks about prepayment charges mid-flow; agent clarifies safely, retains state, and continues qualification.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Okay.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: Residential flat.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Wait, is there any prepayment penalty if I close the loan early?
[AGENT (State: QUALIFICATION_FLOW)]: Home Credit offers transparent terms with zero hidden charges. Exact prepayment options will be confirmed by our Senior Loan Expert. Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 5)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 6)]: Yes, original papers available.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 7)]: 45 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 8)]: Salaried in bank.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 9)]: 90 lakhs value.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 10)]: 5 years.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 4500000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "90 Lakhs",
    "tenure": 5
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 10
  }
}
```

---

## [TC-16] Customer Inquires About Exact Interest Rate
**Objective**: Customer asks for exact interest rate; agent strictly adheres to compliance and defers to senior loan expert without hallucinating numbers.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, Rajesh speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: What is the exact interest rate on this loan?
[AGENT (State: QUALIFICATION_FLOW)]: The exact interest rate will be customized based on your property verification and provided directly by our Senior Loan Expert during the follow-up. We are offering a pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 3)]: Okay, that makes sense. It is a commercial showroom.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, original papers ready.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: 50 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 7)]: Self employed with bank account.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 8)]: 1.5 crore.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 9)]: 7 years.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Commercial",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 5000000,
    "occupation": "Self-Employed",
    "income_mode": "Bank",
    "property_market_value": "1.5 Crore",
    "tenure": 7
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 9
  }
}
```

---

## [TC-17] Industrial Property Golden Path Qualification
**Objective**: Customer owns an industrial factory; verified as 100% eligible category.  
**Language**: `English` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Hello, am I speaking with Mr. Rajesh Sharma?
[CUSTOMER (Turn 1)]: Yes, speaking.
[AGENT (State: OFFER_PRESENTATION)]: Hi Mr. Rajesh Sharma, this is Priya calling from Home Credit. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?
[CUSTOMER (Turn 2)]: Sure, check my eligibility.
[AGENT (State: QUALIFICATION_FLOW)]: To start, could you tell me if your property is residential, commercial, or industrial?
[CUSTOMER (Turn 3)]: It is an industrial factory warehouse in Faridabad.
[AGENT (State: QUALIFICATION_FLOW)]: Got it. And are you the sole owner of the property, or is it jointly owned?
[CUSTOMER (Turn 4)]: Sole owner.
[AGENT (State: QUALIFICATION_FLOW)]: Do you have the original property documents ready and available for verification?
[CUSTOMER (Turn 5)]: Yes, original deeds are available.
[AGENT (State: QUALIFICATION_FLOW)]: How much loan amount are you looking to borrow?
[CUSTOMER (Turn 6)]: 70 lakhs.
[AGENT (State: QUALIFICATION_FLOW)]: Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?
[CUSTOMER (Turn 7)]: Self-employed, all turnover in current bank account.
[AGENT (State: QUALIFICATION_FLOW)]: What would be the approximate current market value of your property?
[CUSTOMER (Turn 8)]: 2 crore market value.
[AGENT (State: QUALIFICATION_FLOW)]: Over how many years would you like to repay the loan?
[CUSTOMER (Turn 9)]: 10 years.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Thank you so much for providing all the details, Mr. Rajesh Sharma. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from Home Credit will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing Home Credit, and have a wonderful day!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Industrial",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 7000000,
    "occupation": "Self-Employed",
    "income_mode": "Bank",
    "property_market_value": "2 Crore",
    "tenure": 10
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 9
  }
}
```

---

## [TC-18] Hindi Golden Path Qualification (Female Grammar)
**Objective**: Full conversation in Hindi with female agent grammar validation.  
**Language**: `Hindi` | **Agent Gender**: `female` | **Expected Disposition**: `QUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Namaste! Kya meri baat Rajesh ji se ho rahi hai?
[CUSTOMER (Turn 1)]: Haan Rajesh bol raha hoon.
[AGENT (State: OFFER_PRESENTATION)]: Namaste Rajesh ji! Main Home Credit se Priya baat kar rahi hoon. Aapki loyalty ke liye hum aapko ₹75 Lakhs tak ka vishesh pre-approved Loan Against Property offer de rahe hain. Kya main eligibility check karne ke liye aapse 2 minute baat kar sakti hoon?
[CUSTOMER (Turn 2)]: Haan theek hai, bataiye.
[AGENT (State: QUALIFICATION_FLOW)]: Kya aap bata sakte hain ki aapki property Residential (ghar/flat), Commercial (dukaan/office), ya Industrial hai?
[CUSTOMER (Turn 3)]: Mera residential flat hai.
[AGENT (State: QUALIFICATION_FLOW)]: Kya aap is property ke akele malik hain ya yeh joint property hai?
[CUSTOMER (Turn 4)]: Mera akele ka hai.
[AGENT (State: QUALIFICATION_FLOW)]: Kya verification ke liye property ke original documents aapke paas uplabdh hain?
[CUSTOMER (Turn 5)]: Haan original registry mere paas hai.
[AGENT (State: QUALIFICATION_FLOW)]: Aap kitna loan amount lena chahte hain?
[CUSTOMER (Turn 6)]: 50 lakh chahiye.
[AGENT (State: QUALIFICATION_FLOW)]: Kya aap Salaried hain ya Self-Employed, aur aapki income bank account mein aati hai ya cash mein?
[CUSTOMER (Turn 7)]: Salaried hoon aur account mein salary aati hai.
[AGENT (State: QUALIFICATION_FLOW)]: Aapki property ki anumanit market value kitni hogi?
[CUSTOMER (Turn 8)]: 1 crore market value hai.
[AGENT (State: QUALIFICATION_FLOW)]: Aap yeh loan kitne saalon mein repay karna chahenge?
[CUSTOMER (Turn 9)]: 10 saal tenure chahiye.
[AGENT (State: SENIOR_EXPERT_HANDOFF)]: Saari jaankari share karne ke liye bahut-bahut dhanyavaad, Rajesh ji. Aapne hamare Loan Against Property offer ki preliminary eligibility qualification safaltapoorvak poori kar li hai! Home Credit ke senior loan expert aapko jaldi hi call karenge taaki exact interest rates discuss karke aapka application finalize kiya ja sake. Aapka din shubh ho!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "SENIOR_EXPERT_HANDOFF",
  "disposition": "QUALIFIED",
  "slots": {
    "property_type": "Residential",
    "ownership_status": "Sole",
    "original_documents_available": true,
    "loan_amount": 5000000,
    "occupation": "Salaried",
    "income_mode": "Bank",
    "property_market_value": "1 Crore",
    "tenure": 10
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "tenure",
    "asked_questions": [],
    "turn_count": 9
  }
}
```

---

## [TC-19] Hindi Agricultural Disqualification (Kheti ki Zameen)
**Objective**: Customer specifies kheti ki zameen in Hindi; agent immediately disqualifies.  
**Language**: `Hindi` | **Agent Gender**: `female` | **Expected Disposition**: `DISQUALIFIED`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Namaste! Kya meri baat Rajesh ji se ho rahi hai?
[CUSTOMER (Turn 1)]: Haan Rajesh bol raha hoon.
[AGENT (State: OFFER_PRESENTATION)]: Namaste Rajesh ji! Main Home Credit se Priya baat kar rahi hoon. Aapki loyalty ke liye hum aapko ₹75 Lakhs tak ka vishesh pre-approved Loan Against Property offer de rahe hain. Kya main eligibility check karne ke liye aapse 2 minute baat kar sakti hoon?
[CUSTOMER (Turn 2)]: Haan bataiye.
[AGENT (State: QUALIFICATION_FLOW)]: Kya aap bata sakte hain ki aapki property Residential (ghar/flat), Commercial (dukaan/office), ya Industrial hai?
[CUSTOMER (Turn 3)]: Yeh meri kheti ki zameen hai gaon mein.
[AGENT (State: DISQUALIFIED)]: Main samajh sakti hoon, Rajesh ji. Is vishesh pre-approved offer ke criteria ke anusaar, agricultural property par loan uplabdh nahi hai. Home Credit ke saath judne ke liye aapka bahut-bahut dhanyavaad. Aapka din shubh ho!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "DISQUALIFIED",
  "disposition": "DISQUALIFIED",
  "slots": {
    "property_type": "Agricultural",
    "ownership_status": null,
    "original_documents_available": null,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": "Agricultural property not eligible",
    "transfer_reason": null,
    "pending_boundary_negotiation": null,
    "active_question_slot": "property_type",
    "asked_questions": [],
    "turn_count": 3
  }
}
```

---

## [TC-20] Hindi Loan Transfer Switch (Purana Loan / EMI Kam)
**Objective**: Customer mentions purana loan in Hindi; agent immediately routes to Loan Transfer Specialist.  
**Language**: `Hindi` | **Agent Gender**: `female` | **Expected Disposition**: `TRANSFER_SPECIALIST`

### Dialogue Flow:
```text
[AGENT (State: IDENTITY_VERIFICATION)]: Namaste! Kya meri baat Rajesh ji se ho rahi hai?
[CUSTOMER (Turn 1)]: Haan Rajesh bol raha hoon.
[AGENT (State: OFFER_PRESENTATION)]: Namaste Rajesh ji! Main Home Credit se Priya baat kar rahi hoon. Aapki loyalty ke liye hum aapko ₹75 Lakhs tak ka vishesh pre-approved Loan Against Property offer de rahe hain. Kya main eligibility check karne ke liye aapse 2 minute baat kar sakti hoon?
[CUSTOMER (Turn 2)]: Mera pehle se loan chal raha hai, mujhe EMI kam karni hai.
[AGENT (State: TRANSFER_HANDOFF)]: Main samajh sakti hoon, Rajesh ji. Kyunki aapka pehle se loan chal raha hai aur aap EMI kam karne ke liye loan transfer chahte hain, iske liye hamari specialized Loan Transfer Team aapki madad karegi. Hamare specialist aapko jaldi hi call karenge. Home Credit par vishwas rakhne ke liye dhanyavaad!
```

**Final Captured Slots & State**:
```json
{
  "final_state": "TRANSFER_HANDOFF",
  "disposition": "TRANSFER_SPECIALIST",
  "slots": {
    "property_type": null,
    "ownership_status": null,
    "original_documents_available": null,
    "loan_amount": null,
    "occupation": null,
    "income_mode": null,
    "property_market_value": null,
    "tenure": null
  },
  "metadata": {
    "callback_time": null,
    "disqualification_reason": null,
    "transfer_reason": "Existing loan / EMI reduction transfer request",
    "pending_boundary_negotiation": null,
    "active_question_slot": "offer_presentation",
    "asked_questions": [],
    "turn_count": 2
  }
}
```

---
