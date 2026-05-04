# Address Book API (FastAPI + SQLite)

Minimal, production-like backend API for an Address Book with CRUD and distance-based search.

## Features
- CRUD for addresses
- SQLite database via SQLAlchemy ORM
- Pydantic validation:
  - latitude in `[-90, 90]`
  - longitude in `[-180, 180]`
- Nearby search:
  - `GET /addresses/nearby?lat=<lat>&lon=<lon>&distance=<km>`
  - Uses Haversine distance in kilometers
- Swagger UI automatically available at `/docs`

## Project Structure
```
main.py
database.py
models.py
schemas.py
crud.py
routes/address.py
utils/distance.py
requirements.txt
```

## Setup

### 1) Create and activate a virtual environment (recommended)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

## Run
```bash
uvicorn main:app --reload
```

- API base URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Example Requests

### Create an address
```bash
curl -X POST http://127.0.0.1:8000/addresses \
  -H "Content-Type: application/json" \
  -d '{"name":"Home","latitude":12.9716,"longitude":77.5946}'
```

### Get all addresses
```bash
curl http://127.0.0.1:8000/addresses
```

### Nearby search (within 5km)
```bash
curl "http://127.0.0.1:8000/addresses/nearby?lat=12.9716&lon=77.5946&distance=5"
```
