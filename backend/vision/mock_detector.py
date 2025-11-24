import asyncio
import random
from typing import List

import httpx


class MockDetector:
    def __init__(self, api_base: str, spot_ids: List[int], interval_seconds: int = 5):
        self.api_base = api_base.rstrip("/")
        self.spot_ids = spot_ids
        self.interval_seconds = interval_seconds

    async def _tick(self, client: httpx.AsyncClient):
        for spot_id in self.spot_ids:
            status = random.choice(["free", "occupied", "unknown"])
            await client.put(
                f"{self.api_base}/spots/{spot_id}/status",
                json={"status": status},
                timeout=10.0,
            )

    async def run_forever(self):
        async with httpx.AsyncClient() as client:
            while True:
                await self._tick(client)
                await asyncio.sleep(self.interval_seconds)
