from datetime import datetime, timezone
from app.config.settings import settings


class ServiceInfoService:

    async def get_info(self):
        return {
            "name": settings.APP_NAME,
            "environment": settings.ENV,
            "version": "1.0.0"
        }

    async def get_time(self):
        return {
            "server_time": datetime.now(timezone.utc).isoformat()
        }
