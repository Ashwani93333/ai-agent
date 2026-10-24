import json
import logging
import os
import re
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, Any, Optional

from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("VoyageOrchestrator")

class _MockAgent:
    def __init__(self, name="agent", seed="", port=8000, endpoint=None):
        self.name = name
        self.seed = seed
        self.port = port
        self.endpoint = endpoint or []
        self.address = f"agent1q{seed[:10]}mockaddress"

    def include(self, protocol):
        pass

    def run(self):
        print(f"[MockAgent] Running {self.name} at {self.address}")

class _MockProtocol:
    def __init__(self, spec=None, name="proto", version="1.0.0"):
        self.spec = spec
        self.name = name
        self.version = version

    def on_message(self, model):
        def decorator(f):
            return f
        return decorator

try:
    from uagents import Agent, Context, Protocol
    from uagents_core.contrib.protocols.chat import (
        ChatAcknowledgement,
        ChatMessage,
        MetadataContent,
        TextContent,
        chat_protocol_spec,
    )
except ImportError:
    # Graceful mock classes for typing & local testing when uagents is installing
    Agent = _MockAgent  # type: ignore
    Context = object  # type: ignore
    Protocol = _MockProtocol  # type: ignore
    ChatAcknowledgement = dict  # type: ignore
    ChatMessage = dict  # type: ignore
    MetadataContent = dict  # type: ignore
    TextContent = dict  # type: ignore
    chat_protocol_spec = None  # type: ignore

from agents.flight_agent import (
    build_flights_carousel,
    build_flight_detail,
    get_flight_by_id,
)
from agents.hotel_agent import (
    build_hotels_carousel,
    build_hotel_detail,
    get_hotel_by_id,
)
from agents.activity_agent import (
    build_activities_carousel,
    get_activity_by_id,
)
from agents.payment_agent import (
    build_traveler_form,
    build_review_card,
    calculate_trip_totals,
)

# Agent setup
SEED_PHRASE = os.getenv("VOYAGE_ORCHESTRATOR_SEED", "voyage-ai-orchestrator-hackathon-seed-2026")
PORT = int(os.getenv("PORT", "8000"))
ENDPOINT_URL = os.getenv("AGENT_ENDPOINT_URL", f"http://127.0.0.1:{PORT}/submit")

agent = Agent(
    name="voyage_concierge",
    seed=SEED_PHRASE,
    port=PORT,
    endpoint=[ENDPOINT_URL]
)

# Initialize Agent Chat Protocol (ACP)
if chat_protocol_spec:
    chat_proto = Protocol(spec=chat_protocol_spec)
else:
    chat_proto = Protocol(name="chat_protocol", version="1.0.0")


# ──────────────────────────────────────────────────────────────────────────────
# Helper: Build ASI:One ChatMessage with Text + Interactive Card Declaration
# ──────────────────────────────────────────────────────────────────────────────

def card_message(
    narration: str,
    card_kind: str,
    card_payload: Dict[str, Any],
    is_terminal: bool = False
) -> Any:
    """Builds a compliant ASI:One ChatMessage containing a text bubble and card metadata."""
    metadata = {
        "card_protocol_version": "1",
        "requires_card_interaction": "false" if is_terminal else "true",
        "card_kind": card_kind,
        "card_payload": json.dumps(card_payload),
        "preferred_drawer_width_px": "580",
    }
    if is_terminal:
        metadata["is_terminal"] = "true"

    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[
            TextContent(type="text", text=narration),
            MetadataContent(type="metadata", metadata=metadata),
        ],
    )

def text_message(text: str) -> Any:
    """Builds a standard text-only ChatMessage."""
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )


# ──────────────────────────────────────────────────────────────────────────────
# Selection Parsing: Handles both Direct @mention JSON and Planner-Mediated Prose
# ──────────────────────────────────────────────────────────────────────────────

def parse_incoming_selection(text: str) -> Dict[str, Any]:
    """
    Parses user selection from ASI:One chat.
    ASI:One delivers selections in two formats:
      1. Verbatim JSON (when chatting directly via @mention)
      2. Natural-language prose summary (when routed via ASI:One planner LLM)
    """
    cleaned = text.strip()
    # 1. Try parsing direct JSON
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # 2. Heuristic extraction for planner prose
    selection: Dict[str, Any] = {}
    lower_text = cleaned.lower()

    # Flight IDs
    for fl_id in ["fl_indigo_602", "fl_airindia_815", "fl_akasa_114"]:
        if fl_id.lower() in lower_text:
            selection["action"] = "pick_flight"
            selection["flight_id"] = fl_id
            break

    # Cabin class
    if "business" in lower_text:
        selection["cabin_class"] = "business"
    elif "economy" in lower_text:
        selection["cabin_class"] = "economy"

    # Hotel IDs
    for ht_id in ["ht_taj_exotica", "ht_w_goa", "ht_heritage_fontainhas"]:
        if ht_id.lower() in lower_text:
            selection["action"] = "pick_hotel"
            selection["hotel_id"] = ht_id
            break

    # Room tier
    if "deluxe" in lower_text or "villa" in lower_text:
        selection["room_tier"] = "deluxe"
    elif "standard" in lower_text or "suite" in lower_text:
        selection["room_tier"] = "standard"

    # Activity IDs
    for act_id in ["act_scuba_grand_island", "act_sunset_catamaran", "act_spice_plantation"]:
        if act_id.lower() in lower_text:
            selection["action"] = "pick_activity"
            selection["activity_id"] = act_id
            break

    # Form / Escrow actions
    if "confirm" in lower_text or "escrow" in lower_text or "authorize" in lower_text:
        selection["action"] = "execute_escrow_payment"
    elif "restart" in lower_text or "modify" in lower_text:
        selection["action"] = "restart_plan"

    return selection


# ──────────────────────────────────────────────────────────────────────────────
# Message Router & Conversational Flow State Machine
# ──────────────────────────────────────────────────────────────────────────────

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    """Primary ACP entrypoint for ASI:One conversations."""
    # 1. Send immediate ACP acknowledgment
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id,
        ),
    )

    # 2. Extract latest text content
    last_text = next(
        (c.text for c in msg.content if isinstance(c, TextContent)),
        "",
    ).strip()

    logger.info(f"Received message from {sender}: {last_text}")

    # 3. Retrieve or initialize user session in agent storage
    session: Dict[str, Any] = ctx.storage.get(sender) or {}

    # Initial greetings or trigger words
    is_initial_prompt = (
        not last_text
        or last_text.lower() in {"hi", "hello", "hey", "start", "plan", "goa", "trip", "voyage"}
        or "plan a trip" in last_text.lower()
        or "book" in last_text.lower()
    )

    if is_initial_prompt and not session.get("stage"):
        session = {"stage": "flights"}
        ctx.storage.set(sender, session)
        
        narration = (
            "🌴 **Welcome to VoyageAI!** I am your autonomous travel concierge orchestrator. "
            "I coordinate flight finders, luxury stay curators, and smart escrow agents on Fetch.ai.\n\n"
            "Here are the best live flight options for **New Delhi (DEL) → Goa (GOI)**. "
            "Please select a flight from the carousel below:"
        )
        await ctx.send(
            sender,
            card_message(narration, "carousel", build_flights_carousel("DEL", "GOI"))
        )
        return

    # Parse incoming interaction selection
    selection = parse_incoming_selection(last_text)
    action = selection.get("action")

    # ── Step 1: Flight Selected → Show Flight Detail (Cabin Class) ──────────────
    if action == "pick_flight" or "flight_id" in selection:
        flight_id = selection.get("flight_id", "fl_indigo_602")
        flight_data = get_flight_by_id(flight_id)
        
        session["flight_id"] = flight_id
        session["flight_name"] = flight_data["airline"]
        session["flight_price"] = flight_data["economy_price"]
        session["stage"] = "flight_detail"
        ctx.storage.set(sender, session)

        narration = (
            f"✈️ Excellent choice! You picked **{flight_data['airline']}**.\n"
            "Review flight timings and select your preferred cabin class:"
        )
        await ctx.send(
            sender,
            card_message(narration, "detail", build_flight_detail(flight_id))
        )
        return

    # ── Step 2: Cabin Selected → Show Hotel Carousel ────────────────────────────
    if action == "pick_cabin" or selection.get("cabin_class"):
        cabin = selection.get("cabin_class", "economy")
        session["cabin_class"] = cabin
        
        # Adjust flight price if business selected
        flight_data = get_flight_by_id(session.get("flight_id", "fl_indigo_602"))
        if cabin == "business":
            session["flight_price"] = flight_data["business_price"]
        else:
            session["flight_price"] = flight_data["economy_price"]

        session["stage"] = "hotels"
        ctx.storage.set(sender, session)

        narration = (
            f"✅ **{cabin.title()} Class** locked in.\n\n"
            "Now let's choose your accommodation. My **Stay Discovery Agent** has scouted "
            "these top-rated luxury resorts and villas in Goa:"
        )
        await ctx.send(
            sender,
            card_message(narration, "carousel", build_hotels_carousel("Goa"))
        )
        return

    # ── Step 3: Hotel Selected → Show Hotel Detail (Room Tiers) ─────────────────
    if action == "pick_hotel" or "hotel_id" in selection:
        hotel_id = selection.get("hotel_id", "ht_w_goa")
        hotel_data = get_hotel_by_id(hotel_id)

        session["hotel_id"] = hotel_id
        session["hotel_name"] = hotel_data["name"]
        session["hotel_price"] = hotel_data["standard_room_price"]
        session["nights"] = 2
        session["stage"] = "hotel_detail"
        ctx.storage.set(sender, session)

        narration = (
            f"🏨 You selected **{hotel_data['name']}** in {hotel_data['location']}.\n"
            "Review resort amenities and choose your room tier:"
        )
        await ctx.send(
            sender,
            card_message(narration, "detail", build_hotel_detail(hotel_id))
        )
        return

    # ── Step 4: Room Tier Confirmed → Show Activities Carousel ──────────────────
    if action == "confirm_hotel_tier" or selection.get("room_tier"):
        room_tier = selection.get("room_tier", "standard")
        session["room_tier"] = room_tier

        hotel_data = get_hotel_by_id(session.get("hotel_id", "ht_w_goa"))
        if room_tier == "deluxe":
            session["hotel_price"] = hotel_data["deluxe_villa_price"]
        else:
            session["hotel_price"] = hotel_data["standard_room_price"]

        session["stage"] = "activities"
        ctx.storage.set(sender, session)

        narration = (
            f"🌴 **{room_tier.title()} Room** selected.\n\n"
            "Next, my **Experience Curator Agent** recommends these exclusive local adventures. "
            "Pick an experience to add to your itinerary:"
        )
        await ctx.send(
            sender,
            card_message(narration, "carousel", build_activities_carousel())
        )
        return

    # ── Step 5: Activity Selected → Show Traveler Details Form ──────────────────
    if action == "pick_activity" or "activity_id" in selection:
        activity_id = selection.get("activity_id", "act_scuba_grand_island")
        activity_data = get_activity_by_id(activity_id)

        session["activity_id"] = activity_id
        session["activity_name"] = activity_data["name"]
        session["activity_price"] = activity_data["price_per_person"]
        session["stage"] = "traveler_form"
        ctx.storage.set(sender, session)

        narration = (
            f"🤿 Added **{activity_data['name']}** to your package!\n\n"
            "Please fill in your primary traveler contact information to prepare the booking vouchers:"
        )
        await ctx.send(
            sender,
            card_message(narration, "form", build_traveler_form(session))
        )
        return

    # ── Step 6: Traveler Form Submitted → Show Review & Escrow Card ─────────────
    if action == "submit_traveler_form" or "full_name" in selection:
        session["full_name"] = selection.get("full_name", session.get("full_name", "Rahul Sharma"))
        session["email"] = selection.get("email", session.get("email", "rahul@example.com"))
        session["phone"] = selection.get("phone", session.get("phone", "+91 98765 43210"))
        session["stage"] = "review"
        ctx.storage.set(sender, session)

        narration = (
            "📋 **Package Itinerary Complete!**\n\n"
            "Review your comprehensive travel summary below. Payments are protected via "
            "**Fetch.ai Smart Escrow Protocol** — funds are locked and only released upon verified check-in:"
        )
        await ctx.send(
            sender,
            card_message(narration, "review", build_review_card(session))
        )
        return

    # ── Step 7: Escrow Payment Execution & Confirmation ─────────────────────────
    if action == "execute_escrow_payment":
        totals = calculate_trip_totals(session)
        trip_id = totals["trip_id"]
        tx_hash = f"0x{uuid4().hex[:16]}...{uuid4().hex[:8]}"

        # Clear session for fresh bookings
        ctx.storage.set(sender, {})

        confirmation_text = (
            f"🎉 **BOOKING CONFIRMED & ESCROW LOCKED!**\n\n"
            f"• **Trip Reference:** `{trip_id}`\n"
            f"• **Lead Passenger:** {session.get('full_name', 'Rahul Sharma')}\n"
            f"• **Flight:** {session.get('flight_name', 'IndiGo 6E-602')} (PNR: `6E-VYG99`)\n"
            f"• **Resort:** {session.get('hotel_name', 'W Goa')} ({session.get('nights', 2)} Nights)\n"
            f"• **Experience:** {session.get('activity_name', 'Scuba Diving Safari')}\n"
            f"• **Escrow Settled:** **{totals['fet_tokens']} FET** (₹{totals['grand_total_inr']:,})\n"
            f"• **Fetch Ledger Tx:** `{tx_hash}`\n\n"
            f"🛡️ *Protected by Fetch.ai Payment Protocol. E-tickets sent to {session.get('email', 'guest@email.com')}.*\n\n"
            "Type **'plan'** anytime to organize your next adventure!"
        )
        await ctx.send(sender, text_message(confirmation_text))
        return

    # ── Reset / Fallback ────────────────────────────────────────────────────────
    if action == "restart_plan":
        ctx.storage.set(sender, {})
        await ctx.send(
            sender,
            text_message("🔄 Trip session reset. Type **'start'** or **'plan a trip'** to begin again!")
        )
        return

    # Default fallback guide
    await ctx.send(
        sender,
        text_message(
            "👋 Welcome! I am **VoyageAI**, your Autonomous Travel Concierge. "
            "Type **'plan a trip to Goa'** to browse flights, luxury stays, and curated experiences!"
        )
    )


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handles incoming message acknowledgments from ASI:One."""
    logger.debug(f"Received ACP acknowledgment for message {msg.acknowledged_msg_id} from {sender}")


# Attach protocol to agent
agent.include(chat_proto)

if __name__ == "__main__":
    logger.info(f"🚀 Starting VoyageAI Concierge Agent on port {PORT}...")
    logger.info(f"Agent address: {agent.address}")
    agent.run()
