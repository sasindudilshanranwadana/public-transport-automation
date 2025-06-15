# backend/app/main.py

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv                                           # 🔧 Ensure we can load .env
import os
import logging                                                            # 🔧 For logging exceptions
import stripe                                                             # 🔧 Stripe SDK

from models import Location, PlanRequest, PaymentRequest                  # your Pydantic models
from ptv_client import plan_trip, get_nearby_vehicles                                          # your trip-planning function
from payment import process_payment                                       # your payment helper

# ─── 0) Load environment ────────────────────────────────────────────────────
load_dotenv()                                                              # 🔧 read .env from project root

# ─── 1) Configure Stripe ────────────────────────────────────────────────────
stripe.api_key = os.getenv("STRIPE_API_KEY")                              # 🔧 set Stripe key

# ─── 2) Configure logging ───────────────────────────────────────────────────
logger = logging.getLogger("uvicorn.error")                                # 🔧 use Uvicorn’s error logger

# ─── 3) FastAPI app init ────────────────────────────────────────────────────
app = FastAPI(title="Melbourne Transport Companion")

# ─── 4) Location endpoint ───────────────────────────────────────────────────
@app.post("/location")
async def receive_location(loc: Location):
    # simply forward or store the location
    # e.g., await db.save_location(loc)
    return {"status": "received"}

# ─── 5) Nearby vehicles ─────────────────────────────────────────────────────
@app.get("/vehicles")
async def vehicles(lat: float, lon: float):
    try:
        return await get_nearby_vehicles(lat, lon)
    except Exception as e:
        logger.error("Error in /vehicles", exc_info=e)                     # 🔧 log full traceback
        raise HTTPException(status_code=500, detail="Failed to fetch vehicles")

# ─── 6) Trip planning ───────────────────────────────────────────────────────
@app.post("/plan")
async def plan(req: PlanRequest):
    try:
        # 🔧 unpack floats if your plan_trip signature expects lat/lon separately
        o_lat, o_lon = req.origin.lat, req.origin.lon
        d_lat, d_lon = req.destination.lat, req.destination.lon
        return await plan_trip(o_lat, o_lon, d_lat, d_lon)
    except HTTPException:
        # let FastAPI re-raise your own HTTPExceptions
        raise
    except Exception as e:
        logger.error("Error in /plan", exc_info=e)                          # 🔧 log full traceback
        raise HTTPException(status_code=500, detail="Trip planning failed")

# ─── 7) Payment processing ──────────────────────────────────────────────────
@app.post("/payment")
async def payment(req: PaymentRequest):
    try:
        result = process_payment(req.trip_id, req.amount, req.token)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))