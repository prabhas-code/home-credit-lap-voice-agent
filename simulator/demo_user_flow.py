"""
Demonstration script for User-Specified Flows
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agent_engine import HomeCreditVoiceAgent


def run_demo():
    print("=" * 80)
    print("DEMO 1: USER-SPECIFIED HINDI FEMALE FLOW")
    print("=" * 80)
    agent = HomeCreditVoiceAgent({
        "company_name": "Home Credit",
        "customer_name": "Rajesh",
        "agent_name": "Priya",
        "agent_gender": "female",
        "language_to_speak": "Hindi"
    })

    print("[AGENT]:", agent.get_initial_greeting(), "\n")
    turns = [
        "yes",
        "I have a 3BHK flat in Noida worth 1.2 crore and need 50 lakhs",
        "akela",
        "haan",
        "salaried hoon, salary bank account mein aati hai",
        "10 saal"
    ]

    for t in turns:
        print("[CUSTOMER]:", t)
        res = agent.process_turn(t)
        st = res["call_state"]
        resp = res["agent_response"]
        print(f"[AGENT ({st})]: {resp}")
        filled = {k: v for k, v in res["slots"].items() if v is not None}
        print(f"   📊 [SLOTS ({len(filled)}/8)]: {filled}\n")

    print("=" * 80)
    print("DEMO 2: JOINT + ORIGINAL DOCUMENTS TEST")
    print("=" * 80)
    agent2 = HomeCreditVoiceAgent({
        "company_name": "Home Credit",
        "customer_name": "Rajesh",
        "agent_name": "Priya",
        "agent_gender": "female",
        "language_to_speak": "Hindi"
    })
    agent2.get_initial_greeting()
    agent2.process_turn("haan")
    agent2.process_turn("sure bataiye")
    agent2.process_turn("ghar hai")

    print("[CUSTOMER]: joint hai")
    r1 = agent2.process_turn("joint hai")
    print(f"[AGENT]: {r1['agent_response']}")
    print("   📊 [SLOTS]:", {k: v for k, v in r1["slots"].items() if v is not None}, "\n")

    print("[CUSTOMER]: original documents mere paas hain")
    r2 = agent2.process_turn("original documents mere paas hain")
    print(f"[AGENT]: {r2['agent_response']}")
    print("   📊 [SLOTS]:", {k: v for k, v in r2["slots"].items() if v is not None}, "\n")


if __name__ == "__main__":
    run_demo()
