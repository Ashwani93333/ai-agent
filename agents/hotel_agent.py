import json
import os
from typing import Dict, Any, List

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "mock_data", "hotels.json")

def load_hotels() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_hotel_by_id(hotel_id: str) -> Dict[str, Any]:
    hotels = load_hotels()
    for ht in hotels:
        if ht["id"] == hotel_id:
            return ht
    return hotels[0]

def build_hotels_carousel(destination: str = "Goa") -> Dict[str, Any]:
    """Generates an ASI:One Carousel card payload for curated hotel stays."""
    hotels = load_hotels()
    items = []
    for ht in hotels:
        items.append({
            "id": ht["id"],
            "image": ht["hero_image"],
            "title": ht["name"],
            "subtitle": f"{ht['location']} · {ht['rating']}",
            "badges": ht.get("badges", [{"label": "Verified Stay", "variant": "info"}]),
            "secondary_text": f"₹{ht['standard_room_price']:,} / night",
            "primary_cta": {
                "label": "View Resort",
                "selection": {
                    "action": "pick_hotel",
                    "hotel_id": ht["id"],
                    "hotel_name": ht["name"]
                }
            }
        })
    
    return {
        "title": f"Curated Stays in {destination}",
        "subtitle": "Beachfront resorts, luxury villas & heritage estates",
        "items": items
    }

def build_hotel_detail(hotel_id: str) -> Dict[str, Any]:
    """Generates an ASI:One Detail card payload with room tier options."""
    ht = get_hotel_by_id(hotel_id)
    return {
        "title": ht["name"],
        "hero_image": ht["hero_image"],
        "summary_rows": [
            {"label": "Location", "value": ht["location"]},
            {"label": "Rating", "value": ht["rating"]},
            {"label": "Amenities", "value": ", ".join(ht["amenities"][:3])},
            {"label": "Check-in / Out", "value": f"{ht['check_in']} / {ht['check_out']}"}
        ],
        "sub_options": {
            "name": "room_tier",
            "kind": "radio",
            "label": "Choose Room Category",
            "choices": [
                {
                    "value": "standard",
                    "label": "Standard Ocean View Suite",
                    "secondary_text": f"₹{ht['standard_room_price']:,} / night (Breakfast included)"
                },
                {
                    "value": "deluxe",
                    "label": "Deluxe Private Plunge Pool Villa",
                    "secondary_text": f"₹{ht['deluxe_villa_price']:,} / night (Butler service + Spa credits)"
                }
            ]
        },
        "ctas": [
            {
                "label": "Select Room & Add Experiences",
                "primary": True,
                "selection": {
                    "action": "confirm_hotel_tier",
                    "hotel_id": ht["id"]
                }
            },
            {
                "label": "Browse Other Stays",
                "selection": {
                    "action": "view_hotels"
                }
            }
        ]
    }
