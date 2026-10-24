"""
🌴 VoyageAI Concierge — Hosted Agentverse Cloud Edition
Copy-paste this file directly into the Agentverse Web Code Editor (https://agentverse.ai/)
No local computer, ngrok, or localtunnel required. Runs 24/7 on Fetch.ai cloud.
"""

import json
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, Any

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    MetadataContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# ──────────────────────────────────────────────────────────────────────────────
# 1. Mock Datasets (Embedded for standalone cloud execution)
# ──────────────────────────────────────────────────────────────────────────────

FLIGHTS = [
    {
        "id": "fl_indigo_602",
        "airline": "IndiGo 6E-602",
        "logo": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=128&auto=format&fit=crop&q=80",
        "origin": "New Delhi (DEL)",
        "destination": "Goa Dabolim (GOI)",
        "departure_time": "06:15 AM",
        "arrival_time": "08:50 AM",
        "duration": "2h 35m",
        "stops": "Non-stop",
        "badge": "Fastest",
        "badge_variant": "info",
        "economy_price": 5400,
        "business_price": 11500,
        "co2": "112 kg"
    },
    {
        "id": "fl_airindia_815",
        "airline": "Air India AI-815",
        "logo": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=128&auto=format&fit=crop&q=80",
        "origin": "New Delhi (DEL)",
        "destination": "Goa Mopa (GOX)",
        "departure_time": "09:40 AM",
        "arrival_time": "12:15 PM",
        "duration": "2h 35m",
        "stops": "Non-stop",
        "badge": "Top Rated",
        "badge_variant": "success",
        "economy_price": 6100,
        "business_price": 14200,
        "co2": "108 kg"
    },
    {
        "id": "fl_akasa_114",
        "airline": "Akasa Air QP-114",
        "logo": "https://images.unsplash.com/photo-1569154941061-e231b4725ef1?w=128&auto=format&fit=crop&q=80",
        "origin": "New Delhi (DEL)",
        "destination": "Goa Dabolim (GOI)",
        "departure_time": "17:30 PM",
        "arrival_time": "20:10 PM",
        "duration": "2h 40m",
        "stops": "Non-stop",
        "badge": "Best Value",
        "badge_variant": "success",
        "economy_price": 4850,
        "business_price": 9900,
        "co2": "98 kg"
    }
]

HOTELS = [
    {
        "id": "ht_taj_exotica",
        "name": "Taj Exotica Resort & Spa, Benaulim",
        "location": "South Goa",
        "rating": "4.9 ★",
        "hero_image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=720&auto=format&fit=crop&q=80",
        "standard_price": 14500,
        "deluxe_price": 28000,
        "amenities": ["Private Beach", "Infinity Pool", "Ayurvedic Spa"]
    },
    {
        "id": "ht_w_goa",
        "name": "W Goa Beachfront Retreat, Vagator",
        "location": "North Goa",
        "rating": "4.8 ★",
        "hero_image": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=720&auto=format&fit=crop&q=80",
        "standard_price": 12800,
        "deluxe_price": 24500,
        "amenities": ["Rock Pool", "Direct Beach Access", "Live DJ Lounge"]
    },
    {
        "id": "ht_heritage_fontainhas",
        "name": "Heritage Latin Quarter Villa, Panaji",
        "location": "Central Goa",
        "rating": "4.7 ★",
        "hero_image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=720&auto=format&fit=crop&q=80",
        "standard_price": 6200,
        "deluxe_price": 11000,
        "amenities": ["Portuguese Architecture", "Artisan Cafe", "Walk to Historic Sites"]
    }
]

ACTIVITIES = [
    {
        "id": "act_scuba_grand_island",
        "name": "Grand Island Scuba Diving & Dolphin Safari",
        "duration": "5 hours (Morning)",
        "rating": "4.9 ★",
        "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=720&auto=format&fit=crop&q=80",
        "price": 3200
    },
    {
        "id": "act_sunset_catamaran",
        "name": "Mandovi Luxury Sunset Catamaran Cruise",
        "duration": "2.5 hours (Evening)",
        "rating": "4.8 ★",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=720&auto=format&fit=crop&q=80",
        "price": 2100
    },
    {
        "id": "act_spice_plantation",
        "name": "Sahakari Spice Plantation & Heritage Feast",
        "duration": "3 hours (Afternoon)",
        "rating": "4.7 ★",
        "image": "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=720&auto=format&fit=crop&q=80",
        "price": 1400
    }
]


# ──────────────────────────────────────────────────────────────────────────────
# 2. ASI:One Interactive Card Builders
# ──────────────────────────────────────────────────────────────────────────────

def card_message(narration: str, card_kind: str, card_payload: Dict[str, Any]) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[
            TextContent(type="text", text=narration),
            MetadataContent(
                type="metadata",
                metadata={
                    "card_protocol_version": "1",
                    "requires_card_interaction": "true",
                    "card_kind": card_kind,
                    "card_payload": json.dumps(card_payload),
                    "preferred_drawer_width_px": "580",
                },
            ),
        ],
    )

def build_flights_carousel():
    items = []
    for fl in FLIGHTS:
        items.append({
            "id": fl["id"],
            "image": fl["logo"],
            "title": fl["airline"],
            "subtitle": f"{fl['departure_time']} - {fl['arrival_time']} · {fl['duration']}",
            "badges": [{"label": fl["badge"], "variant": fl["badge_variant"]}],
            "secondary_text": f"₹{fl['economy_price']:,}",
            "primary_cta": {
                "label": "Select Flight",
                "selection": {"action": "pick_flight", "flight_id": fl["id"]}
            }
        })
    return {"title": "Select Outbound Flight", "subtitle": "New Delhi (DEL) ✈️ Goa · Direct Routes", "items": items}

def build_flight_detail(flight_id: str):
    fl = next((f for f in FLIGHTS if f["id"] == flight_id), FLIGHTS[0])
    return {
        "title": f"{fl['airline']} · Flight Details",
        "hero_image": fl["logo"],
        "summary_rows": [
            {"label": "Route", "value": f"{fl['origin']} → {fl['destination']}"},
            {"label": "Departure", "value": fl["departure_time"]},
            {"label": "Duration", "value": fl["duration"]},
            {"label": "CO₂ Offset", "value": fl["co2"]}
        ],
        "sub_options": {
            "name": "cabin_class",
            "kind": "radio",
            "label": "Select Cabin Class",
            "choices": [
                {"value": "economy", "label": "Economy Class", "secondary_text": f"₹{fl['economy_price']:,}"},
                {"value": "business", "label": "Business Class", "secondary_text": f"₹{fl['business_price']:,}"}
            ]
        },
        "ctas": [
            {"label": "Confirm Cabin & Pick Stay", "primary": True, "selection": {"action": "pick_cabin", "flight_id": fl["id"]}}
        ]
    }

def build_hotels_carousel():
    items = []
    for ht in HOTELS:
        items.append({
            "id": ht["id"],
            "image": ht["hero_image"],
            "title": ht["name"],
            "subtitle": f"{ht['location']} · {ht['rating']}",
            "badges": [{"label": "Verified Luxury", "variant": "info"}],
            "secondary_text": f"₹{ht['standard_price']:,} / night",
            "primary_cta": {
                "label": "Select Resort",
                "selection": {"action": "pick_hotel", "hotel_id": ht["id"]}
            }
        })
    return {"title": "Curated Stays in Goa", "subtitle": "Beachfront resorts & private pool villas", "items": items}

def build_hotel_detail(hotel_id: str):
    ht = next((h for h in HOTELS if h["id"] == hotel_id), HOTELS[0])
    return {
        "title": ht["name"],
        "hero_image": ht["hero_image"],
        "summary_rows": [
            {"label": "Location", "value": ht["location"]},
            {"label": "Rating", "value": ht["rating"]},
            {"label": "Amenities", "value": ", ".join(ht["amenities"])}
        ],
        "sub_options": {
            "name": "room_tier",
            "kind": "radio",
            "label": "Select Room Category",
            "choices": [
                {"value": "standard", "label": "Standard Ocean View Suite", "secondary_text": f"₹{ht['standard_price']:,} / night"},
                {"value": "deluxe", "label": "Deluxe Private Pool Villa", "secondary_text": f"₹{ht['deluxe_price']:,} / night"}
            ]
        },
        "ctas": [
            {"label": "Confirm Room & Add Activity", "primary": True, "selection": {"action": "confirm_hotel_tier", "hotel_id": ht["id"]}}
        ]
    }

def build_activities_carousel():
    items = []
    for act in ACTIVITIES:
        items.append({
            "id": act["id"],
            "image": act["image"],
            "title": act["name"],
            "subtitle": f"{act['duration']} · {act['rating']}",
            "badges": [{"label": "Popular", "variant": "success"}],
            "secondary_text": f"₹{act['price']:,} / person",
            "primary_cta": {
                "label": "Add Activity",
                "selection": {"action": "pick_activity", "activity_id": act["id"]}
            }
        })
    return {"title": "Exclusive Curated Experiences", "subtitle": "Handpicked Goan adventures", "items": items}

def build_traveler_form():
    return {
        "title": "Lead Traveler Details",
        "subtitle": "Used for flight e-tickets and resort check-in vouchers",
        "fields": [
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True, "placeholder": "Rahul Sharma"},
            {"name": "email", "label": "Email Address", "type": "email", "required": True, "placeholder": "rahul@example.com"},
            {"name": "phone", "label": "Phone Number", "type": "tel", "required": True, "placeholder": "+91 98765 43210"}
        ],
        "submit_cta": {
            "label": "Review Package & Escrow",
            "selection": {"action": "submit_traveler_form"}
        }
    }

def build_review_card(session: Dict[str, Any]):
    flight_price = session.get("flight_price", 5400)
    hotel_price = session.get("hotel_price", 12800) * 2  # 2 nights
    activity_price = session.get("activity_price", 3200)
    subtotal = flight_price + hotel_price + activity_price
    tax = int(subtotal * 0.12)
    grand_total = subtotal + tax
    fet_tokens = round(grand_total / 85.0, 2)
    trip_id = session.get("trip_id", f"VYG-{uuid4().hex[:6].upper()}")

    return {
        "title": "Itinerary Review & Escrow Settlement",
        "subtitle": f"Trip #{trip_id} · Lead: {session.get('full_name', 'Rahul Sharma')}",
        "items": [
            {"label": f"Flight: {session.get('flight_name', 'IndiGo 6E-602')}", "amount": f"₹{flight_price:,}"},
            {"label": f"Stay: {session.get('hotel_name', 'W Goa')} (2 Nights)", "amount": f"₹{hotel_price:,}"},
            {"label": f"Activity: {session.get('activity_name', 'Scuba Safari')}", "amount": f"₹{activity_price:,}"},
            {"label": "Taxes & Service Fees (12% GST)", "amount": f"₹{tax:,}"}
        ],
        "total": {
            "label": "Total Package (Protected by Fetch Escrow)",
            "amount": f"₹{grand_total:,}",
            "secondary_amount": f"{fet_tokens} FET"
        },
        "ctas": [
            {
                "label": f"Authorize Escrow Deposit ({fet_tokens} FET)",
                "primary": True,
                "selection": {"action": "execute_escrow", "fet": fet_tokens, "total": grand_total}
            }
        ]
    }


# ──────────────────────────────────────────────────────────────────────────────
# 3. Cloud Agent Setup & Chat Protocol Handlers
# ──────────────────────────────────────────────────────────────────────────────

agent = Agent()
chat_proto = Protocol(spec=chat_protocol_spec)

def parse_selection(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text.strip())
    except Exception:
        pass
    lower = text.lower()
    for fl in ["fl_indigo_602", "fl_airindia_815", "fl_akasa_114"]:
        if fl in lower:
            return {"action": "pick_flight", "flight_id": fl}
    if "business" in lower:
        return {"action": "pick_cabin", "cabin_class": "business"}
    elif "economy" in lower:
        return {"action": "pick_cabin", "cabin_class": "economy"}
    for ht in ["ht_taj_exotica", "ht_w_goa", "ht_heritage_fontainhas"]:
        if ht in lower:
            return {"action": "pick_hotel", "hotel_id": ht}
    if "deluxe" in lower:
        return {"action": "confirm_hotel_tier", "room_tier": "deluxe"}
    elif "standard" in lower:
        return {"action": "confirm_hotel_tier", "room_tier": "standard"}
    for act in ["act_scuba_grand_island", "act_sunset_catamaran", "act_spice_plantation"]:
        if act in lower:
            return {"action": "pick_activity", "activity_id": act}
    if "confirm" in lower or "escrow" in lower or "authorize" in lower:
        return {"action": "execute_escrow"}
    return {}

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Acknowledge immediately
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.now(timezone.utc), acknowledged_msg_id=msg.msg_id))

    last_text = next((c.text for c in msg.content if isinstance(c, TextContent)), "").strip()
    session = ctx.storage.get(sender) or {}
    selection = parse_selection(last_text)
    action = selection.get("action")

    # Step 0: Initial prompt
    if not action and (not session.get("stage") or last_text.lower() in {"hi", "hello", "plan", "start", "goa", "trip"}):
        session["stage"] = "flights"
        ctx.storage.set(sender, session)
        narration = "🌴 **Welcome to VoyageAI!** Here are the best live flights for **Delhi (DEL) → Goa**. Select an option below:"
        await ctx.send(sender, card_message(narration, "carousel", build_flights_carousel()))
        return

    # Step 1: Pick Flight
    if action == "pick_flight":
        fl_id = selection.get("flight_id", "fl_indigo_602")
        fl = next((f for f in FLIGHTS if f["id"] == fl_id), FLIGHTS[0])
        session["flight_id"] = fl_id
        session["flight_name"] = fl["airline"]
        session["flight_price"] = fl["economy_price"]
        session["stage"] = "flight_detail"
        ctx.storage.set(sender, session)
        await ctx.send(sender, card_message(f"✈️ Selected **{fl['airline']}**. Choose cabin class:", "detail", build_flight_detail(fl_id)))
        return

    # Step 2: Pick Cabin
    if action == "pick_cabin":
        cabin = selection.get("cabin_class", "economy")
        session["cabin_class"] = cabin
        fl = next((f for f in FLIGHTS if f["id"] == session.get("flight_id")), FLIGHTS[0])
        session["flight_price"] = fl["business_price"] if cabin == "business" else fl["economy_price"]
        session["stage"] = "hotels"
        ctx.storage.set(sender, session)
        narration = f"✅ **{cabin.title()} Class** locked. Now choose a luxury stay in Goa:"
        await ctx.send(sender, card_message(narration, "carousel", build_hotels_carousel()))
        return

    # Step 3: Pick Hotel
    if action == "pick_hotel":
        ht_id = selection.get("hotel_id", "ht_w_goa")
        ht = next((h for h in HOTELS if h["id"] == ht_id), HOTELS[0])
        session["hotel_id"] = ht_id
        session["hotel_name"] = ht["name"]
        session["hotel_price"] = ht["standard_price"]
        session["stage"] = "hotel_detail"
        ctx.storage.set(sender, session)
        await ctx.send(sender, card_message(f"🏨 Selected **{ht['name']}**. Choose room category:", "detail", build_hotel_detail(ht_id)))
        return

    # Step 4: Confirm Room Tier
    if action == "confirm_hotel_tier":
        tier = selection.get("room_tier", "standard")
        ht = next((h for h in HOTELS if h["id"] == session.get("hotel_id")), HOTELS[0])
        session["hotel_price"] = ht["deluxe_price"] if tier == "deluxe" else ht["standard_price"]
        session["stage"] = "activities"
        ctx.storage.set(sender, session)
        narration = f"🌴 **{tier.title()} Room** confirmed. Add a curated local experience to your trip:"
        await ctx.send(sender, card_message(narration, "carousel", build_activities_carousel()))
        return

    # Step 5: Pick Activity
    if action == "pick_activity":
        act_id = selection.get("activity_id", "act_scuba_grand_island")
        act = next((a for a in ACTIVITIES if a["id"] == act_id), ACTIVITIES[0])
        session["activity_name"] = act["name"]
        session["activity_price"] = act["price"]
        session["stage"] = "traveler_form"
        ctx.storage.set(sender, session)
        narration = f"🤿 Added **{act['name']}**. Please enter lead traveler information:"
        await ctx.send(sender, card_message(narration, "form", build_traveler_form()))
        return

    # Step 6: Submit Form
    if action == "submit_traveler_form":
        session["full_name"] = selection.get("full_name", "Rahul Sharma")
        session["email"] = selection.get("email", "rahul@example.com")
        session["stage"] = "review"
        ctx.storage.set(sender, session)
        narration = "📋 **Package Summary Ready!** Payments are protected by Fetch.ai Smart Escrow Protocol:"
        await ctx.send(sender, card_message(narration, "review", build_review_card(session)))
        return

    # Step 7: Escrow Payment Execution
    if action == "execute_escrow":
        fet = selection.get("fet", 750.0)
        total = selection.get("total", 63750)
        fee = round(fet * 0.015, 2)
        vendor_allocation = round(fet - fee, 2)
        escrow_contract = f"fetch1escrow{uuid4().hex[:16]}"
        tx_hash = f"0x{uuid4().hex[:32]}"
        ctx.storage.set(sender, {})

        confirmed = (
            f"🎉 **BOOKING CONFIRMED & SMART ESCROW LOCKED!**\n\n"
            f"• **Lead Traveler:** {session.get('full_name', 'Rahul Sharma')}\n"
            f"• **Flight:** {session.get('flight_name', 'IndiGo 6E-602')}\n"
            f"• **Stay:** {session.get('hotel_name', 'W Goa')} (2 Nights)\n"
            f"• **Activity:** {session.get('activity_name', 'Scuba Safari')}\n\n"
            f"💳 **Fetch.ai Decentralized Payment Protocol Settlement:**\n"
            f"• **Escrow Total Locked:** **{fet} FET** (₹{total:,})\n"
            f"• **Smart Escrow Contract:** `{escrow_contract}`\n"
            f"• **Protocol Network Fee (1.5%):** `{fee} FET`\n"
            f"• **Vendor Allocation:** `{vendor_allocation} FET`\n"
            f"• **Ledger Tx Hash:** `{tx_hash}`\n\n"
            f"📋 **Milestone Escrow Release Schedule:**\n"
            f"  1. 50% released upon airport check-in verification.\n"
            f"  2. 50% released upon resort check-in verification.\n\n"
            f"🛡️ *Protected by Fetch.ai Payment Protocol. Vouchers sent to {session.get('email', 'guest@email.com')}.*"
        )
        await ctx.send(sender, ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=confirmed)]
        ))
        return

@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Delivered ACP ack to {sender}")

agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
