# Testing Strategy

## Testing Pyramid
- Unit tests: 70%
- Integration tests: 20%
- UI tests: 10%

## Day 0 Scope
- Error handling tests
- Security middleware tests

## Auth testing (added)
- Unit tests: test the `UserService` and `AuthService` behaviors (password hashing, authenticate, token creation/validation).
- Integration tests: full register -> token -> protected endpoint flows using `httpx` and the test FastAPI app. These tests ensure middleware, response format, and DB wiring are correct.

## Running auth tests
- To run the full test suite including auth tests:

```bash
pytest -q
```

or run specific tests:

```bash
pytest tests/integration/test_auth_api.py -q
pytest tests/unit/test_auth_service.py -q
```

## Tools
- Pytest
- pytest-asyncio
- pytest-cov

## Fixtures & Test DB
- Tests use an async SQLite in-memory database fixture (see `tests/conftest.py`) which provides a clean DB per test run. When adding tests for auth, use the same `db` fixture to create users and verify login flows.

## Coverage Target
- Minimum 80%
