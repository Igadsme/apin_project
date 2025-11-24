import asyncio
import os

from vision.mock_detector import MockDetector


API_BASE = os.getenv("APIN_API_BASE", "http://127.0.0.1:8000")
SPOT_IDS = list(range(1, 21))
INTERVAL_SECONDS = int(os.getenv("APIN_DETECTOR_INTERVAL", "5"))


async def main():
    detector = MockDetector(api_base=API_BASE, spot_ids=SPOT_IDS, interval_seconds=INTERVAL_SECONDS)
    print(f"Starting mock detector against {API_BASE} for spots {SPOT_IDS}")
    await detector.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
