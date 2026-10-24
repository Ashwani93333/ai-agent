import os
import sys
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

try:
    from uagents_core.utils.registration import (
        register_chat_agent,
        RegistrationRequestCredentials,
    )
except ImportError:
    print("❌ Error: uagents_core is not installed. Run via .venv\\Scripts\\python.exe")
    sys.exit(1)

agentverse_key = os.getenv("AGENTVERSE_KEY") or os.getenv("AGENTVERSE_API_KEY")
agent_seed = os.getenv("AGENT_SEED_PHRASE") or os.getenv("VOYAGE_ORCHESTRATOR_SEED", "voyage-ai-orchestrator-hackathon-seed-2026")
endpoint_url = os.getenv("AGENT_ENDPOINT_URL", "https://nine-phones-drive.loca.lt/sumbit")

if not agentverse_key:
    print("\n⚠️  MISSING AGENTVERSE_KEY!")
    print("1. Click the purple 'Copy' button on your Agentverse screen next to AGENTVERSE_KEY.")
    print("2. Paste it into your .env file: AGENTVERSE_KEY=\"your_copied_key_here\"")
    print("3. Run: .venv\\Scripts\\python register_agent.py\n")
    sys.exit(1)

print(f"🚀 Registering agent 'voyage-concierge' on Agentverse...")
print(f"• Endpoint: {endpoint_url}")

try:
    register_chat_agent(
        "voyage-concierge",
        endpoint_url,
        active=True,
        credentials=RegistrationRequestCredentials(
            agentverse_api_key=agentverse_key,
            agent_seed_phrase=agent_seed,
        ),
    )
    print("\n✅ SUCCESS: Agent 'voyage-concierge' registered on Agentverse!")
    print("👉 Now switch back to your Agentverse browser tab and click 'Evaluate Registration'.\n")
except Exception as e:
    print(f"\n❌ Registration failed with error: {e}")
    sys.exit(1)
