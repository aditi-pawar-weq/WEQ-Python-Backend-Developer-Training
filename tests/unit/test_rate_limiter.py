from app.utils.rate_limiter import RateLimiter


def test_rate_limiter_blocks_after_limit():
    rl = RateLimiter(limit=5, window_seconds=60)
    key = "1.2.3.4"
    # first 5 allowed
    for _ in range(5):
        assert rl.allow(key) is True

    # 6th denied
    assert rl.allow(key) is False

    # reset allows again
    rl.reset(key)
    assert rl.allow(key) is True
