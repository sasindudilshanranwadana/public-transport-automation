# API Endpoints

## `POST /location`
**Request**: `{ lat: number, lon: number }`

**Response**: `{ status: "received" }`

---

## `GET /vehicles`
**Query Params**: `lat`, `lon`

**Response**: `[{ route: string, direction: number, departure_utc: string }, ...]`

---

## `POST /plan`
**Request**: `{ origin: { lat: number, lon: number }, destination: string }`

**Response**: `{ itinerary: ... }` (PTV response format)

---

## `POST /pay`
**Request**: `{ trip_id: string, amount: number, token: string }`

**Response**: `{ status: "paid", receipt: string }`
