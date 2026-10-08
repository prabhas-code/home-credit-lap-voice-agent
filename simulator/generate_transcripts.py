"""
Generates complete markdown conversation transcripts for all test scenarios.
"""

import json
import os
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agent_engine import HomeCreditVoiceAgent


def set_default_serializer(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def generate_all_transcripts():
    scenarios_path = os.path.join(os.path.dirname(__file__), "..", "test_suite", "scenarios.json")
    output_path = os.path.join(os.path.dirname(__file__), "..", "transcripts", "all_scenario_transcripts.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(scenarios_path, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    lines = [
        "# CALL LOGS & COMPLETE CONVERSATION TRANSCRIPTS",
        "",
        "This document contains the exact turn-by-turn conversation transcripts, runtime state transitions, and slot updates across all 20 verified test scenarios for the **Home Credit Loan Against Property (LAP) AI Voice Agent**.",
        "",
        "---",
        ""
    ]

    for sc in scenarios:
        sc_id = sc["id"]
        name = sc["name"]
        desc = sc["description"]
        context = sc.get("context", {})
        turns = sc.get("turns", [])
        expected_final_state = sc.get("expected_final_state")
        disposition = sc.get("disposition")

        lines.append(f"## [{sc_id}] {name}")
        lines.append(f"**Objective**: {desc}  ")
        lines.append(f"**Language**: `{context.get('language_to_speak', 'English')}` | **Agent Gender**: `{context.get('agent_gender', 'female')}` | **Expected Disposition**: `{disposition}`")
        lines.append("")
        lines.append("### Dialogue Flow:")
        lines.append("```text")

        agent = HomeCreditVoiceAgent(context)
        initial_greeting = agent.get_initial_greeting()
        lines.append(f"[AGENT (State: {agent.state.call_state})]: {initial_greeting}")

        turn_idx = 1
        for turn in turns:
            user_text = turn["user"]
            lines.append(f"[CUSTOMER (Turn {turn_idx})]: {user_text}")
            result = agent.process_turn(user_text)
            lines.append(f"[AGENT (State: {result['call_state']})]: {result['agent_response']}")
            turn_idx += 1
            if result["is_terminal"]:
                break

        lines.append("```")
        lines.append("")
        lines.append("**Final Captured Slots & State**:")
        lines.append("```json")
        lines.append(json.dumps({
            "final_state": agent.state.call_state,
            "disposition": disposition,
            "slots": agent.state.slots,
            "metadata": agent.state.metadata
        }, indent=2, default=set_default_serializer))
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Successfully generated full transcripts for {len(scenarios)} scenarios at: {output_path}")


if __name__ == "__main__":
    generate_all_transcripts()
