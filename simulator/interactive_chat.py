"""
Interactive CLI Simulator for Home Credit LAP AI Voice Agent.
Allows you to roleplay as a customer and talk to the voice agent in real time.
"""

import sys
import os

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agent_engine import HomeCreditVoiceAgent


def run_interactive_session():
    print("=" * 80)
    print("       HOME CREDIT LOAN AGAINST PROPERTY (LAP) VOICE AGENT SIMULATOR")
    print("=" * 80)
    print("Select Language:")
    print("1. English (Default)")
    print("2. Hindi (Female Agent - Priya)")
    print("3. Hindi (Male Agent - Aarav)")
    choice = input("\nEnter choice (1/2/3) [Default 1]: ").strip()

    context = {
        "company_name": "Home Credit",
        "customer_name": "Mr. Rajesh Sharma",
        "agent_name": "Priya",
        "agent_gender": "female",
        "current_date": "2026-10-08",
        "current_day": "Thursday",
        "current_time": "04:30 PM",
        "language_to_speak": "English",
        "additional_context_from_rag": "Home Credit LAP offers up to 75 Lakhs, tenures 3-15 years, minimal documentation, senior loan expert consultation."
    }

    if choice == "2":
        context["language_to_speak"] = "Hindi"
        context["customer_name"] = "Rajesh"
        context["agent_name"] = "Priya"
        context["agent_gender"] = "female"
    elif choice == "3":
        context["language_to_speak"] = "Hindi"
        context["customer_name"] = "Rajesh"
        context["agent_name"] = "Aarav"
        context["agent_gender"] = "male"

    agent = HomeCreditVoiceAgent(context)
    print("\n" + "-" * 80)
    print(f"Call Connected | Language: {context['language_to_speak']} | Agent: {context['agent_name']} ({context['agent_gender']})")
    print("Type 'exit' or 'quit' at any time to end the simulation.")
    print("-" * 80 + "\n")

    # Initial greeting
    initial_greeting = agent.get_initial_greeting()
    print(f"🎙️  AGENT: {initial_greeting}\n")

    while True:
        try:
            user_input = input("👤 CUSTOMER: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nCall ended by user.")
            break

        result = agent.process_turn(user_input)
        print(f"\n🎙️  AGENT (State: {result['call_state']}): {result['agent_response']}\n")

        # Show slot state summary
        filled_slots = {k: v for k, v in result["slots"].items() if v is not None}
        print(f"   📊 [State: {result['call_state']} | Captured Slots ({len(filled_slots)}/8): {filled_slots}]")
        print("-" * 80 + "\n")

        if result["is_terminal"]:
            print("=" * 80)
            print(f"🏁 CALL TERMINATED with state: {result['call_state']}")
            print("Final Captured Qualification State:")
            for k, v in result["slots"].items():
                print(f"  • {k:<30}: {v}")
            if result["metadata"].get("disqualification_reason"):
                print(f"  • Disqualification Reason     : {result['metadata']['disqualification_reason']}")
            if result["metadata"].get("transfer_reason"):
                print(f"  • Transfer Reason             : {result['metadata']['transfer_reason']}")
            if result["metadata"].get("callback_time"):
                print(f"  • Callback Time               : {result['metadata']['callback_time']}")
            print("=" * 80)
            break


if __name__ == "__main__":
    run_interactive_session()
