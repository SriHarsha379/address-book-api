# Address Book API (FastAPI + SQLite)

Minimal, production-like backend API for an Address Book with CRUD and distance-based search, plus a simple browser-based frontend.

## Features
- Full CRUD for addresses (create, read, update, delete)
- SQLite database via SQLAlchemy ORM
- Pydantic validation:
  - latitude in `[-90, 90]`
  - longitude in `[-180, 180]`
  - name up to 255 characters (optional)
- Nearby search:
  - `GET /addresses/nearby?lat=<lat>&lon=<lon>&distance=<km>`
  - Uses Haversine formula for accurate great-circle distance
- Swagger UI automatically available at `/docs`
- Minimal browser frontend served at `/`

## Project Structure
```
main.py            # FastAPI app entry point, mounts routes and frontend
database.py        # SQLAlchemy engine, session, and Base
models.py          # ORM model: Address
schemas.py         # Pydantic schemas: AddressCreate, AddressUpdate, AddressOut
crud.py            # CRUD helpers (create, get, list, update, delete)
routes/
  address.py       # /addresses router (all address endpoints)
utils/
  distance.py      # haversine_km() distance calculation
frontend/
  index.html       # Simple browser UI
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

## Configuration

| Environment Variable    | Default           | Description                        |
|-------------------------|-------------------|------------------------------------|
| `ADDRESS_BOOK_DB_PATH`  | `address_book.db` | Path to the SQLite database file   |

## Run
```bash
uvicorn main:app --reload
```

- Frontend UI:  http://127.0.0.1:8001/
- API base URL: http://127.0.0.1:8001/addresses
- Swagger UI:   http://127.0.0.1:8001/docs
- Health check: http://127.0.0.1:8001/health

## API Endpoints

| Method   | Endpoint                    | Description                              |
|----------|-----------------------------|------------------------------------------|
| `POST`   | `/addresses`                | Create a new address                     |
| `GET`    | `/addresses`                | List all addresses                       |
| `PUT`    | `/addresses/{id}`           | Update an existing address (partial ok)  |
| `DELETE` | `/addresses/{id}`           | Delete an address                        |
| `GET`    | `/addresses/nearby`         | Find addresses within a distance (km)    |
| `GET`    | `/health`                   | Health check                             |

## Example Requests

### Create an address
```bash
curl -X POST http://127.0.0.1:8001/addresses \
  -H "Content-Type: application/json" \
  -d '{"name":"Home","latitude":12.9716,"longitude":77.5946}'
```

### Get all addresses
```bash
curl http://127.0.0.1:8001/addresses
```

### Update an address
```bash
curl -X PUT http://127.0.0.1:8001/addresses/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Office","latitude":12.9352,"longitude":77.6245}'
```

### Delete an address
```bash
curl -X DELETE http://127.0.0.1:8001/addresses/1
```

### Nearby search (within 5 km)
```bash
curl "http://127.0.0.1:8001/addresses/nearby?lat=12.9716&lon=77.5946&distance=5"
```
