# Security Checklist

## Authentication & Authorization
- [x] JWT (implemented)

### JWT details
- Tokens are standard JSON Web Tokens (JWT) signed with the secret configured in `app/config/settings.py` (`JWT_SECRET`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`).
- Token creation and validation live in `app/services/auth_service.py`.
- Protected endpoints use FastAPI's `HTTPBearer` dependency (see `app/routers/protected.py`) so Swagger UI exposes an "Authorize" control to test Bearer tokens.

### Password hashing
- Passwords are hashed using `passlib`'s CryptContext. For the training/demo environment we use `sha256_crypt` to avoid native build issues in CI. This is acceptable for learning but NOT recommended for production.
- Recommendation for production: switch to `bcrypt` (update `UserService` CryptContext, and ensure the `bcrypt` wheel/native library is available in your deployment environment).

## Input Validation
- [ ] Strict schemas (Planned)

## Data Protection
- [x] No stack traces in responses
- [x] No secrets in logs

## API Security
- [x] Request ID tracking
- [x] Security headers
- [x] Swagger disabled in prod

## Infrastructure
- [x] .env not committed
- [x] .env.example provided
