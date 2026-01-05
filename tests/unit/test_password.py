from app.services.user_service import pwd_context


def test_password_hash_and_verify():
    password = "Str0ngPass"
    hashed = pwd_context.hash(password)
    assert hashed != password
    assert pwd_context.verify(password, hashed) is True
    assert pwd_context.verify("wrong", hashed) is False
