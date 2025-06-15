# backend/app/ptv_client.py

from models import Location
import os, hashlib, hmac, httpx

PTV_DEV_ID     = os.getenv("PTV_DEV_ID")
PTV_DEV_SECRET = os.getenv("PTV_DEV_SECRET")
PTV_BASE_URL   = "https://timetableapi.ptv.vic.gov.au"

async def plan_trip(origin: Location, destination: Location) -> dict:
    """
    origin and destination are Pydantic Location models with .lat and .lon
    """
    # 1) Build the unsigned path + query using attribute access
    path = "/v3/travel/trip"
    query = (
        f"?origin_lat={origin.lat}"
        f"&origin_lon={origin.lon}"
        f"&dest_lat={destination.lat}"
        f"&dest_lon={destination.lon}"
    )
    unsigned_url = f"{path}{query}"

    # 2) Sign the request
    signature = hmac.new(
        PTV_DEV_SECRET.encode("utf-8"),
        unsigned_url.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    url = (
        f"{PTV_BASE_URL}{unsigned_url}"
        f"&devid={PTV_DEV_ID}"
        f"&signature={signature}"
    )

    # 3) Perform the request
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

# TODO: implement get_nearby_vehicles
async def get_nearby_vehicles(lat: float, lon: float) -> list:
    """
    Fetch nearby public transport vehicles given latitude and longitude.
    Returns a list of dicts with keys: route, minutes, etc.
    """
    # Example endpoint and implementation:
    path = "/v3/vehicles/route-types/0"  # 0 for trains, 1 for trams, etc.
    query = f"?lat={lat}&lon={lon}"
    unsigned_url = f"{path}{query}"

    # Sign as before
    signature = hmac.new(
        PTV_DEV_SECRET.encode("utf-8"),
        unsigned_url.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()
    url = (
        f"{PTV_BASE_URL}{unsigned_url}"
        f"&devid={PTV_DEV_ID}"
        f"&signature={signature}"
    )

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        # Transform PTV response to simple list:
        vehicles = []
        for v in data.get('vehicles', []):
            vehicles.append({
                'route': v.get('run_id'),  # or appropriate field
                'minutes': v.get('estimated_departure_minutes')
            })
        return vehicles
