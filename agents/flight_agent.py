import json
import os
from typing import Dict, Any, List

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "mock_data", "flights.json")

def load_flights() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_flight_by_id(flight_id: str) -> Dict[str, Any]:
    flights = load_flights()
    for fl in flights:
        if fl["id"] == flight_id:
            return fl
    return flights[0]

def build_flights_carousel(origin: str = "DEL", destination: str = "GOI") -> Dict[str, Any]:
    """Generates an ASI:One Carousel card payload for available flights."""
    flights = load_flights()
    items = []
    for fl in flights:
        items.append({
            "id": fl["id"],
            "image": fl["logo"],
            "title": fl["airline"],
            "subtitle": f"{fl['departure_time']} - {fl['arrival_time']} · {fl['duration']}",
            "badges": [{"label": fl["badge"], "variant": fl["badge_variant"]}],
            "secondary_text": f"₹{fl['economy_price']:,}",
            "primary_cta": {
                "label": "Select Flight",
                "selection": {
                    "action": "pick_flight",
                    "flight_id": fl["id"],
                    "airline": fl["airline"]
                }
            }
        })
    
    return {
        "title": "Select Outbound Flight",
        "subtitle": f"{origin} ✈️ {destination} · Direct Options",
        "items": items
    }

def build_flight_detail(flight_id: str) -> Dict[str, Any]:
    """Generates an ASI:One Detail card payload with cabin selection radio options."""
    fl = get_flight_by_id(flight_id)
    return {
        "title": f"{fl['airline']} · Flight Details",
        "hero_image": fl["logo"],
        "summary_rows": [
            {"label": "Route", "value": f"{fl['origin']} → {fl['destination']}"},
            {"label": "Departure", "value": fl["departure_time"]},
            {"label": "Arrival", "value": fl["arrival_time"]},
            {"label": "Duration", "value": fl["duration"]},
            {"label": "Stops", "value": fl["stops"]},
            {"label": "CO₂ Offset", "value": fl["co2_emissions"]}
        ],
        "sub_options": {
            "name": "cabin_class",
            "kind": "radio",
            "label": "Select Cabin Class",
            "choices": [
                {
                    "value": "economy",
                    "label": "Economy Class",
                    "secondary_text": f"₹{fl['economy_price']:,} (Standard 15kg baggage)"
                },
                {
                    "value": "business",
                    "label": "Business Class",
                    "secondary_text": f"₹{fl['business_price']:,} (Priority boarding + Lounge access)"
                }
            ]
        },
        "ctas": [
            {
                "label": "Confirm Cabin & Proceed",
                "primary": True,
                "selection": {
                    "action": "pick_cabin",
                    "flight_id": fl["id"]
                }
            },
            {
                "label": "Change Flight",
                "selection": {
                    "action": "view_flights"
                }
            }
        ]
    }
