import asyncio
from app.utils import get_logger
from app.tasks.update_artsits import fetch_artists_from_spotify_periodical

logger = get_logger(__name__)


class BackgroundRunner:
    def __init__(self, func):
        self.func = func
        self.period = 10

    async def run_background(self):
        while True:
            try:
                await self.func()
            except Exception as e:
                logger.exception(e)
            finally:
                await asyncio.sleep(self.period)


runner = BackgroundRunner(fetch_artists_from_spotify_periodical)
