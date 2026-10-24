import json
import os
from typing import Dict, Any, List

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "mock_data", "activities.json")

def load_activities() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_activity_by_id(act_id: str) -> Dict[str, Any]:
    activities = load_activities()
    for act in activities:
        if act["id"] == act_id:
            return act
    return activities[0]

def build_activities_carousel() -> Dict[str, Any]:
    """Generates an ASI:One Carousel card payload for curated experiences."""
    activities = load_activities()
    items = []
    for act in activities:
        items.append({
            "id": act["id"],
            "image": act["image"],
            "title": act["name"],
            "subtitle": f"{act['duration']} · {act['rating']}",
            "badges": act.get("badges", [{"label": "Popular", "variant": "info"}]),
            "secondary_text": f"₹{act['price_per_person']:,} / person",
            "primary_cta": {
                "label": "Add to Itinerary",
                "selection": {
                    "action": "pick_activity",
                    "activity_id": act["id"],
                    "activity_name": act["name"]
                }
            }
        })
    
    return {
        "title": "Exclusive Curated Experiences",
        "subtitle": "Elevate your journey with handpicked local adventures",
        "items": items
    }
