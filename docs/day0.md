# Day 0 – Security & Testing Setup (FastAPI)

## What did I do today?

Today, I completed **Day 0** of the WEQ Python Backend Training. The goal of Day 0 was to set up a secure FastAPI foundation and proper testing system before building real features.

**In simple words:**  
I made sure my backend app is **secure by default**, **does not leak errors**, and is **tested properly**.

---

## What I built

### 1. FastAPI Application
- Created a basic FastAPI app
- Added routes only for testing (`/health`, `/boom`)

### 2. Security Middleware

I added a security middleware that runs for **every request**.

**It does:**
- Generates a unique **Request ID** (UUID) for every request
- Stores it in `request.state.request_id`
- Adds security headers to the response:
  - `X-Request-ID`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`

**This helps in:**
- Debugging issues
- Tracing requests in logs
- Improving basic API security

### 3. Central Error Handling

I created a **global error handler**.

**What it does:**
- Catches all unhandled exceptions
- Logs the real error internally
- Returns a safe, generic error message to the client
- Never exposes stack traces or internal details

**Example response:**
```json
{
  "error": "Internal server error",
  "request_id": "abc-123-uuid"
}
```

**This prevents security leaks.**

### 4. Environment Configuration
- Used `.env` and `.env.example`
- Added environment variable `ENV`
- Disabled Swagger (`/docs`) automatically when `ENV=prod`

This makes the app **production-ready**.

### 5. Proper Testing Setup

I set up **pytest** with:
- Async testing support
- Coverage reporting
- Minimum coverage requirement (80%)

I used:
- `httpx.AsyncClient`
- `ASGITransport` (modern FastAPI testing approach)

### 6. Tests I Wrote

#### Error Handling Test
Checks that:
- API returns `500`
- No stack trace is leaked
- `request_id` is included in response

#### Security Middleware Tests
Verifies:
- Request ID is added to response headers
- Security headers are present
- Middleware works for normal requests

### 7. Documentation

I created:
- `SECURITY.md` – checklist of security practices
- `TESTING_STRATEGY.md` – explains how tests are structured

---

## Test Results

- All tests passing
- 100% code coverage
- No security issues
- Ready for Day 1

**Example output:**
```
3 passed in 0.11s
Total coverage: 100%
```

---

## Project Structure (Day 0)

```
weq-day0/
├── app/
│   ├── main.py
│   ├── middleware/
│   │   ├── security.py
│   │   └── error_handler.py
│   └── config/
│       └── settings.py
├── tests/
│   ├── conftest.py
│   ├── test_security.py
│   └── test_error_handling.py
├── docs/
│   ├── SECURITY.md
│   └── TESTING_STRATEGY.md
├── pytest.ini
├── .env.example
└── requirements.txt
```

---

## What I learned today (in simple words)

- How **middleware** works in FastAPI
- Why we should **never expose errors** to users
- How to add **basic security headers**
- How to write **async API tests**
- Why **test coverage** matters
- How **real production projects** are structured

---

## Day 0 Status

- Day 0 completed successfully
- Security foundation ready
- Testing infrastructure ready
- Ready to start Day 1

---

## Next Steps (Day 1)

With the security and testing foundation in place, I'm ready to:
- Build real API endpoints
- Add database integration
- Implement authentication
- Create business logic

**Day 0 is the foundation. Day 1 is where the real development begins!** 