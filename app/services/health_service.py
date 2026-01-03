from datetime import datetime, timezone


class HealthService:

    async def ping(self):
        return {"status": "ok"}

    async def live(self):
        return {
            "status": "live",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    async def ready(self):
        # Later we will add DB check
        return {"status": "ready"}
