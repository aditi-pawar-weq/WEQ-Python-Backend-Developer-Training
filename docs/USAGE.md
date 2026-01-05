# Usage — Register, Get Token, Try Protected Endpoint

This quick guide shows how to register a user, obtain a JWT access token, and call a protected endpoint using either the Swagger UI or curl.

## 1) Start the app

```bash
uvicorn app.main:app --reload
```

API base: `http://127.0.0.1:8000`

## 2) Using Swagger (recommended for exploration)

1. Open `http://127.0.0.1:8000/docs`.
2. Use `POST /auth/register` to create a user. Example body:

```json
{
  "username": "alice",
  "password": "s3cret"
}
```

3. Use `POST /auth/token` with the same credentials to get a token. The response contains an `access_token`.

4. Click the "Authorize" button in the Swagger UI and paste:

```
Bearer <access_token>
```

5. Call any protected endpoint (for example `GET /protected`) — the request will include `request_id` and follow the standard response wrapper.

## 3) Using curl

Register:

```bash
curl -s -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"username":"alice","password":"s3cret"}' | jq
```

Get token:

```bash
curl -s -X POST http://127.0.0.1:8000/auth/token -H "Content-Type: application/json" -d '{"username":"alice","password":"s3cret"}' | jq
```

The token response looks like:

```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "token_type": "bearer"
  },
  "request_id": "..."
}
```

Call protected endpoint with the token:

```bash
curl -s -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/protected | jq
```

## Notes & Recommendations
- The training environment uses `sha256_crypt` for password hashing to avoid native `bcrypt` build issues. For production, switch to `bcrypt` and rotate secrets safely.
- JWT configuration lives in `app/config/settings.py`. Keep `JWT_SECRET` private and rotate it periodically.
- If you need to automate tests, use the test fixtures in `tests/conftest.py` which provide isolated databases for each run.
