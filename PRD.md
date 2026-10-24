# 📄 VoyageAI — Product Requirements Document (PRD)
### Autonomous Travel & Experience Concierge on ASI:One & Fetch.ai
**Challenge:** ASI:One Agent Challenge (Fetch-A-Thon 3.0): *From Intent to Action*  
**Status:** In Production / Live  
**Target Platform:** [ASI:One](https://asi1.ai/) & [Agentverse](https://agentverse.ai/)  
**Version:** 1.0.0  

---

## 1. Executive Summary & Vision

### 1.1 Vision Statement
To transform travel planning from a fragmented, multi-tab ordeal into an effortless, unified, conversational experience where a single user prompt instantly mobilizes an autonomous multi-agent swarm, resulting in verifiable on-chain bookings protected by decentralized smart escrow.

### 1.2 Core Value Proposition
- **From Intent to Action**: Moves beyond basic text-only chatbots by generating **ASI:One Interactive Cards** directly in the chat drawer (selection carousels, radio detail cards, native forms, and payment reviews).
- **True Multi-Agent Collaboration**: A central orchestrator dynamically delegates domain tasks to specialized agents (FlightFinder, StayDiscovery, ExperienceCurator, and PaymentEscrow).
- **Decentralized Escrow Security**: Eliminates opaque booking markups and fraud through trustless smart escrow contracts on the Fetch.ai Dorado testnet, releasing funds only upon milestone check-in verifications.

---

## 2. Target Personas & Use Cases

### 2.1 Target Personas
1. **The Modern Leisure Traveler (Persona: Rahul)**
   - *Pain Point*: Spends 4+ hours jumping between airline portals, hotel aggregators, and activity blogs.
   - *Goal*: Request a complete weekend getaway to Goa in one natural sentence and customize it in under 3 minutes.
2. **The Crypto / Web3 Nomad (Persona: Elena)**
   - *Pain Point*: Frustrated by conventional credit card foreign exchange fees, slow refund disputes, and lack of crypto payment options.
   - *Goal*: Lock travel deposits in FET tokens via smart contract escrow with automatic milestone releases.
3. **The Corporate Event & Group Coordinator (Persona: Marcus)**
   - *Pain Point*: Needs clear itemized breakdowns, transparent vendor allocations, and automated receipts without hidden surcharges.
   - *Goal*: Receive instant verifiable ledger transaction hashes and line-item receipts.

### 2.2 Primary User Stories
- **US-01**: *As a traveler*, I want to type a natural request like *"Plan a luxury weekend trip to Goa"* so that I immediately see real-time flight options without filling search forms.
- **US-02**: *As a traveler*, I want to compare flight timings, cabin classes (Economy vs. Business), and carbon footprints inside an interactive card drawer.
- **US-03**: *As a traveler*, I want to browse vetted luxury beachfront resorts and select private pool villas with real-time price updates.
- **US-04**: *As an adventure seeker*, I want curated local excursions (e.g., PADI Scuba Diving or Catamaran Cruises) seamlessly bundled into my itinerary.
- **US-05**: *As a buyer*, I want to enter my traveler contact information directly in a native in-chat form without redirecting to external websites.
- **US-06**: *As a buyer*, I want to inspect a transparent line-item summary with dual-currency breakdown (INR + FET tokens) and lock the booking via a Fetch.ai smart escrow contract.

---

## 3. Product Features & Functional Requirements

### 3.1 Multi-Agent Swarm Structure
The system shall deploy a specialized multi-agent architecture:
- **Voyage Concierge Orchestrator (`voyage_orchestrator.py`)**:
  - Serves as the primary public entrypoint registered on Agentverse and discoverable on ASI:One.
  - Manages session state, handles message acknowledgments (`ChatAcknowledgement`), parses incoming user actions, and choreographs sub-agents.
- **FlightFinder Agent (`agents/flight_agent.py`)**:
  - Scours available non-stop routes between origin and destination airports.
  - Returns metadata including flight ID, carrier logos, departure/arrival schedules, cabin tiers, baggage allowances, and CO₂ emissions.
- **StayDiscovery Agent (`agents/hotel_agent.py`)**:
  - Curates high-rating beachfront hotels, heritage estates, and luxury boutique resorts.
  - Provides room tier variations (Standard Ocean View Suite vs. Deluxe Plunge Pool Villa) with night rates and amenities.
- **ExperienceCurator Agent (`agents/activity_agent.py`)**:
  - Matches destinations with guided local adventures (scuba diving, catamaran sunset sailing, spice plantation tours).
  - Bundles per-person pricing, duration, and safety certifications.
- **Payment & Escrow Agent (`agents/payment_agent.py`)**:
  - Formulates traveler contact intake forms.
  - Computes subtotal, dynamic 12% GST taxation, and live FET token conversion (1 FET ≈ 85 INR benchmark).
  - Manages the Fetch.ai Smart Escrow Protocol (locks total funds, allocates 1.5% protocol micro-commission, and establishes milestone releases).

### 3.2 ASI:One Interactive Cards Specification
The application shall implement all four standard card schemas under **ASI:One Card Protocol v1**:

| Card Stage | Schema Kind | Components & Interactions |
| :--- | :--- | :--- |
| **Stage 1: Flight Selection** | `carousel` | Horizontal scroll track, airline logos, flight duration, carbon badge, economy pricing, `Select Flight` primary CTA. |
| **Stage 2: Cabin Selector** | `detail` | Hero visual, summary rows (Route, Duration, Stops, CO₂), radio selection group (`economy` vs. `business`), `Confirm Cabin & Proceed` CTA. |
| **Stage 3: Resort Discovery** | `carousel` | High-res resort imagery, location, star ratings, nightly rate badge, `View Resort` primary CTA. |
| **Stage 4: Room Tier Picker** | `detail` | Resort hero image, amenity grid, check-in/out policies, radio selection group (`standard` vs. `deluxe`), `Select Room & Add Experiences` CTA. |
| **Stage 5: Activity Curation** | `carousel` | Experience imagery, duration badge, per-person pricing, `Add to Itinerary` CTA. |
| **Stage 6: Traveler Intake** | `form` | Native drawer form with fields (`full_name`, `email`, `phone`, `special_requests`), client-side validation, `Generate Final Itinerary & Review` submit CTA. |
| **Stage 7: Itinerary & Escrow** | `review` | Complete line-item breakdown (Flight + Stay + Activity + Taxes), dual currency total (INR & FET), Escrow Protection Badge, `Confirm & Lock Escrow` CTA. |
| **Stage 8: Terminal Certificate** | `text` / `terminal` | Final confirmed PNR, booking vouchers, Fetch.ai smart contract address, Dorado ledger transaction hash, and 2-milestone check-in release schedule. |

---

## 4. Monetization & Economic Model

### 4.1 Fetch.ai Escrow & Micro-Commission Architecture
1. **Trustless Escrow Deposit**:
   - Booking funds are not transferred directly to unverified merchants upfront.
   - 100% of the traveler’s funds are deposited into a Fetch.ai Escrow Smart Contract.
2. **Two-Stage Milestone Release**:
   - **Milestone 1 (50%)**: Released to the airline upon airport check-in verification.
   - **Milestone 2 (50%)**: Released to the resort and tour operator upon hotel reception check-in.
3. **Agent Protocol Fee**:
   - The Voyage Concierge receives a **1.5% protocol coordination fee** denominated in FET tokens per settled booking, incentivizing agent uptime and catalog maintenance.

---

## 5. Non-Functional & Technical Requirements

### 5.1 Performance & Latency
- **ACP Response Time**: Less than **1.5 seconds** from user prompt / card action to the delivery of the next card metadata.
- **Wire Payload Constraint**: Strict enforcement of ASI:One's **64 KB** ceiling per interactive card payload. Current VoyageAI payloads range between **1.8 KB and 4.2 KB**, providing 15x safety margin.

### 5.2 Fault Tolerance & Parsing Robustness
- **Hybrid Selection Ingestion**:
  - Handles direct structured JSON delivered via `@mention` in ASI:One.
  - Automatically strips leading `@agent1q...` mentions using regex extraction (`re.search(r"\{.*\}", text)`).
  - Provides a heuristic prose fallback parser for natural language user input routed through the ASI:One planner LLM.
- **Session Re-entrancy**:
  - User sessions are stored and indexed by sender address.
  - Users can restart or modify plans at any point by typing `"restart"` or clicking `"Customize Plan"`.

### 5.3 Security & Privacy
- **Seed Phrase Protection**: Private keys and seed phrases are isolated in local environment variables (`.env`) and never exposed over ACP packets.
- **On-Chain Transparency**: Real-time generation of verifiable transaction hashes formatted for the Dorado Testnet Explorer.

---

## 6. Success Metrics & KPIs

1. **End-to-End Conversion Rate**: >85% of users who initiate a trip prompt complete through to escrow lock.
2. **Card Rendering Fidelity**: 100% validation on all ASI:One Interactive Card schemas (`carousel`, `detail`, `form`, `review`).
3. **Zero-Tab Experience**: Total booking flow completed inside the ASI:One drawer without navigating to external browser tabs.
4. **Agent Response Reliability**: 99.9% uptime during active hackathon evaluation sessions.
