# Day 3 – Notes API Implementation

## Overview

On Day 3, I implemented the **Notes feature** in the FastAPI backend application. This includes creating and listing notes, following a clean architecture pattern, and ensuring all functionality is covered by automated tests.

---

## What I Did on Day 3

### 1. Notes API

Implemented REST APIs for managing notes:

- **Create Note** – Add a new note
- **List Notes** – Fetch all notes

#### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/notes/` | Create a new note |
| `GET` | `/notes/` | Get all notes |

---

### Authentication (JWT)

After the Day 3 work we also added a simple JSON Web Token (JWT) based
authentication flow to support protected endpoints and demo user accounts.

- Endpoints:
  - `POST /auth/register` — register a new user (body: username, password)
  - `POST /auth/token` — exchange credentials for an access token
- Tokens are standard JWTs created with the secret configured via `JWT_SECRET`
  in the environment (see `app/config/settings.py`).
- Protected endpoints accept an HTTP Bearer token and are implemented using
  FastAPI's `HTTPBearer` dependency so the Swagger UI shows an "Authorize"
  control where you can paste `Bearer <token>` and try protected routes.

Files to review for auth:
- `app/models/user.py` — User model
- `app/repositories/user_repository.py` — persistence helpers
- `app/services/user_service.py` — registration & authentication (password hashing)
- `app/services/auth_service.py` — token creation & validation
- `app/routers/auth.py` — register & token endpoints

### Authentication — implemented features (summary)

We extended the demo auth skeleton into a small, production-minded flow (safe for learning / demos):

- Registration (`POST /auth/register`)
  - Accepts `email`, `name`, `password` (Pydantic request model).
  - Password validator enforces min length and requires at least one uppercase letter and one digit.
  - Returns an access token on successful registration together with user info (id, email, name).

- Login / Token (`POST /auth/token`)
  - Accepts identifier (email or username) and password.
  - Issues a JWT access token on successful authentication.
  - Rate-limited (demo in-memory limiter): 5 failed attempts per minute per IP, returns 429 after limit.

- Logout (`POST /auth/logout`)
  - Protected endpoint that blacklists the current token (DB-backed `revoked_tokens` table).
  - Returns 204 No Content on success; blacklisted tokens are rejected by protected routes.

- Protected endpoints
  - `GET /protected` demonstrates use of the `get_current_user` dependency which validates tokens and checks the blacklist.
  - FastAPI's HTTP Bearer integration exposes the Swagger "Authorize" button so you can paste `Bearer <token>` and try protected routes.

What changed in code
- `app/models/user.py` — added `email` and `name` fields and `RevokedToken` model (DB table `revoked_tokens`).
- `app/repositories/token_repository.py` — manages revoked tokens.
- `app/services/user_service.py` — registration now accepts email/name and hashes passwords.
- `app/services/auth_service.py` — token creation/validation and blacklist checks in `get_current_user`.
- `app/routers/auth.py` — `POST /auth/register`, `POST /auth/token` (rate-limited), and `POST /auth/logout` implemented.

Notes & next steps
- Password hashing currently uses `passlib`'s `sha256_crypt` for demo stability. For production, switch to `bcrypt` (12 rounds) and ensure the native `bcrypt` wheel is available.
- JWT claim hardening (aud, iss, kid) and default expiry change (30 minutes) are planned next steps.
- Token blacklist is DB-backed for persistence; for high-scale deployments consider storing token identifiers (jti) with TTL in Redis.



### 2. Clean Architecture

Followed proper separation of concerns:

#### Router Layer (`app/routers/note.py`)
- Handles HTTP requests and responses
- No business logic
- Routes requests to service layer

#### Service Layer (`app/services/note_service.py`)
- Contains business logic
- Validates data
- Coordinates between router and repository

#### Repository Layer (`app/repositories/note_repository.py`)
- Handles database operations
- Data access logic
- CRUD operations

#### Schema Layer (`app/schemas/note.py`)
- Request and response validation using Pydantic
- Data models
- Type validation

**Benefits:**
- Clean separation of concerns
- Easy to test and maintain
- Scalable architecture

---

### 3. Database Integration

Used **SQLAlchemy (Async)** for database interaction.

#### Note Model

Created `Note` model with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key (auto-increment) |
| `title` | String | Note title |
| `content` | Text | Note content |
| `created_at` | DateTime | Timestamp of creation |

**Database:**
- Async SQLAlchemy ORM
- SQLite database (development)
- Alembic for migrations (if used)

---

### 4. Testing

Wrote and executed automated tests using **pytest**:

#### Unit Tests
- **Note Repository Tests**
  - Test database CRUD operations
  - Verify data persistence
- **Note Service Tests**
  - Test business logic
  - Validate service methods

#### Integration Tests
- **Create Note API Test**
  - Test POST endpoint
  - Verify response format
  - Check data validation
- **List Notes API Test**
  - Test GET endpoint
  - Verify returned data structure
  - Check empty list handling

**Result:** All tests passed successfully ✅

---

### 5. Test Coverage

**Coverage Report:**
- **Required coverage:** 80%
- **Achieved coverage:** ~94% ✅

**Coverage exceeded requirements by 14%!**

---

## How to Run the Project

### Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

Note: the application uses a FastAPI async lifespan context manager to
perform startup tasks (for example creating DB tables) instead of the
older `@app.on_event("startup")` decorator.

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

### View API Documentation

Open your browser and go to:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Tip: use the "Authorize" button in the Swagger UI to paste a Bearer token
(`Bearer <token>`) and try protected endpoints.

---

## API Testing

### Using Swagger

#### Create Note

**Request:**
```
POST http://127.0.0.1:8000/notes/
Content-Type: application/json
```

**Body:**
```json
{
  "title": "My Note",
  "content": "This is a sample note"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "My Note",
    "content": "This is a sample note",
    "created_at": "2026-01-05T12:00:00"
  },
  "request_id": "unique-uuid"
}
```

#### List Notes

**Request:**
```
GET http://127.0.0.1:8000/notes/
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "My Note",
      "content": "This is a sample note",
      "created_at": "2026-01-05T12:00:00"
    }
  ],
  "request_id": "unique-uuid"
}
```

---

## Project Structure (Day 3)

```
app/
├── routers/
│   ├── health.py
│   ├── service.py
│   └── note.py              # NEW: Notes router
├── services/
│   ├── health_service.py
│   ├── service_info.py
│   └── note_service.py      # NEW: Notes service
├── repositories/
│   └── note_repository.py   # NEW: Notes repository
├── models/
│   └── note.py              # NEW: SQLAlchemy model
├── schemas/
│   └── note.py              # NEW: Pydantic schemas
├── database/
│   ├── __init__.py
│   └── connection.py        # Database connection
├── utils/
│   └── response.py
├── middleware/
│   ├── security.py
│   └── error_handler.py
├── config/
│   └── settings.py
└── main.py

tests/
├── unit/
│   ├── test_health_service.py
│   ├── test_service_info.py
│   ├── test_note_service.py      # NEW: Service tests
│   └── test_note_repository.py   # NEW: Repository tests
├── integration/
│   ├── test_health_api.py
│   ├── test_service_api.py
│   └── test_note_api.py          # NEW: API tests
├── test_security.py
└── test_error_handling.py
```

---

## Simple Explanation (Interview Ready)

> On Day 3, I implemented a **Notes feature** using FastAPI. I followed a **clean architecture** by separating routers, services, and repositories. I added APIs to **create and list notes**, integrated an **async database using SQLAlchemy**, and wrote **unit and integration tests** with pytest. All tests passed with **more than 80% coverage**.

---

## Key Learnings

### 1. Clean Architecture Benefits
- Code is easier to test
- Changes are isolated to specific layers
- Business logic is independent of framework

### 2. Async Database Operations
- Better performance with async SQLAlchemy
- Non-blocking I/O operations
- Scalable for concurrent requests

### 3. Test-Driven Development
- Writing tests first helps design better APIs
- Tests document expected behavior
- High coverage gives confidence in code

### 4. Pydantic Validation
- Automatic request/response validation
- Type safety
- Clear error messages for invalid data

---

## Test Results

```
==================== test session starts ====================
collected 18 items

tests/unit/test_note_repository.py ....         [ 22%]
tests/unit/test_note_service.py ....            [ 44%]
tests/integration/test_note_api.py ....         [ 66%]
tests/integration/test_health_api.py ...        [ 83%]
tests/integration/test_service_api.py ...       [100%]

==================== 18 passed in 0.45s ====================

Coverage Report:
Name                              Stmts   Miss  Cover
-----------------------------------------------------
app/routers/note.py                  12      0   100%
app/services/note_service.py         15      1    93%
app/repositories/note_repository.py  18      1    94%
app/schemas/note.py                   8      0   100%
-----------------------------------------------------
TOTAL                               427     25    94%
```

---

## Status

✅ **Day 3 Assignment Completed Successfully**

**What's Working:**
- Create Note API ✅
- List Notes API ✅
- Database integration ✅
- Unit tests ✅
- Integration tests ✅
- 94% test coverage ✅

---

## Progress Summary

- **Day 0:** Security & Testing Setup ✅
- **Day 1:** Core Service APIs ✅
- **Day 2:** API Development & Testing ✅
- **Day 3:** Notes API Implementation ✅

---