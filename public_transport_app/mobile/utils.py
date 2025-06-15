import requests
from requests.exceptions import RequestException

API_BASE_URL = "http://timetableapi.ptv.vic.gov.au"

def post_location(lat, lon):
    """Send current GPS location to the backend."""
    url = f"{API_BASE_URL}/location"
    payload = {"lat": lat, "lon": lon}
    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
    except RequestException as e:
        print(f"Error posting location: {e}")


def fetch_vehicles(lat, lon):
    """Fetch nearby public transport departures."""
    url = f"{API_BASE_URL}/vehicles"
    params = {"lat": lat, "lon": lon}
    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except RequestException as e:
        print(f"Error fetching vehicles: {e}")
        return []


def plan_trip_request(origin, destination):
    """Request trip planning from backend."""
    url = f"{API_BASE_URL}/plan"
    payload = {
        "origin": {"lat": origin[0], "lon": origin[1]},
        "destination": destination
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except RequestException as e:
        print(f"Error planning trip: {e}")
        return {}


def make_payment(trip_id, amount, token):
    """Send payment request to backend."""
    url = f"{API_BASE_URL}/pay"
    payload = {"trip_id": trip_id, "amount": amount, "token": token}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except RequestException as e:
        print(f"Error making payment: {e}")
        return {"success": False}
