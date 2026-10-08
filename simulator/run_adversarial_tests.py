"""
Adversarial & Natural Language Test Suite Runner for Home Credit LAP Voice Agent
Executes 33+ natural-language, short-answer, Hindi/Hinglish, compound, and edge-case tests.
Includes strict verification of the Repetition Detector Rule.
"""

import json
import os
import sys

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agent_engine import HomeCreditVoiceAgent


def test_repetition_detector():
    """
    Dedicated test for Repetition Detection:
    Ensures that when a customer provides an answer, the agent never asks that question again.
    """
    print("\n" + "=" * 80)
    print("RUNNING REPETITION DETECTOR VERIFICATION")
    print("=" * 80)
    
    agent = HomeCreditVoiceAgent({
        "customer_name": "Rajesh",
        "agent_name": "Priya",
        "agent_gender": "female",
        "language_to_speak": "Hindi"
    })
    
    # 1. Start call
    agent.get_initial_greeting()
    # Turn 1: Confirm identity
    r1 = agent.process_turn("haan")
    # Turn 2: Accept offer
    r2 = agent.process_turn("theek hai bataiye")
    # Prompt asks: property type
    assert "property" in r2["agent_response"].lower()
    
    # Turn 3: Customer says "residential flat"
    r3 = agent.process_turn("residential flat")
    # Slot property_type is populated
    assert agent.state.slots["property_type"] == "Residential"
    # Next prompt MUST ask ownership, NOT property type
    assert "property" not in r3["agent_response"].lower() or "malik" in r3["agent_response"].lower()
    assert "malik" in r3["agent_response"].lower() or "joint" in r3["agent_response"].lower()
    
    # Turn 4: Customer gives short answer "akela"
    r4 = agent.process_turn("akela")
    # Slot ownership_status is populated
    assert agent.state.slots["ownership_status"] == "Sole", f"Expected Sole, got {agent.state.slots['ownership_status']}"
    # Agent MUST NOT ask ownership question again! Next prompt MUST ask original documents!
    assert "malik" not in r4["agent_response"].lower() and "akele" not in r4["agent_response"].lower(), "ERROR: Agent repeated ownership question after 'akela'!"
    assert "document" in r4["agent_response"].lower() or "kagazat" in r4["agent_response"].lower() or "documents" in r4["agent_response"].lower()
    
    # Turn 5: Customer gives short answer "haan" to documents
    r5 = agent.process_turn("haan")
    # Slot original_documents_available is populated
    assert agent.state.slots["original_documents_available"] is True, f"Expected True, got {agent.state.slots['original_documents_available']}"
    # Agent MUST NOT ask documents question again! Next prompt MUST ask loan amount!
    assert "document" not in r5["agent_response"].lower() and "documents" not in r5["agent_response"].lower(), "ERROR: Agent repeated documents question after 'haan'!"
    assert "loan" in r5["agent_response"].lower() or "amount" in r5["agent_response"].lower()
    
    print("✅ REPETITION DETECTOR PASSED: Agent strictly progresses without repeating answered slots!")
    print("=" * 80 + "\n")
    return True


def run_adversarial_suite(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    total = len(scenarios)
    passed_count = 0
    failures = []

    print("=" * 80)
    print(f"RUNNING {total} ADVERSARIAL & NATURAL HINDI/ENGLISH TEST SCENARIOS")
    print("=" * 80)

    for sc in scenarios:
        sc_id = sc["id"]
        name = sc["name"]
        context = sc.get("context", {})
        turns = sc.get("turns", [])
        expected_final_state = sc.get("expected_final_state")
        expected_slots = sc.get("expected_slots", {})

        agent = HomeCreditVoiceAgent(context)
        agent.get_initial_greeting()

        for turn in turns:
            res = agent.process_turn(turn["user"])
            if res["is_terminal"]:
                break

        # Verification
        passed = True
        errs = []

        if expected_final_state and agent.state.call_state != expected_final_state:
            passed = False
            errs.append(f"State expected '{expected_final_state}', got '{agent.state.call_state}'")

        for k, v in expected_slots.items():
            actual = agent.state.slots.get(k)
            if v != actual:
                passed = False
                errs.append(f"Slot '{k}' expected '{v}', got '{actual}'")

        if passed:
            passed_count += 1
            print(f"[{sc_id}] {name:<65} -> [PASS]")
        else:
            print(f"[{sc_id}] {name:<65} -> [FAIL]")
            for e in errs:
                print(f"     ↳ Error: {e}")
            failures.append((sc_id, name, errs))

    print("=" * 80)
    print(f"ADVERSARIAL TEST SUMMARY: {passed_count}/{total} PASSED ({passed_count/total*100:.1f}%)")
    print("=" * 80)

    return passed_count == total


if __name__ == "__main__":
    rep_ok = test_repetition_detector()
    adv_path = os.path.join(os.path.dirname(__file__), "..", "test_suite", "adversarial_scenarios.json")
    adv_ok = run_adversarial_suite(adv_path)
    
    if rep_ok and adv_ok:
        print("\n🏆 ALL TESTS & REPETITION CHECKS PASSED 100%!")
        sys.exit(0)
    else:
        sys.exit(1)
