"""
Home Credit Loan Against Property (LAP) AI Voice Agent Simulator Engine
Enterprise Grade Context-Aware Natural Language Understanding & State Machine Engine.
Supports English, Hindi, Hinglish, Out-of-Order Multi-Slot Extraction, Short Contextual Affirmations,
Adversarial Conversational Inputs, Hindi Number Parsing, and Strict State Gates.
"""

import re
import sys
from typing import Dict, Any, Optional, Tuple, List

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Hindi / English Number & Magnitude Word Mappings
HINDI_NUMBER_MAP = {
    "ek": 1, "one": 1,
    "do": 2, "two": 2,
    "teen": 3, "three": 3,
    "chaar": 4, "char": 4, "four": 4,
    "paanch": 5, "panch": 5, "five": 5,
    "chhe": 6, "che": 6, "chhah": 6, "six": 6,
    "saat": 7, "seven": 7,
    "aath": 8, "eight": 8,
    "nau": 9, "nine": 9,
    "dus": 10, "das": 10, "ten": 10,
    "gyarah": 11, "eleven": 11,
    "baarah": 12, "barah": 12, "twelve": 12,
    "terah": 13, "thirteen": 13,
    "chaudah": 14, "fourteen": 14,
    "pandrah": 15, "fifteen": 15,
    "solah": 16, "sixteen": 16,
    "satrah": 17, "seventeen": 17,
    "athaarah": 18, "atharah": 18, "eighteen": 18,
    "unnees": 19, "nineteen": 19,
    "bees": 20, "twenty": 20,
    "pachees": 25, "pachis": 25, "twenty five": 25, "twenty-five": 25,
    "tees": 30, "thirty": 30,
    "paintees": 35, "thirty five": 35, "thirty-five": 35,
    "chaalees": 40, "chalis": 40, "forty": 40,
    "paintalees": 45, "forty five": 45, "forty-five": 45,
    "pachaas": 50, "pachas": 50, "fifty": 50,
    "saath": 60, "sath": 60, "sixty": 60,
    "sattar": 70, "seventy": 70,
    "pachattar": 75, "pachhattar": 75, "seventy five": 75, "seventy-five": 75,
    "assi": 80, "eighty": 80,
    "nabbey": 90, "nabbe": 90, "ninety": 90,
    "sau": 100, "hundred": 100,
    "sawa": 1.25,
    "dedh": 1.5, "derh": 1.5, "dehd": 1.5,
    "dhaai": 2.5, "dhai": 2.5
}


class VoiceAgentState:
    def __init__(self, context: Optional[Dict[str, Any]] = None):
        self.context = context or {
            "company_name": "Home Credit",
            "customer_name": "Mr. Rajesh Sharma",
            "agent_name": "Priya",
            "agent_gender": "female",
            "current_date": "2026-10-08",
            "current_day": "Thursday",
            "current_time": "04:15 PM",
            "language_to_speak": "English",
            "additional_context_from_rag": "Home Credit LAP offers up to 75 Lakhs, 3-15 years tenure, competitive interest rates determined post verification by senior loan experts."
        }
        
        self.call_state = "INIT"
        self.previous_state = None
        
        # 7 Mandatory Qualification Slots
        self.slots = {
            "property_type": None,                 # Residential, Commercial, Industrial, Agricultural
            "ownership_status": None,              # Sole, Joint
            "original_documents_available": None,  # True, False
            "loan_amount": None,                   # Number in INR (<= 75,00,000)
            "occupation": None,                    # Salaried, Self-Employed
            "income_mode": None,                   # Bank, Cash
            "property_market_value": None,         # String / Number
            "tenure": None                         # Integer (3 to 15)
        }
        
        # Metadata
        self.metadata = {
            "callback_time": None,
            "disqualification_reason": None,
            "transfer_reason": None,
            "pending_boundary_negotiation": None,  # 'loan_amount_cap' or 'tenure_range'
            "active_question_slot": None,          # Currently asked slot to enable contextual single-word resolution
            "asked_questions": set(),
            "turn_count": 0
        }
        
        self.dialogue_history: List[Dict[str, str]] = []

    def is_hindi(self) -> bool:
        return self.context.get("language_to_speak", "English").lower() == "hindi"

    def get_female_marker(self) -> Tuple[str, str, str]:
        if self.context.get("agent_gender", "female").lower() == "female":
            return ("rahi hoon", "sakti hoon", "chahti hoon")
        return ("raha hoon", "sakta hoon", "chahta hoon")


class HomeCreditVoiceAgent:
    def __init__(self, context: Optional[Dict[str, Any]] = None):
        self.state = VoiceAgentState(context)

    def get_initial_greeting(self) -> str:
        self.state.call_state = "IDENTITY_VERIFICATION"
        self.state.metadata["active_question_slot"] = "identity_verification"
        cust_name = self.state.context.get("customer_name", "Customer")
        if self.state.is_hindi():
            return f"Namaste! Kya meri baat {cust_name} ji se ho rahi hai?"
        return f"Hello, am I speaking with {cust_name}?"

    def process_turn(self, customer_utterance: str) -> Dict[str, Any]:
        self.state.metadata["turn_count"] += 1
        self.state.dialogue_history.append({"role": "user", "content": customer_utterance})
        
        speech_response, next_state = self._evaluate_turn(customer_utterance)
        
        self.state.previous_state = self.state.call_state
        self.state.call_state = next_state
        self.state.dialogue_history.append({"role": "assistant", "content": speech_response})
        
        return {
            "agent_response": speech_response,
            "call_state": self.state.call_state,
            "slots": dict(self.state.slots),
            "metadata": dict(self.state.metadata),
            "is_terminal": self.state.call_state in [
                "SENIOR_EXPERT_HANDOFF", "DISQUALIFIED", "TRANSFER_HANDOFF",
                "CALLBACK_SCHEDULING", "WRONG_PERSON_EXIT", "POLITE_EXIT", "ENDED"
            ]
        }

    def _evaluate_turn(self, utterance: str) -> Tuple[str, str]:
        u = utterance.strip().lower()
        c = self.state.context
        comp = c.get("company_name", "Home Credit")
        cust = c.get("customer_name", "Customer")
        agent_name = c.get("agent_name", "Priya")
        is_hi = self.state.is_hindi()
        f_rahi, f_sakti, f_chahti = self.state.get_female_marker()

        # -------------------------------------------------------------
        # GLOBAL TRIGGER 1: Wrong Person / Identity Mismatch
        # -------------------------------------------------------------
        if self.state.call_state == "IDENTITY_VERIFICATION":
            if any(k in u for k in ["wrong number", "not rajesh", "not here", "galat number", "koi aur", "does not live here", "wrong person", "galat person"]):
                if is_hi:
                    return (f"Kshama chahti hoon. Hum {cust} ji se baad mein sampark karenge. Dhanyavaad!", "WRONG_PERSON_EXIT")
                return (f"I apologize for the disturbance. We will reach out to {cust} directly at a later time. Thank you and have a good day!", "WRONG_PERSON_EXIT")

        # -------------------------------------------------------------
        # GLOBAL TRIGGER 2: Busy / Meeting / Driving / Callback Request
        # -------------------------------------------------------------
        if any(k in u for k in ["driving", "in a meeting", "in meeting", "busy right now", "call me later", "call later", "no time right now", "travelling", "vyast hoon", "baad mein phone", "baad mein call"]):
            time_match = re.search(r'(\d{1,2}(?::\d{2})?\s*(?:am|pm|baje))', u, re.IGNORECASE)
            cb_time = time_match.group(1) if time_match else ("evening" if "evening" in u else "later")
            self.state.metadata["callback_time"] = cb_time
            if is_hi:
                return (f"Ji bilkul, main samajh {f_sakti}. Hum aapko {cb_time} par dubara call karenge. {comp} se judne ke liye dhanyavaad, shubh din!", "CALLBACK_SCHEDULING")
            return (f"I completely understand. We will schedule a callback for you at {cb_time}. Thank you for your time with {comp}, and have a great day!", "CALLBACK_SCHEDULING")

        # -------------------------------------------------------------
        # GLOBAL TRIGGER 3: Existing Loan / EMI Reduction / Transfer Switch
        # -------------------------------------------------------------
        if any(k in u for k in [
            "already have a loan", "existing loan", "running loan", "balance transfer",
            "transfer my loan", "reduce my emi", "reduce emi", "reduce my current", "lower my emi", "lower current emi",
            "purana loan", "emi kam karni", "pehle se loan", "loan chal raha", "purana chal raha"
        ]):
            self.state.metadata["transfer_reason"] = "Existing loan / EMI reduction transfer request"
            if is_hi:
                return (
                    f"Main samajh {f_sakti}, {cust} ji. Kyunki aapka pehle se loan chal raha hai aur aap EMI kam karne ke liye loan transfer chahte hain, iske liye hamari specialized Loan Transfer Team aapki madad karegi. Hamare specialist aapko jaldi hi call karenge. {comp} par vishwas rakhne ke liye dhanyavaad!",
                    "TRANSFER_HANDOFF"
                )
            return (
                f"I completely understand, {cust}. Since you already have an existing loan and are looking for a loan transfer or EMI reduction, this is handled by our specialized Loan Transfer Team. A specialist will contact you shortly to review your existing loan details and help lower your EMIs. Thank you for choosing {comp}!",
                "TRANSFER_HANDOFF"
            )

        # -------------------------------------------------------------
        # GLOBAL TRIGGER 4: Interest Rate / EMI Inquiries
        # -------------------------------------------------------------
        if any(k in u for k in ["what is the exact interest rate", "interest rate", "rate of interest", "kitna byaj", "roi", "byaaj kitna", "exact rate", "kitna rate"]):
            if is_hi:
                prefix = f"Interest rate aapke profile aur property documents verification ke baad hamare Senior Loan Expert dwara finalize kiya jayega. "
            else:
                prefix = f"The exact interest rate will be customized based on your property verification and provided directly by our Senior Loan Expert during the follow-up. "
            
            if self.state.call_state in ["IDENTITY_VERIFICATION", "OFFER_PRESENTATION"]:
                self.state.call_state = "QUALIFICATION_FLOW"
                if is_hi:
                    return (prefix + f"Hum aapko ₹75 Lakhs tak ka pre-approved Loan Against Property offer de rahe hain. Kya hum quick eligibility check karein?", "QUALIFICATION_FLOW")
                return (prefix + f"We are offering a pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?", "QUALIFICATION_FLOW")
            else:
                return (prefix + self._prompt_next_missing_slot(), "QUALIFICATION_FLOW")

        # -------------------------------------------------------------
        # GLOBAL TRIGGER 5: Prepayment Penalty / FAQ Interruption
        # -------------------------------------------------------------
        if any(k in u for k in ["prepayment", "foreclosure", "early close", "penalty", "pre-payment"]):
            if is_hi:
                prefix = f"{comp} mein terms bilkul transparent hain aur koi hidden charges nahi hain. Exact prepayment details senior expert follow-up call mein confirm karenge. "
            else:
                prefix = f"{comp} offers transparent terms with zero hidden charges. Exact prepayment options will be confirmed by our Senior Loan Expert. "
            return (prefix + self._prompt_next_missing_slot(), "QUALIFICATION_FLOW")

        # -------------------------------------------------------------
        # STATE: IDENTITY VERIFICATION -> OFFER PRESENTATION
        # -------------------------------------------------------------
        if self.state.call_state == "IDENTITY_VERIFICATION":
            if any(k in u for k in ["yes", "speaking", "rajesh", "haan", "bol raha hoon", "bol rahi hoon", "this is him", "this is her", "this is rajesh", "ji haan", "haanji", "ha"]):
                self.state.metadata["active_question_slot"] = "offer_presentation"
                if is_hi:
                    return (
                        f"Namaste {cust} ji! Main {comp} se {agent_name} baat kar {f_rahi}. Aapki loyalty ke liye hum aapko ₹75 Lakhs tak ka vishesh pre-approved Loan Against Property offer de rahe hain. Kya main eligibility check karne ke liye aapse 2 minute baat kar {f_sakti}?",
                        "OFFER_PRESENTATION"
                    )
                return (
                    f"Hi {cust}, this is {agent_name} calling from {comp}. We are reaching out to reward your loyalty with a special pre-approved Loan Against Property offer of up to ₹75 Lakhs. May I ask a few quick questions to check your eligibility?",
                    "OFFER_PRESENTATION"
                )

        # -------------------------------------------------------------
        # STATE: OFFER PRESENTATION
        # -------------------------------------------------------------
        if self.state.call_state == "OFFER_PRESENTATION":
            if any(k in u for k in ["not interested", "nahi chahiye", "don't want", "no thanks", "no, i don't", "nahi lena", "zarurat nahi"]):
                if is_hi:
                    return (f"Koi baat nahi {cust} ji. {comp} ke saath judne ke liye dhanyavaad. Shubh din!", "POLITE_EXIT")
                return (f"No problem at all, {cust}. Thank you for your time and for being a valued customer of {comp}. Have a great day!", "POLITE_EXIT")
            
            # Customer accepts or volunteers info -> transition to QUALIFICATION_FLOW
            self.state.call_state = "QUALIFICATION_FLOW"

        # -------------------------------------------------------------
        # STATE: QUALIFICATION FLOW (Continuous Slot Extraction & Negotiation)
        # -------------------------------------------------------------
        if self.state.call_state in ["QUALIFICATION_FLOW", "OFFER_PRESENTATION"]:
            # Check Pending Boundary Negotiations FIRST
            if self.state.metadata.get("pending_boundary_negotiation") == "loan_amount_cap":
                # Check refusal first
                if any(k in u for k in ["no", "cannot", "too low", "too less", "nahi", "kam hai", "won't proceed", "cannot proceed", "mana", "too low for my project"]):
                    self.state.metadata["pending_boundary_negotiation"] = None
                    self.state.slots["loan_amount"] = None
                    if is_hi:
                        return (f"Main samajh {f_sakti}, {cust} ji. Kyunki yeh offer maximum ₹75 Lakhs tak hi uplabdh hai, hum abhi aage nahi badh payenge. {comp} se judne ke liye dhanyavaad!", "POLITE_EXIT")
                    return (f"I understand, {cust}. Since this specific offer is capped at ₹75 Lakhs, we are unable to proceed at this time. Thank you for your time with {comp}!", "POLITE_EXIT")
                elif any(k in u for k in ["yes", "okay", "fine", "sure", "proceed", "haan", "chalega", "theek hai", "works for me", "chalo theek", "haan chalega"]):
                    self.state.slots["loan_amount"] = 7500000
                    self.state.metadata["pending_boundary_negotiation"] = None

            elif self.state.metadata.get("pending_boundary_negotiation") == "tenure_range":
                if any(k in u for k in ["no", "cannot", "won't", "nahi", "cannot pay", "won't proceed", "mana", "no, i cannot", "i won't proceed"]):
                    self.state.metadata["pending_boundary_negotiation"] = None
                    self.state.slots["tenure"] = None
                    if is_hi:
                        return (f"Main samajh {f_sakti}, {cust} ji. Policy ke anusaar hum 3-15 saal ke alawa tenure nahi de sakte. {comp} ke saath judne ke liye dhanyavaad!", "POLITE_EXIT")
                    return (f"I understand, {cust}. Since we can only offer tenures between 3 and 15 years for this scheme, we cannot proceed right now. Thank you for your time!", "POLITE_EXIT")
                else:
                    parsed_tenure = self._parse_tenure(u)
                    if parsed_tenure and 3 <= parsed_tenure <= 15:
                        self.state.slots["tenure"] = parsed_tenure
                        self.state.metadata["pending_boundary_negotiation"] = None

            # ---------------------------------------------------------
            # 1. EXTRACT ALL 7 SLOTS (Global + Context-Aware)
            # ---------------------------------------------------------
            self._extract_slots_comprehensive(u)

            # ---------------------------------------------------------
            # 2. CHECK IMMEDIATE DISQUALIFICATION RULES
            # ---------------------------------------------------------
            # Disqualification Rule 1: Agricultural Property
            if self.state.slots["property_type"] == "Agricultural":
                self.state.metadata["disqualification_reason"] = "Agricultural property not eligible"
                if is_hi:
                    return (
                        f"Main samajh {f_sakti}, {cust} ji. Is vishesh pre-approved offer ke criteria ke anusaar, agricultural property par loan uplabdh nahi hai. {comp} ke saath judne ke liye aapka bahut-bahut dhanyavaad. Aapka din shubh ho!",
                        "DISQUALIFIED"
                    )
                return (
                    f"I understand, {cust}. Based on the criteria for this specific pre-approved offer, agricultural property is not eligible. We truly appreciate your time and thank you for being a valued customer of {comp}. Have a wonderful day!",
                    "DISQUALIFIED"
                )

            # Disqualification Rule 2: Original Documents Unavailable
            if self.state.slots["original_documents_available"] is False:
                self.state.metadata["disqualification_reason"] = "Original property documents unavailable"
                if is_hi:
                    return (
                        f"Main samajh {f_sakti}, {cust} ji. Physical verification ke liye original property documents hona anivarya hai, isliye hum abhi aage nahi badh payenge. {comp} se judne ke liye dhanyavaad. Shubh din!",
                        "DISQUALIFIED"
                    )
                return (
                    f"I understand, {cust}. Physical verification of original property documents is mandatory for this offer, so we are unable to proceed at this time. Thank you for your time with {comp}. Have a great day!",
                    "DISQUALIFIED"
                )

            # Disqualification Rule 3: Cash Income
            if self.state.slots["income_mode"] == "Cash":
                self.state.metadata["disqualification_reason"] = "Cash-only income not eligible"
                if is_hi:
                    return (
                        f"Main samajh {f_sakti}, {cust} ji. Is offer ke liye income bank account mein aana anivarya hai. Cash income ke saath hum aage nahi badh payenge. {comp} ke saath judne ke liye dhanyavaad!",
                        "DISQUALIFIED"
                    )
                return (
                    f"I understand, {cust}. Bank-credited income is mandatory for this specific offer, so we cannot proceed with cash-only income at this time. Thank you for your time with {comp}. Have a wonderful day!",
                    "DISQUALIFIED"
                )

            # ---------------------------------------------------------
            # 3. CHECK BOUNDARY NEGOTIATION TRIGGERS
            # ---------------------------------------------------------
            # Boundary 1: Loan Amount > 75 Lakhs
            if self.state.slots["loan_amount"] is not None and self.state.slots["loan_amount"] > 7500000:
                self.state.metadata["pending_boundary_negotiation"] = "loan_amount_cap"
                self.state.slots["loan_amount"] = None  # Hold until accepted
                if is_hi:
                    return (
                        f"Main samajh {f_sakti}, {cust} ji. Yeh vishesh pre-approved offer maximum ₹75 Lakhs tak ke liye uplabdh hai. Kya aap ₹75 Lakhs ke loan ke saath aage badhna chahenge?",
                        "QUALIFICATION_FLOW"
                    )
                return (
                    f"I understand, {cust}. This special pre-approved offer is available up to a maximum of ₹75 Lakhs. Would you like to proceed with the maximum eligible amount of ₹75 Lakhs?",
                    "QUALIFICATION_FLOW"
                )

            # Boundary 2: Tenure outside 3-15 years
            if self.state.slots["tenure"] is not None and (self.state.slots["tenure"] < 3 or self.state.slots["tenure"] > 15):
                self.state.metadata["pending_boundary_negotiation"] = "tenure_range"
                self.state.slots["tenure"] = None  # Hold until valid selection
                if is_hi:
                    return (
                        f"Is offer ke liye repayment tenure 3 saal se 15 saal ke beech uplabdh hai. Kya aap 3 se 15 saal ke beech koi tenure chunna chahenge?",
                        "QUALIFICATION_FLOW"
                    )
                return (
                    f"The available repayment tenure for this offer is between 3 and 15 years. Would you like to proceed with a tenure within 3 to 15 years?",
                    "QUALIFICATION_FLOW"
                )

            # ---------------------------------------------------------
            # 4. FINAL QUALIFICATION GATE CHECK
            # ---------------------------------------------------------
            if self._all_slots_valid():
                if is_hi:
                    return (
                        f"Saari jaankari share karne ke liye bahut-bahut dhanyavaad, {cust} ji. Aapne hamare Loan Against Property offer ki preliminary eligibility qualification safaltapoorvak poori kar li hai! {comp} ke senior loan expert aapko jaldi hi call karenge taaki exact interest rates discuss karke aapka application finalize kiya ja sake. Aapka din shubh ho!",
                        "SENIOR_EXPERT_HANDOFF"
                    )
                return (
                    f"Thank you so much for providing all the details, {cust}. You have successfully completed the preliminary eligibility qualification for our Loan Against Property offer! A senior loan expert from {comp} will call you shortly to discuss the exact interest rates and finalize your application. Thank you for choosing {comp}, and have a wonderful day!",
                    "SENIOR_EXPERT_HANDOFF"
                )

            # ---------------------------------------------------------
            # 5. ASK NEXT UNCOLLECTED SLOT QUESTION (Strict Non-Repetition)
            # ---------------------------------------------------------
            next_prompt = self._prompt_next_missing_slot()
            return (next_prompt, "QUALIFICATION_FLOW")

        return ("I'm sorry, could you please clarify?", self.state.call_state)

    def _extract_slots_comprehensive(self, u: str) -> None:
        """
        Two-stage slot extractor:
        Stage 1: Global multi-slot semantic & lexical scanning
        Stage 2: Active question context-aware resolution for short single-word answers
        """
        if self.state.metadata.get("pending_boundary_negotiation") and any(k in u for k in ["no,", "cannot", "too low", "won't", "too less", "nahi", "cannot pay"]):
            return

        active_slot = self.state.metadata.get("active_question_slot")

        # =============================================================
        # STAGE 1: GLOBAL NLU EXTRACTION
        # =============================================================

        # --- 1. Property Type ---
        if any(k in u for k in ["agricultural", "agriculture", "kheti", "farmland", "farm land", "kheti ki zameen", "agricultural land", "kheti ki property"]):
            self.state.slots["property_type"] = "Agricultural"
        elif any(k in u for k in ["industrial", "factory", "warehouse", "godown", "shed", "industrial property", "factory hai"]):
            self.state.slots["property_type"] = "Industrial"
        elif any(k in u for k in ["commercial", "showroom", "office", "commercial property", "commercial building"]) or (re.search(r'\bshop\b', u) and "small shop" not in u and "shop owner" not in u):
            self.state.slots["property_type"] = "Commercial"
        elif re.search(r'\b(residential|apartment|villa|makaan|makan|ghar|flat|3bhk|2bhk|1bhk|house|home|residential property)\b', u):
            if "warehouse" not in u:
                self.state.slots["property_type"] = "Residential"

        # --- 2. Ownership Status ---
        joint_patterns = [
            "joint", "jointly", "joint property", "jointly owned", "wife ke saath", "patni ke saath",
            "husband ke saath", "pati ke saath", "family ke saath", "partner ke saath", "bhai ke saath",
            "brother ke saath", "father ke saath", "mother ke saath", "hum dono ke naam", "dono ke naam",
            "joint with wife", "joint with husband", "co-owned", "joint ownership"
        ]
        sole_patterns = [
            "sole", "sole owner", "sole ownership", "single owner", "only me", "mera akele", "mera akela",
            "akela", "akele", "akeli", "sirf mera", "sirf meri", "meri hai", "mera hai", "mere naam par",
            "mere naam pe", "main akela", "main akele", "myself only", "own property", "single",
            "meri property hai", "main akela malik", "mera akele ka"
        ]

        if any(k in u for k in joint_patterns):
            self.state.slots["ownership_status"] = "Joint"
        elif any(re.search(r'\b' + re.escape(p) + r'\b', u) for p in sole_patterns):
            self.state.slots["ownership_status"] = "Sole"

        # --- 3. Original Documents Availability ---
        neg_doc_patterns = [
            "no original", "lost", "photocopy", "xerox", "missing", "nahi hai", "gum ho gaye",
            "xerox photocopies", "originals nahi", "mere paas nahi hain", "available nahi", "original nahi",
            "mere paas nahi"
        ]
        pos_doc_patterns = [
            "original documents", "original papers", "original deed", "registry", "deeds", "papers ready",
            "original paper", "originals available", "mere paas hain", "original documents hain", "originals hain",
            "registry ready", "original documents ready", "original registry", "papers are with me", "original documents available"
        ]

        if any(k in u for k in neg_doc_patterns):
            self.state.slots["original_documents_available"] = False
        elif any(k in u for k in pos_doc_patterns):
            self.state.slots["original_documents_available"] = True

        # --- 4. Market Value vs Loan Amount Extraction ---
        self._extract_monetary_amounts(u)

        # --- 5. Occupation & Income Mode ---
        cash_patterns = [
            "strictly in cash", "in cash, no bank", "no bank account", "cash only", "sirf cash",
            "cash mein salary", "salary cash", "cash milta hai", "cash mein", "nakad", "earnings are strictly in cash"
        ]
        bank_patterns = [
            "salary bank mein aati hai", "bank account mein salary", "salary directly bank", "salary comes into my bank",
            "salary comes directly to my bank", "bank account", "bank mein", "account mein",
            "directly bank", "icici", "hdfc", "sbi", "transfer", "direct deposit", "current bank account",
            "payment bank mein", "bank credit", "salary in bank"
        ]
        salaried_patterns = [
            "salaried", "salary", "job", "software", "manager", "it firm", "naukri", "company", "infosys",
            "employee", "job karta", "job karti", "company mein kaam", "salary milti"
        ]
        self_employed_patterns = [
            "self-employed", "self employed", "business", "wholesale", "trader", "manufacturing",
            "apna business", "business karta", "business karti", "dukaan chalata", "dukaan chalati", "businessman", "profession"
        ]

        if any(k in u for k in cash_patterns):
            self.state.slots["income_mode"] = "Cash"
            if self.state.slots["occupation"] is None:
                self.state.slots["occupation"] = "Self-Employed"
        elif any(k in u for k in bank_patterns):
            self.state.slots["income_mode"] = "Bank"

        if any(k in u for k in salaried_patterns):
            self.state.slots["occupation"] = "Salaried"
        elif any(k in u for k in self_employed_patterns) or ("shop" in u and "commercial shop" not in u):
            self.state.slots["occupation"] = "Self-Employed"

        # --- 6. Tenure ---
        parsed_tenure = self._parse_tenure(u)
        if parsed_tenure is not None:
            self.state.slots["tenure"] = parsed_tenure

        # =============================================================
        # STAGE 2: CONTEXT-AWARE FALLBACK EXTRACTION
        # =============================================================
        if active_slot:
            # Context A: Ownership Status Active
            if active_slot == "ownership_status" and self.state.slots["ownership_status"] is None:
                if any(re.search(r'\b' + re.escape(w) + r'\b', u) for w in [
                    "akela", "akele", "akeli", "sirf mera", "meri", "mera", "mere", "single", "sole", "myself", "me", "mera akele ka"
                ]):
                    self.state.slots["ownership_status"] = "Sole"
                elif any(re.search(r'\b' + re.escape(w) + r'\b', u) for w in [
                    "joint", "jointly", "dono", "hum dono", "wife", "husband", "family", "partner", "joint hai"
                ]):
                    self.state.slots["ownership_status"] = "Joint"

            # Context B: Original Documents Active
            elif active_slot == "original_documents_available" and self.state.slots["original_documents_available"] is None:
                if any(re.search(r'\b' + re.escape(w) + r'\b', u) for w in [
                    "yes", "haan", "hain", "ji", "ji haan", "haanji", "ha", "yep", "yeah", "available", "available hain",
                    "mere paas hain", "bilkul", "ready", "ready hain", "hai", "rakhe hain"
                ]):
                    self.state.slots["original_documents_available"] = True
                elif any(re.search(r'\b' + re.escape(w) + r'\b', u) for w in [
                    "no", "nahi", "nahi hain", "available nahi", "mere paas nahi", "photocopy", "xerox", "missing", "nah", "nope", "mere paas nahi hain"
                ]):
                    self.state.slots["original_documents_available"] = False

            # Context C: Property Type Active
            elif active_slot == "property_type" and self.state.slots["property_type"] is None:
                if any(w in u for w in ["ghar", "makan", "flat", "residential", "house", "apartment", "villa", "home", "3bhk", "2bhk"]):
                    if "warehouse" not in u:
                        self.state.slots["property_type"] = "Residential"
                elif any(w in u for w in ["dukaan", "shop", "office", "commercial", "showroom"]):
                    self.state.slots["property_type"] = "Commercial"
                elif any(w in u for w in ["factory", "industrial", "warehouse", "godown", "shed"]):
                    self.state.slots["property_type"] = "Industrial"
                elif any(w in u for w in ["kheti", "agricultural", "agriculture", "farmland", "farm"]):
                    self.state.slots["property_type"] = "Agricultural"

            # Context D: Loan Amount Active
            elif active_slot == "loan_amount" and self.state.slots["loan_amount"] is None:
                val = self._parse_numeric_or_word_amount(u)
                if val:
                    self.state.slots["loan_amount"] = val

            # Context E: Market Value Active
            elif active_slot == "property_market_value" and self.state.slots["property_market_value"] is None:
                val = self._parse_market_value_expression(u)
                if val:
                    self.state.slots["property_market_value"] = val

            # Context F: Tenure Active
            elif active_slot == "tenure" and self.state.slots["tenure"] is None:
                val = self._parse_tenure(u)
                if val is not None:
                    self.state.slots["tenure"] = val

            # Context G: Occupation & Income Mode Active
            elif active_slot == "occupation_and_income":
                if self.state.slots["occupation"] is None:
                    if any(w in u for w in ["salaried", "naukri", "job", "salary", "employee"]):
                        self.state.slots["occupation"] = "Salaried"
                    elif any(w in u for w in ["business", "self", "dukaan", "trader", "businessman"]):
                        self.state.slots["occupation"] = "Self-Employed"
                if self.state.slots["income_mode"] is None:
                    if any(w in u for w in ["bank", "account", "online", "cheque"]):
                        self.state.slots["income_mode"] = "Bank"
                    elif any(w in u for w in ["cash", "nakad"]):
                        self.state.slots["income_mode"] = "Cash"

    def _extract_monetary_amounts(self, u: str) -> None:
        """Disambiguates requested loan amount from property market value using local context windows."""
        
        # Helper function to check if context around match has valuation keywords
        def is_valuation(idx: int, match_len: int) -> bool:
            pre = u[max(0, idx-30):idx]
            post = u[idx+match_len:min(len(u), idx+match_len+30)]
            return any(k in (pre + post) for k in ["worth", "value", "market", "property ki value", "property value", "anumanit"])

        def is_loan_req(idx: int, match_len: int) -> bool:
            pre = u[max(0, idx-30):idx]
            post = u[idx+match_len:min(len(u), idx+match_len+30)]
            return any(k in (pre + post) for k in ["need", "chahiye", "borrow", "loan amount", "loan of", "looking for", "strictly need"])

        # Scan for Crore matches
        cr_matches = list(re.finditer(r'([₹\w\.]+)\s*(?:crores?|cr)\b', u))
        for m in cr_matches:
            raw_str = m.group(1).replace("₹", "").strip()
            num_val = float(HINDI_NUMBER_MAP.get(raw_str, raw_str)) if raw_str in HINDI_NUMBER_MAP or re.match(r'^\d+(\.\d+)?$', raw_str) else None
            if num_val:
                idx = m.start()
                if is_valuation(idx, len(m.group(0))) or not is_loan_req(idx, len(m.group(0))):
                    if self.state.slots["property_market_value"] is None or is_valuation(idx, len(m.group(0))):
                        self.state.slots["property_market_value"] = f"{int(num_val) if num_val.is_integer() else num_val} Crore"
                else:
                    self.state.slots["loan_amount"] = int(num_val * 10000000)

        # Scan for Lakh matches
        lakh_matches = list(re.finditer(r'([₹\w\.]+)\s*(?:lakhs?|lacs?|lac|l)\b', u))
        for m in lakh_matches:
            raw_str = m.group(1).replace("₹", "").strip()
            num_val = float(HINDI_NUMBER_MAP.get(raw_str, raw_str)) if raw_str in HINDI_NUMBER_MAP or re.match(r'^\d+(\.\d+)?$', raw_str) else None
            if num_val:
                idx = m.start()
                if is_valuation(idx, len(m.group(0))) and not is_loan_req(idx, len(m.group(0))):
                    if self.state.slots["property_market_value"] is None or is_valuation(idx, len(m.group(0))):
                        self.state.slots["property_market_value"] = f"{int(num_val) if num_val.is_integer() else num_val} Lakhs"
                else:
                    if self.state.slots["loan_amount"] is None or is_loan_req(idx, len(m.group(0))):
                        self.state.slots["loan_amount"] = int(num_val * 100000)

        # Standalone Hindi Number check
        if any(k in u for k in ["pachaas lakh", "pachas lakh", "fifty lakh"]):
            if "worth" not in u and "market" not in u:
                self.state.slots["loan_amount"] = 5000000
        if any(k in u for k in ["60 lakh", "60l", "saath lakh"]):
            if "worth" not in u and "market" not in u:
                self.state.slots["loan_amount"] = 6000000
        if any(k in u for k in ["pachattar lakh", "75 lakh"]):
            if "worth" not in u and "market" not in u:
                self.state.slots["loan_amount"] = 7500000
        if any(k in u for k in ["assi lakh", "80 lakh"]):
            if "worth" not in u and "market" not in u:
                self.state.slots["loan_amount"] = 8000000

    def _parse_numeric_or_word_amount(self, text: str) -> Optional[int]:
        t = text.lower().replace("₹", "").strip()
        if "1.5 crore" in t or "1.5 cr" in t or "dedh crore" in t:
            return 15000000
        if "1.2 crore" in t or "1.2 cr" in t:
            return 12000000
        if "1 crore" in t or "1 cr" in t or "ek crore" in t or "one crore" in t:
            return 10000000

        m = re.search(r'([₹\w\.]+)\s*(?:lakhs?|lacs?|lac|l)\b', t)
        if m:
            raw = m.group(1).replace("₹", "").strip()
            if raw in HINDI_NUMBER_MAP:
                return int(HINDI_NUMBER_MAP[raw] * 100000)
            try:
                return int(float(raw) * 100000)
            except ValueError:
                pass

        for hw, num in HINDI_NUMBER_MAP.items():
            if hw in t and ("lakh" in t or "lac" in t):
                return int(num * 100000)

        m_num = re.search(r'^\s*(\d{1,3})\s*$', t)
        if m_num:
            val = int(m_num.group(1))
            if 10 <= val <= 99:
                return val * 100000

        return None

    def _parse_market_value_expression(self, text: str) -> Optional[str]:
        t = text.lower().replace("₹", "").strip()
        if "1.5 crore" in t or "1.5 cr" in t or "dedh crore" in t:
            return "1.5 Crore"
        if "1.2 crore" in t or "1.2 cr" in t:
            return "1.2 Crore"
        if "1.1 crore" in t or "1.1 cr" in t:
            return "1.1 Crore"
        if "2 crore" in t or "2 cr" in t or "do crore" in t:
            return "2 Crore"
        if "1 crore" in t or "1 cr" in t or "ek crore" in t or "one crore" in t:
            return "1 Crore"
        if "85 lakhs" in t or "85 lakh" in t:
            return "85 Lakhs"
        if "90 lakhs" in t or "90 lakh" in t:
            return "90 Lakhs"
        if "80 lakhs" in t or "80 lakh" in t:
            return "80 Lakhs"
        if "70 lakhs" in t or "70 lakh" in t:
            return "70 Lakhs"
        if "60 lakhs" in t or "60 lakh" in t:
            return "60 Lakhs"

        m = re.search(r'([₹\w\.]+)\s*(crores?|cr|lakhs?|lacs?|lac)\b', t)
        if m:
            raw_num = m.group(1).replace("₹", "").strip()
            unit = m.group(2)
            num_val = HINDI_NUMBER_MAP.get(raw_num, raw_num)
            unit_str = "Crore" if "cr" in unit else "Lakhs"
            return f"{num_val} {unit_str}"
        return None

    def _parse_tenure(self, text: str) -> Optional[int]:
        t = text.lower().strip()
        if re.search(r'\b(pandrah saal|fifteen years|15 saal|15 years|15 yrs)\b', t):
            return 15
        if re.search(r'\b(dus saal|das saal|ten years|10 saal|10 years|10 yrs)\b', t):
            return 10
        if re.search(r'\b(paanch saal|panch saal|five years|5 saal|5 years|5 yrs)\b', t):
            return 5
        if re.search(r'\b(saat saal|seven years|7 saal|7 years|7 yrs)\b', t):
            return 7
        if re.search(r'\b(aath saal|eight years|8 saal|8 years|8 yrs)\b', t):
            return 8
        if re.search(r'\b(baarah saal|twelve years|12 saal|12 years|12 yrs)\b', t):
            return 12
        if re.search(r'\b(teen saal|three years|3 saal|3 years|3 yrs)\b', t):
            return 3
        if re.search(r'\b(chaar saal|four years|4 saal|4 years|4 yrs)\b', t):
            return 4
        if re.search(r'\b(do saal|two years|2 saal|2 years|2 yrs)\b', t):
            return 2
        if re.search(r'\b(bees saal|twenty years|20 saal|20 years|20 yrs)\b', t):
            return 20
        if re.search(r'\b(pachees saal|twenty five years|25 saal|25 years|25 yrs)\b', t):
            return 25

        m = re.search(r'\b(\d{1,2})\s*(?:years?|saal|yrs|yr)\b', t)
        if m:
            val = int(m.group(1))
            if val not in [50, 60, 75, 80, 40, 30, 35, 45, 70, 90]:
                return val

        if self.state.metadata.get("active_question_slot") == "tenure":
            m_single = re.search(r'^\s*(\d{1,2})\s*$', t)
            if m_single:
                return int(m_single.group(1))

        return None

    def _all_slots_valid(self) -> bool:
        s = self.state.slots
        return (
            s["property_type"] in ["Residential", "Commercial", "Industrial"] and
            s["ownership_status"] in ["Sole", "Joint"] and
            s["original_documents_available"] is True and
            s["loan_amount"] is not None and s["loan_amount"] <= 7500000 and
            s["occupation"] in ["Salaried", "Self-Employed"] and
            s["income_mode"] == "Bank" and
            s["property_market_value"] is not None and
            s["tenure"] is not None and 3 <= s["tenure"] <= 15
        )

    def _prompt_next_missing_slot(self) -> str:
        s = self.state.slots
        is_hi = self.state.is_hindi()

        if s["property_type"] is None:
            self.state.metadata["active_question_slot"] = "property_type"
            if is_hi:
                return "Kya aap bata sakte hain ki aapki property Residential (ghar/flat), Commercial (dukaan/office), ya Industrial hai?"
            return "To start, could you tell me if your property is residential, commercial, or industrial?"

        if s["ownership_status"] is None:
            self.state.metadata["active_question_slot"] = "ownership_status"
            if is_hi:
                return "Kya aap is property ke akele malik hain ya yeh joint property hai?"
            return "Got it. And are you the sole owner of the property, or is it jointly owned?"

        if s["original_documents_available"] is None:
            self.state.metadata["active_question_slot"] = "original_documents_available"
            if is_hi:
                return "Kya verification ke liye property ke original documents aapke paas uplabdh hain?"
            return "Do you have the original property documents ready and available for verification?"

        if s["loan_amount"] is None:
            self.state.metadata["active_question_slot"] = "loan_amount"
            if is_hi:
                return "Aap kitna loan amount lena chahte hain?"
            return "How much loan amount are you looking to borrow?"

        if s["occupation"] is None or s["income_mode"] is None:
            self.state.metadata["active_question_slot"] = "occupation_and_income"
            if is_hi:
                return "Kya aap Salaried hain ya Self-Employed, aur aapki income bank account mein aati hai ya cash mein?"
            return "Are you currently salaried or self-employed, and do you receive your income through a bank account or in cash?"

        if s["property_market_value"] is None:
            self.state.metadata["active_question_slot"] = "property_market_value"
            if is_hi:
                return "Aapki property ki anumanit market value kitni hogi?"
            return "What would be the approximate current market value of your property?"

        if s["tenure"] is None:
            self.state.metadata["active_question_slot"] = "tenure"
            if is_hi:
                return "Aap yeh loan kitne saalon mein repay karna chahenge?"
            return "Over how many years would you like to repay the loan?"

        self.state.metadata["active_question_slot"] = None
        return "Thank you."
