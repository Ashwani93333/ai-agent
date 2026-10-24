# 🌴 VoyageAI — Autonomous Travel & Experience Concierge
### ASI:One Agent Challenge (Fetch-A-Thon 3.0): From Intent to Action

[![Fetch.ai](https://img.shields.io/badge/Fetch.ai-uAgents-blue)](https://fetch.ai/)
[![Protocol](https://img.shields.io/badge/Protocol-ACP%20(Agent%20Chat%20Protocol)-purple)](https://innovationlab.fetch.ai/)
[![ASI:One Cards](https://img.shields.io/badge/UI-ASI%3AOne%20Interactive%20Cards-success)](https://asi1.ai/)
[![Python](https://img.shields.io/badge/Python-3.11+-brightgreen)](https://www.python.org/)

---

## 🎯 1. Overview & Problem Solved

### The Problem
Traditional online travel booking is fragmented and painful:
- Users bounce between 5–10 browser tabs comparing flights, resorts, and activities.
- Conversational AI chatbots only output plain text recommendations without executable outcomes.
- Travelers lack decentralized escrow protection for cross-vendor bookings.

### The Solution: VoyageAI
**VoyageAI** is a multi-agent travel concierge operating directly inside **[ASI:One](https://asi1.ai/)**. Powered by the **Agent Chat Protocol (ACP)** and **ASI1 Interactive Cards**, it converts a simple conversational prompt like:
> *"Plan a luxury weekend getaway to Goa with flights from Delhi, beachfront villa, and scuba diving."*

into an interactive, executable journey right inside the ASI:One conversation drawer without requiring a custom frontend.

### Target Users
- **Leisure Travelers & Digital Nomads**: Who want curated, multi-service travel packages booked in minutes.
- **Corporate & Event Travelers**: Seeking streamlined bookings with automated expense receipts.
- **Web3 / Crypto Users**: Who prefer trustless escrow deposits settled in **FET tokens**.

---

## 🏗️ 2. Multi-Agent Architecture

```
                                  [ ASI:One User ]
                                         │
                                         ▼ (ACP over WebSockets/HTTP)
                         ┌───────────────────────────────┐
                         │   Voyage Concierge Agent      │
                         │   (Registered on Agentverse)  │
                         └───────────────┬───────────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 ▼                       ▼                       ▼
      ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
      │ FlightFinder Agent │  │ StayDiscovery Agent│  │ Activity Agent     │
      │ • Live route comparison│• Curated villas/resorts│• Local guided tours│
      │ • Cabin class tiers│  │ • Room tier pricing│  │ • PADI diving/safari│
      └────────────────────┘  └────────────────────┘  └────────────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │      Payment & Escrow Agent   │
                         │  • Line-item tax calculation  │
                         │  • FET Token exchange rate   │
                         │  • Fetch.ai Payment Protocol  │
                         └───────────────────────────────┘
```

---

## 🎴 3. ASI:One Interactive Cards Implemented

VoyageAI showcases all four standard **ASI1 Interactive Card schemas** inside the chat drawer:

| Stage | Card Kind | Wire Payload & Interaction |
| :--- | :--- | :--- |
| **1. Flights Selection** | `carousel` | Horizontally scrollable airline cards with timings, duration, carbon metrics, and direct `Select Flight` CTA. |
| **2. Cabin Selection** | `detail` | Flight route details with interactive radio selectors for `Economy` vs. `Business` class. |
| **3. Stays Selection** | `carousel` | Handpicked beachfront resorts and villas with photo previews and night rates. |
| **4. Room Tier Picker** | `detail` | Resort amenities with radio options for `Standard Ocean View` vs. `Deluxe Private Pool Villa`. |
| **5. Curated Activities** | `carousel` | Exclusive local adventures (Scuba Safari, Catamaran Cruise, Spice Plantation). |
| **6. Guest Details** | `form` | Native drawer form capturing Lead Traveler Name, Email, and Phone. |
| **7. Escrow Authorization**| `review` | Complete line-item breakdown (INR + FET conversion) with `Authorize Escrow Deposit` CTA. |

---

## 💰 4. Fetch.ai Payment Protocol & Monetization Model

1. **Decentralized Escrow**: Rather than paying vendors upfront, booking funds are locked in a Fetch.ai Escrow smart contract upon traveler confirmation.
2. **Milestone Release**: Funds are automatically released to the airline, hotel, and activity providers upon verifiable check-in / boarding verification.
3. **Agent-to-Agent Micro-Commission**: The orchestrator receives a **1.5% protocol fee in FET** for coordinating the sub-agents and verifying booking integrity.

---

## 🚀 5. Quick Start & Local Testing

### Prerequisites
- Python 3.10 or 3.11
- Git

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/Ashwani93333/voyage-ai-agent.git
cd voyage-ai-agent

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```

### 3. Run the End-to-End Test Suite
To validate all card schemas, wire payloads, and state transitions locally:
```bash
python test_client.py
```
Expected output:
```
🔍 Validating [Flights Carousel] (card_kind: 'carousel') -> ✅ PASS
🔍 Validating [Flight Detail with Cabin Selector] (card_kind: 'detail') -> ✅ PASS
🔍 Validating [Stays Carousel] (card_kind: 'carousel') -> ✅ PASS
🔍 Validating [Hotel Detail with Room Tier] (card_kind: 'detail') -> ✅ PASS
🔍 Validating [Activities Carousel] (card_kind: 'carousel') -> ✅ PASS
🔍 Validating [Traveler Contact Form] (card_kind: 'form') -> ✅ PASS
🔍 Validating [Itinerary Review & Escrow Card] (card_kind: 'review') -> ✅ PASS
✨ ALL TESTS & CARD SCHEMAS PASSED SUCCESSFULLY!
```

### 4. Run the Agent Locally
```bash
python voyage_orchestrator.py
```

---

## 🌐 6. Registering on Agentverse & ASI:One

To make VoyageAI discoverable on [ASI:One](https://asi1.ai/):

1. **Log in to [Agentverse.ai](https://agentverse.ai/)**
2. Go to **Agents** → **New Agent** → Select **Local Agent with Mailbox**.
3. Generate a **Mailbox API Key** and add it to your `.env`:
   ```env
   AGENTVERSE_API_KEY="your_agentverse_mailbox_key_here"
   ```
4. Update `voyage_orchestrator.py` agent definition:
   ```python
   agent = Agent(
       name="voyage_concierge",
       seed=SEED_PHRASE,
       mailbox=f"{AGENTVERSE_API_KEY}@https://agentverse.ai",
   )
   ```
5. In Agentverse, register the **Agent Chat Protocol** capability so that the agent appears on [ASI:One](https://asi1.ai/).
6. Open [asi1.ai](https://asi1.ai/) and start a conversation with `@voyage_concierge`.

---

## 📋 7. Hackathon Submission Deliverables

- **Public GitHub Repository**: Complete open-source code with instructions.
- **Agentverse Profile URL**: Registered address for `@voyage_concierge`.
- **ASI:One Shared Chat URL**: Demonstrating full journey from initial intent to confirmed booking escrow.
- **Demo Video**: 2-minute walkthrough showing interactive cards rendering and multi-step action execution.

---

*Built for the ASI:One Agent Challenge — Fetch-A-Thon 3.0*
