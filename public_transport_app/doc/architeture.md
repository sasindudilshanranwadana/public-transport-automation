# System Architecture

This document outlines the high-level design and data flows for the Melbourne Transport Companion App.

## Components
- **Mobile Client (Kivy)**: UI for location updates, vehicle display, trip planning, and payments.
- **API Server (FastAPI)**: Handles incoming requests for location, vehicles, trip planning, and payments.
- **PTV Integration**: Communicates with the PTV Developer API for departures and trip itineraries.
- **Payment Gateway**: Integrates with Stripe for secure payment processing.

## Data Flows
1. **Location Update**: Client → `POST /location` → Server → forward/store
2. **Vehicle Lookup**: Client → `GET /vehicles?lat=&lon=` → Server → PTV → returns list
3. **Trip Planning**: Client → `POST /plan` → Server → PTV → returns itinerary
4. **Payment**: Client → `POST /pay` → Server → Stripe → returns status/receipt
