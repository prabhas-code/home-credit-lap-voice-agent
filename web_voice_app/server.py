"""
Lightweight Local Voice Agent Web Server.
Provides a web browser UI with microphone voice interaction, real-time speech synthesis (TTS),
live speech recognition (STT), audio call recording, and transcript download.
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "simulator"))
from agent_engine import HomeCreditVoiceAgent

# In-memory sessions
sessions: dict = {}


class VoiceAgentHTTPHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html_path = os.path.join(os.path.dirname(__file__), "index.html")
            with open(html_path, "rb") as f:
                self.wfile.write(f.read())
            return
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        body = json.loads(post_data) if post_data else {}

        if parsed.path == "/api/start_call":
            session_id = body.get("session_id", "default")
            lang = body.get("language", "English")
            cust = body.get("customer_name", "Mr. Rajesh Sharma")
            agent_gender = body.get("agent_gender", "female")

            agent = HomeCreditVoiceAgent({
                "company_name": "Home Credit",
                "customer_name": cust,
                "agent_name": "Priya" if agent_gender == "female" else "Aarav",
                "agent_gender": agent_gender,
                "language_to_speak": lang
            })
            sessions[session_id] = agent
            greeting = agent.get_initial_greeting()

            self._send_json({
                "agent_response": greeting,
                "call_state": agent.state.call_state,
                "slots": agent.state.slots
            })

        elif parsed.path == "/api/process_turn":
            session_id = body.get("session_id", "default")
            user_text = body.get("user_utterance", "")
            agent = sessions.get(session_id)

            if not agent:
                agent = HomeCreditVoiceAgent()
                sessions[session_id] = agent

            res = agent.process_turn(user_text)
            self._send_json(res)

        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data: dict):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def run_server(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, VoiceAgentHTTPHandler)
    print("=" * 80)
    print(f"🎙️  LOCAL VOICE AGENT WEB APP RUNNING AT: http://localhost:{port}")
    print("Open http://localhost:8080 in Chrome or Edge to speak with your microphone!")
    print("=" * 80)
    httpd.serve_forever()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
