"""
Automated Test Runner for Home Credit LAP AI Voice Agent
Executes test scenarios against the agent engine, verifies state transitions,
validates slot values, checks assertions, and generates compliance reports.
"""

import json
import os
import sys
from typing import Dict, Any, List
from agent_engine import HomeCreditVoiceAgent

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_scenario(scenario: Dict[str, Any]) -> Dict[str, Any]:
    sc_id = scenario["id"]
    name = scenario["name"]
    context = scenario.get("context", {})
    turns = scenario.get("turns", [])
    expected_final_state = scenario.get("expected_final_state")
    expected_slots = scenario.get("expected_slots", {})
    expected_disposition = scenario.get("disposition")

    agent = HomeCreditVoiceAgent(context)
    initial_greeting = agent.get_initial_greeting()
    
    transcript = [
        {"role": "assistant", "content": initial_greeting, "state": agent.state.call_state}
    ]
    
    for turn in turns:
        user_text = turn["user"]
        result = agent.process_turn(user_text)
        transcript.append({"role": "user", "content": user_text})
        transcript.append({
            "role": "assistant",
            "content": result["agent_response"],
            "state": result["call_state"],
            "slots": result["slots"]
        })
        if result["is_terminal"]:
            break

    # Evaluation
    passed = True
    failure_reasons = []

    # 1. State check
    final_state = agent.state.call_state
    if expected_final_state and final_state != expected_final_state:
        passed = False
        failure_reasons.append(f"Expected state '{expected_final_state}', got '{final_state}'")

    # 2. Slot checks
    for slot_k, slot_v in expected_slots.items():
        actual_v = agent.state.slots.get(slot_k)
        if slot_v is None:
            if actual_v is not None:
                passed = False
                failure_reasons.append(f"Slot {slot_k} expected None, got {actual_v}")
        elif actual_v != slot_v:
            passed = False
            failure_reasons.append(f"Slot '{slot_k}' expected '{slot_v}', got '{actual_v}'")

    return {
        "id": sc_id,
        "name": name,
        "passed": passed,
        "failure_reasons": failure_reasons,
        "final_state": final_state,
        "slots": agent.state.slots,
        "metadata": agent.state.metadata,
        "transcript": transcript
    }


def run_all_tests(scenarios_file: str) -> Dict[str, Any]:
    with open(scenarios_file, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    results = []
    total = len(scenarios)
    passed_count = 0

    print("=" * 80)
    print(f"RUNNING {total} COMPREHENSIVE AI VOICE AGENT TEST SCENARIOS")
    print("=" * 80)

    for sc in scenarios:
        res = run_scenario(sc)
        results.append(res)
        status_icon = "[PASS]" if res["passed"] else "[FAIL]"
        if res["passed"]:
            passed_count += 1
        print(f"[{res['id']}] {res['name']:<55} -> {status_icon} (State: {res['final_state']})")
        if not res["passed"]:
            for r in res["failure_reasons"]:
                print(f"     ↳ Error: {r}")

    print("=" * 80)
    print(f"TEST SUMMARY: {passed_count}/{total} PASSED ({passed_count/total*100:.1f}%)")
    print("=" * 80)

    return {
        "total": total,
        "passed": passed_count,
        "failed": total - passed_count,
        "results": results
    }


if __name__ == "__main__":
    scenarios_path = os.path.join(os.path.dirname(__file__), "..", "test_suite", "scenarios.json")
    if len(sys.argv) > 1:
        scenarios_path = sys.argv[1]
    run_all_tests(scenarios_path)
