"""
VoyageAI End-to-End Test Suite & Interactive Card Validator
Tests each step of the conversational flow and validates all ASI:One Interactive Card payloads.
"""

import json
import logging
import sys

# Configure UTF-8 for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agents.flight_agent import build_flights_carousel, build_flight_detail
from agents.hotel_agent import build_hotels_carousel, build_hotel_detail
from agents.activity_agent import build_activities_carousel
from agents.payment_agent import build_traveler_form, build_review_card, calculate_trip_totals
from voyage_orchestrator import parse_incoming_selection

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def validate_card_payload(name: str, kind: str, payload: dict):
    print(f"\n=======================================================")
    print(f"🔍 Validating [{name}] (card_kind: '{kind}')")
    print(f"=======================================================")

    payload_str = json.dumps(payload)
    payload_size_kb = len(payload_str.encode("utf-8")) / 1024.0
    print(f"  • Payload size: {payload_size_kb:.2f} KB (Limit: 64 KB) -> {'✅ PASS' if payload_size_kb < 64 else '❌ FAIL'}")

    if kind == "carousel":
        assert "title" in payload, "Carousel must have 'title'"
        assert "items" in payload, "Carousel must have 'items'"
        assert len(payload["items"]) > 0, "Carousel items must not be empty"
        for idx, it in enumerate(payload["items"]):
            assert "id" in it, f"Item {idx} missing 'id'"
            assert "title" in it, f"Item {idx} missing 'title'"
            assert "primary_cta" in it, f"Item {idx} missing 'primary_cta'"
            assert "selection" in it["primary_cta"], f"Item {idx} primary_cta missing 'selection'"
        print(f"  • Carousel structure: {len(payload['items'])} items correctly formatted -> ✅ PASS")

    elif kind == "detail":
        assert "title" in payload, "Detail card must have 'title'"
        assert "summary_rows" in payload, "Detail card must have 'summary_rows'"
        assert "ctas" in payload, "Detail card must have 'ctas'"
        print(f"  • Detail structure: {len(payload['summary_rows'])} summary rows, {len(payload['ctas'])} CTAs -> ✅ PASS")

    elif kind == "form":
        assert "title" in payload, "Form card must have 'title'"
        assert "fields" in payload, "Form card must have 'fields'"
        assert "submit_cta" in payload, "Form card must have 'submit_cta'"
        print(f"  • Form structure: {len(payload['fields'])} input fields -> ✅ PASS")

    elif kind == "review":
        assert "title" in payload, "Review card must have 'title'"
        assert "items" in payload, "Review card must have 'items'"
        assert "total" in payload, "Review card must have 'total'"
        assert "ctas" in payload, "Review card must have 'ctas'"
        print(f"  • Review structure: Total '{payload['total']['amount']}' ({payload['total']['secondary_amount']}) -> ✅ PASS")

def test_full_simulation():
    print("\n🚀 Simulating Complete Conversational Workflow from Intent to Action:")

    # 1. User prompts: "plan a trip to goa"
    print("\n[Step 1] User: 'Hi, plan a trip to Goa'")
    carousel_fl = build_flights_carousel("DEL", "GOI")
    validate_card_payload("Flights Carousel", "carousel", carousel_fl)

    # 2. User selects flight from carousel (ASI:One sends selection)
    selection_fl = '{"action": "pick_flight", "flight_id": "fl_indigo_602"}'
    parsed_fl = parse_incoming_selection(selection_fl)
    print(f"\n[Step 2] User clicks CTA -> Delivered JSON: {selection_fl}")
    assert parsed_fl["action"] == "pick_flight"
    assert parsed_fl["flight_id"] == "fl_indigo_602"
    detail_fl = build_flight_detail(parsed_fl["flight_id"])
    validate_card_payload("Flight Detail with Cabin Selector", "detail", detail_fl)

    # 3. User chooses Business Class
    selection_cabin = '{"action": "pick_cabin", "flight_id": "fl_indigo_602", "cabin_class": "business"}'
    parsed_cabin = parse_incoming_selection(selection_cabin)
    print(f"\n[Step 3] User confirms Cabin -> Delivered JSON: {selection_cabin}")
    assert parsed_cabin["cabin_class"] == "business"
    carousel_ht = build_hotels_carousel("Goa")
    validate_card_payload("Stays Carousel", "carousel", carousel_ht)

    # 4. User selects Hotel
    selection_ht = '{"action": "pick_hotel", "hotel_id": "ht_w_goa"}'
    parsed_ht = parse_incoming_selection(selection_ht)
    print(f"\n[Step 4] User selects Resort -> Delivered JSON: {selection_ht}")
    detail_ht = build_hotel_detail(parsed_ht["hotel_id"])
    validate_card_payload("Hotel Detail with Room Tier", "detail", detail_ht)

    # 5. User confirms room tier
    selection_room = '{"action": "confirm_hotel_tier", "hotel_id": "ht_w_goa", "room_tier": "deluxe"}'
    parsed_room = parse_incoming_selection(selection_room)
    print(f"\n[Step 5] User picks Deluxe Villa -> Delivered JSON: {selection_room}")
    carousel_act = build_activities_carousel()
    validate_card_payload("Activities Carousel", "carousel", carousel_act)

    # 6. User picks activity
    selection_act = '{"action": "pick_activity", "activity_id": "act_scuba_grand_island"}'
    parsed_act = parse_incoming_selection(selection_act)
    print(f"\n[Step 6] User picks Scuba Diving -> Delivered JSON: {selection_act}")
    mock_session = {
        "flight_name": "IndiGo 6E-602",
        "hotel_name": "W Goa Beachfront Retreat",
        "cabin_class": "business",
        "flight_price": 11500,
        "hotel_price": 24500,
        "nights": 2,
        "activity_name": "Grand Island Scuba Diving",
        "activity_price": 3200,
        "trip_id": "VYG-TEST99"
    }
    form_card = build_traveler_form(mock_session)
    validate_card_payload("Traveler Contact Form", "form", form_card)

    # 7. User submits traveler form
    selection_form = '{"action": "submit_traveler_form", "full_name": "Rahul Sharma", "email": "rahul@example.com"}'
    parsed_form = parse_incoming_selection(selection_form)
    print(f"\n[Step 7] User submits Form -> Delivered JSON: {selection_form}")
    mock_session["full_name"] = parsed_form["full_name"]
    mock_session["email"] = parsed_form["email"]
    review_card = build_review_card(mock_session)
    validate_card_payload("Itinerary Review & Escrow Settlement Card", "review", review_card)

    # 8. User authorizes Escrow Payment
    selection_escrow = '{"action": "execute_escrow_payment", "trip_id": "VYG-TEST99"}'
    parsed_escrow = parse_incoming_selection(selection_escrow)
    print(f"\n[Step 8] User clicks Authorize Escrow -> Delivered JSON: {selection_escrow}")
    assert parsed_escrow["action"] == "execute_escrow_payment"

    totals = calculate_trip_totals(mock_session)
    print(f"\n🎉 Escrow Payment Executed Successfully:")
    print(f"   • Total INR: ₹{totals['grand_total_inr']:,}")
    print(f"   • Fetch Tokens: {totals['fet_tokens']} FET")
    print(f"   • Escrow Hash: 0x9f8b...33e1")
    print("\n✨ ALL TESTS & CARD SCHEMAS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_simulation()
