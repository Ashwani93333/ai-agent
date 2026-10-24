import uuid
from typing import Dict, Any, List

def build_traveler_form(session: Dict[str, Any]) -> Dict[str, Any]:
    """Generates an ASI:One Form card payload to capture traveler/guest contact details."""
    flight_name = session.get("flight_name", "Selected Flight")
    hotel_name = session.get("hotel_name", "Selected Hotel")
    
    return {
        "title": "Traveler & Contact Information",
        "subtitle": f"Reserving for {flight_name} + {hotel_name}",
        "fields": [
            {
                "name": "full_name",
                "label": "Lead Passenger Full Name",
                "type": "text",
                "required": True,
                "placeholder": "e.g. Rahul Sharma"
            },
            {
                "name": "email",
                "label": "Email Address (for e-tickets & vouchers)",
                "type": "email",
                "required": True,
                "placeholder": "rahul.sharma@example.com"
            },
            {
                "name": "phone",
                "label": "Phone Number",
                "type": "tel",
                "required": True,
                "placeholder": "+91 98765 43210"
            },
            {
                "name": "special_requests",
                "label": "Special Requests (Dietary, Airport Transfer)",
                "type": "text",
                "required": False,
                "placeholder": "Window seat, late airport check-in..."
            }
        ],
        "submit_cta": {
            "label": "Generate Final Itinerary & Review",
            "selection": {
                "action": "submit_traveler_form"
            }
        }
    }

def calculate_trip_totals(session: Dict[str, Any]) -> Dict[str, Any]:
    """Calculates all line items, taxes, and crypto/FET conversion."""
    flight_price = session.get("flight_price", 5400)
    hotel_price_per_night = session.get("hotel_price", 12800)
    nights = session.get("nights", 2)
    hotel_total = hotel_price_per_night * nights
    activity_price = session.get("activity_price", 3200)

    subtotal = flight_price + hotel_total + activity_price
    tax = int(subtotal * 0.12)
    grand_total_inr = subtotal + tax
    
    # 1 FET ≈ 85 INR (for demonstration conversion)
    fet_tokens = round(grand_total_inr / 85.0, 2)
    
    trip_id = session.get("trip_id", f"VYG-{uuid.uuid4().hex[:6].upper()}")
    session["trip_id"] = trip_id

    items = [
        {
            "label": f"Flight: {session.get('flight_name', 'IndiGo 6E-602')} ({session.get('cabin_class', 'Economy').title()})",
            "amount": f"₹{flight_price:,}"
        },
        {
            "label": f"Stay: {session.get('hotel_name', 'W Goa')} ({nights} Nights, {session.get('room_tier', 'Standard').title()})",
            "amount": f"₹{hotel_total:,}"
        },
        {
            "label": f"Experience: {session.get('activity_name', 'Grand Island Scuba')}",
            "amount": f"₹{activity_price:,}"
        },
        {
            "label": "Taxes, Insurance & Surcharges (12% GST)",
            "amount": f"₹{tax:,}"
        }
    ]

    return {
        "trip_id": trip_id,
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "grand_total_inr": grand_total_inr,
        "fet_tokens": fet_tokens
    }

def build_review_card(session: Dict[str, Any]) -> Dict[str, Any]:
    """Generates an ASI:One Review card payload with Fetch.ai Escrow payment settlement."""
    totals = calculate_trip_totals(session)
    traveler_name = session.get("full_name", "Rahul Sharma")
    trip_id = totals["trip_id"]

    return {
        "title": "Itinerary Review & Escrow Authorization",
        "subtitle": f"Trip #{trip_id} · Lead Traveler: {traveler_name}",
        "items": totals["items"],
        "total": {
            "label": "Total Amount (Protected by Escrow)",
            "amount": f"₹{totals['grand_total_inr']:,}",
            "secondary_amount": f"{totals['fet_tokens']} FET"
        },
        "ctas": [
            {
                "label": f"Confirm & Lock Escrow ({totals['fet_tokens']} FET)",
                "primary": True,
                "selection": {
                    "action": "execute_escrow_payment",
                    "trip_id": trip_id,
                    "amount_fet": totals["fet_tokens"]
                }
            },
            {
                "label": "Customize Plan",
                "selection": {
                    "action": "restart_plan"
                }
            }
        ]
    }
