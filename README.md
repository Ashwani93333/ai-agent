# 🌴 VoyageAI — Autonomous Travel & Experience Concierge
### ASI:One Agent Challenge (Fetch-A-Thon 3.0): From Intent to Action

[![Fetch.ai](https://img.shields.io/badge/Fetch.ai-uAgents-blue?style=for-the-badge&logo=fetch.ai)](https://fetch.ai/)
[![Protocol](https://img.shields.io/badge/Protocol-ACP%20(Agent%20Chat%20Protocol)-purple?style=for-the-badge)](https://innovationlab.fetch.ai/)
[![ASI:One Cards](https://img.shields.io/badge/UI-ASI%3AOne%20Interactive%20Cards-success?style=for-the-badge)](https://asi1.ai/)
[![Network](https://img.shields.io/badge/Ledger-Fetch.ai%20Dorado%20Testnet-orange?style=for-the-badge)](https://explore-dorado.fetch.ai/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen?style=for-the-badge&logo=python)](https://www.python.org/)

---

## 📖 Table of Contents
1. [Overview & Problem Solved](#-1-overview--problem-solved)
2. [Multi-Agent Swarm Architecture](#-2-multi-agent-swarm-architecture)
3. [ASI:One Interactive Cards Implemented](#-3-asione-interactive-cards-implemented)
4. [Fetch.ai Smart Escrow & Economic Model](#-4-fetchai-smart-escrow--economic-model)
5. [Complete Command & Execution Guide](#-5-complete-command--execution-guide)
   - [Prerequisites](#51-prerequisites)
   - [Setup & Virtual Environment](#52-setup--virtual-environment)
   - [End-to-End Automated Testing](#53-end-to-end-automated-testing)
   - [Method 1: Running Locally with Public Tunnel](#54-method-1-running-locally-with-public-tunnel-recommended-for-development)
   - [Method 2: 100% Cloud-Hosted on Agentverse](#55-method-2-100-cloud-hosted-on-agentverse-recommended-for-production)
6. [Testing on ASI:One](#-6-testing-on-asione)
7. [Repository File Map](#-7-repository-file-map)
8. [Troubleshooting & Common Issues](#-8-troubleshooting--common-issues)
9. [Related Documents](#-9-related-documents)

---

## 🎯 1. Overview & Problem Solved

### The Problem
Traditional online travel booking is fragmented and painful:
- Travelers bounce between 5–10 browser tabs comparing airlines, resorts, and local excursion blogs.
- Conversational AI chatbots only output static, plain text recommendations without executable outcomes.
- Travelers lack decentralized escrow protection against cross-vendor double bookings, cancellations, and hidden charges.

### The Solution: VoyageAI
**VoyageAI** is a multi-agent travel concierge operating directly inside **[ASI:One](https://asi1.ai/)**. Powered by the **Agent Chat Protocol (ACP)** and **ASI:One Interactive Cards**, it converts a simple conversational prompt like:

> *"Plan a luxury weekend getaway to Goa with flights from Delhi, beachfront villa, and scuba diving."*

into an interactive, executable journey right inside the native ASI:One conversation drawer — without requiring an external frontend or leaving the chat interface.

---

## 🏗️ 2. Multi-Agent Swarm Architecture

VoyageAI distributes domain tasks across a coordinated multi-agent network orchestrated by the **Voyage Concierge**:

```
                                  [ ASI:One User ]
                                         │
                                         ▼ (ACP over WebSockets/HTTP)
                         ┌───────────────────────────────┐
                         │   Voyage Concierge Agent      │
                         │  (voyage_orchestrator.py)     │
                         │  (Registered on Agentverse)   │
                         └───────────────┬───────────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 ▼                       ▼                       ▼
      ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
      │ FlightFinder Agent │  │ StayDiscovery Agent│  │ Experience Curator │
      │(agents/flight_agent│  │(agents/hotel_agent)│  │(activity_agent.py) │
      │ • Live route match │  │ • Beachfront villas│  │ • PADI scuba safari│
      │ • Cabin class tiers│  │ • Room tier pricing│  │ • Catamaran cruises│
      └────────────────────┘  └────────────────────┘  └────────────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │    Payment & Escrow Agent     │
                         │   (agents/payment_agent.py)   │
                         │  • Line-item tax calculation  │
                         │  • FET Token exchange rate    │
                         │  • Fetch.ai Smart Escrow      │
                         └───────────────────────────────┘
```

---

## 🎴 3. ASI:One Interactive Cards Implemented

VoyageAI showcases all four standard **ASI:One Interactive Card schemas**:

| Stage | Card Kind | Wire Payload & Interaction |
| :--- | :--- | :--- |
| **1. Flights Selection** | `carousel` | Horizontally scrollable airline cards with timings, duration, carbon metrics, and direct `Select Flight` CTA. |
| **2. Cabin Selection** | `detail` | Flight route details with interactive radio selectors for `Economy` vs. `Business` class. |
| **3. Stays Selection** | `carousel` | Handpicked beachfront resorts and villas with photo previews and night rates. |
| **4. Room Tier Picker** | `detail` | Resort amenities with radio options for `Standard Ocean View` vs. `Deluxe Private Pool Villa`. |
| **5. Curated Activities** | `carousel` | Exclusive local adventures (Scuba Safari, Catamaran Cruise, Spice Plantation). |
| **6. Guest Details** | `form` | Native drawer form capturing Lead Traveler Name, Email, and Phone. |
| **7. Escrow Authorization**| `review` | Complete line-item breakdown (INR + FET conversion) with `Authorize Escrow Deposit` CTA. |
| **8. Confirmation & Receipt**| `text`/`terminal`| Final confirmed PNR, booking vouchers, Fetch.ai smart contract address, Dorado ledger transaction hash, and 2-milestone check-in release schedule. |

---

## 💰 4. Fetch.ai Smart Escrow & Economic Model

1. **Decentralized Escrow**: Rather than paying vendors upfront, booking funds are locked in a Fetch.ai Escrow smart contract upon traveler confirmation.
2. **Two-Stage Milestone Release**:
   - **50% Released**: Upon airport security and boarding check-in verification.
   - **50% Released**: Upon resort reception check-in verification.
3. **Agent Micro-Commission**: The orchestrator receives a **1.5% protocol fee in FET** for coordinating sub-agents and ensuring booking integrity.

---

## 🚀 5. Complete Command & Execution Guide

### 5.1 Prerequisites
- **Python 3.10 or 3.11** installed
- **Git** installed
- **Node.js & npx** (for running localtunnel if testing locally)

---

### 5.2 Setup & Virtual Environment

```bash
# 1. Clone the repository
git clone https://github.com/Ashwani93333/voyage-ai-agent.git
cd voyage-ai-agent

# 2. Create and activate virtual environment
# On Windows (PowerShell):
python -m venv .venv
.venv\Scripts\activate

# On Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate

# 3. Install required Python packages
pip install -r requirements.txt
```

---

### 5.3 End-to-End Automated Testing

Before running the live agent, validate that all agent modules, payload generators, and card schemas conform to the **ASI:One Card Protocol v1**:

```bash
# Run the end-to-end card schema validator
python test_client.py
```

Expected output:
```text
🔍 Validating [Flights Carousel] (card_kind: 'carousel') -> ✅ PASS
🔍 Validating [Flight Detail with Cabin Selector] (card_kind: 'detail') -> ✅ PASS
🔍 Validating [Stays Carousel] (card_kind: 'carousel') -> ✅ PASS
🔍 Validating [Hotel Detail with Room Tier] (card_kind: 'detail') -> ✅ PASS
🔍 Validating [Activities Carousel] (card_kind: 'carousel') -> ✅ PASS
🔍 Validating [Traveler Contact Form] (card_kind: 'form') -> ✅ PASS
🔍 Validating [Itinerary Review & Escrow Card] (card_kind: 'review') -> ✅ PASS
✨ ALL TESTS & CARD SCHEMAS PASSED SUCCESSFULLY!
```

---

### 5.4 Method 1: Running Locally with Public Tunnel (Recommended for Development)

This method runs the agent on your machine and exposes it via a public tunnel to receive live webhooks from ASI:One.

#### Step 1: Configure Environment Variables
Create or edit your `.env` file:
```env
AGENT_ENDPOINT_URL="https://nine-phones-drive.loca.lt/submit"
AGENT_SEED_PHRASE="voyage-ai-orchestrator-hackathon-seed-2026"
PORT=8000
```

#### Step 2: Start the Public Tunnel (Terminal 1)
```bash
npx -y localtunnel --port 8000 --subdomain nine-phones-drive
```
> Keep this terminal open. It will confirm: `your url is: https://nine-phones-drive.loca.lt`

#### Step 3: Register the Agent on Agentverse (One-Time Setup)
```bash
python register_agent.py
```

#### Step 4: Start the Voyage Concierge Orchestrator (Terminal 2)
```bash
python voyage_orchestrator.py
```

Output:
```text
🚀 Starting VoyageAI Concierge Agent on port 8000...
Agent address: agent1qw0wxtlush68t8h92s7y23546zmu72jlq0u9637cl9qq6ql869mz2sc47wm
INFO: Starting server on http://0.0.0.0:8000
INFO: Manifest published successfully: AgentChatProtocol
INFO: Agent registration status updated to active
INFO: Registration on Almanac API successful
```

---

### 5.5 Method 2: 100% Cloud-Hosted on Agentverse (Recommended for Production)

If you don't want to run local tunnels or keep your computer on, you can host VoyageAI directly in the Fetch.ai cloud:

1. Open **[Agentverse.ai](https://agentverse.ai/)** and log in.
2. Go to **My Agents** → click **+ New Agent** → select **Blank Agent**.
3. Name the agent `voyage_concierge`.
4. Open [`agentverse_hosted_agent.py`](agentverse_hosted_agent.py) in this repository, copy the entire file contents, and paste it into the Agentverse web editor.
5. Click **Start** in the top-right corner.
6. The agent is now running 24/7 on Fetch.ai cloud infrastructure!

---

## 🌐 6. Testing on ASI:One

Once your agent is running (via Method 1 or Method 2):

1. Open **[ASI:One](https://asi1.ai/)**.
2. Start a new chat and send:
   ```text
   @agent1qw0wxtlush68t8h92s7y23546zmu72jlq0u9637cl9qq6ql869mz2sc47wm plan a trip to goa
   ```
3. **Interact with the live cards**:
   - **Step 1**: In the **Flights Carousel**, click **`Select Flight`** (e.g. *IndiGo 6E-602*).
   - **Step 2**: In the **Flight Detail Card**, select **`Business Class`** and click **`Confirm Cabin & Proceed`**.
   - **Step 3**: In the **Hotels Carousel**, browse resorts and click **`View Resort`** (e.g. *W Goa*).
   - **Step 4**: In the **Resort Detail Card**, select **`Deluxe Private Pool Villa`** and click **`Select Room & Add Experiences`**.
   - **Step 5**: In the **Activities Carousel**, click **`Add to Itinerary`** on *Grand Island Scuba Diving*.
   - **Step 6**: In the **Traveler Form**, enter passenger name, email, and phone, then submit.
   - **Step 7**: In the **Review & Escrow Card**, inspect the dual-currency pricing (INR + FET tokens) and click **`Confirm & Lock Escrow`**.
   - **Step 8**: Receive the on-chain booking confirmation with PNR, Fetch.ai smart escrow contract address, and transaction hash!

---

## 📁 7. Repository File Map

```text
ai-agent/
├── agents/
│   ├── flight_agent.py         # FlightFinder Agent: routes, pricing tiers, CO2 metrics
│   ├── hotel_agent.py          # StayDiscovery Agent: luxury resorts & room categories
│   ├── activity_agent.py       # ExperienceCurator Agent: guided excursions & tours
│   └── payment_agent.py        # Payment & Escrow Agent: form builder, FET rates, escrow
├── mock_data/
│   ├── flights.json            # Mock dataset for airlines and timings
│   ├── hotels.json             # Mock dataset for resorts and amenities
│   └── activities.json         # Mock dataset for local adventures
├── agentverse_hosted_agent.py  # All-in-one cloud edition for Agentverse Web IDE
├── voyage_orchestrator.py      # Master uAgent orchestrator implementing ACP v1
├── register_agent.py           # Script to register local agent with Agentverse
├── test_client.py              # Automated test suite validating all 4 card schemas
├── requirements.txt            # Python dependencies (uagents, pydantic, requests)
├── .env.example                # Template for configuration environment variables
├── PRD.md                      # Product Requirements Document
├── PWD.md                      # Product Workflow & Architecture Document
└── README.md                   # Complete documentation and command reference
```

---

## 🛠️ 8. Troubleshooting & Common Issues

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **`503 Tunnel Unavailable`** | Localtunnel connection dropped or changed subdomain. | Re-run `npx localtunnel --port 8000 --subdomain nine-phones-drive` and check that the subdomain matches `.env`. |
| **`Could not validate credentials`** | `AGENTVERSE_KEY` in `.env` expired. | Generate a fresh API key from the Agentverse registration screen and update `.env`. |
| **Agent unreachable in ASI:One** | Local orchestrator is not running. | Verify `python voyage_orchestrator.py` is running in an active terminal on port 8000. |
| **ModuleNotFoundError** | Running Python from global instead of virtual environment. | Always activate the virtual environment (`.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on Linux/Mac). |

---

## 📚 9. Related Documents

- 📄 [Product Requirements Document (PRD.md)](PRD.md)
- 🛠️ [Product Workflow & Architecture Document (PWD.md)](PWD.md)

---

*Built with ❤️ for the ASI:One Agent Challenge (Fetch-A-Thon 3.0)*
