import asyncio
import time
from itertools import chain
from typing import Any

import httpx

from src.utils import TimestampMsWindow, split_time_window


class HyperLiquid:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def _request(
        self,
        method: str,
        url: str,
        req_json: Any | None = None,
        *,
        content_type: str = "application/json",
    ) -> httpx.Response:
        retries = 2

        while True:
            try:
                return await self._client.request(
                    method, url, json=req_json, headers={"Content-Type": content_type}
                )
            except httpx.RequestError:
                if retries == 0:
                    raise
                retries -= 1

    async def get_user_fills(
        self, user: str, time_window: TimestampMsWindow | None = None
    ):
        if time_window is None:
            time_window = (0, int(time.time() * 1000))

        resp = await self._request(
            "POST",
            "https://api.hyperliquid.xyz/info",
            {
                "type": "userFillsByTime",
                "user": user,
                "startTime": time_window[0],
                "endTime": time_window[1],
            },
        )
        resp.raise_for_status()
        fills = resp.json()
        if len(fills) == 2000:
            windows = split_time_window(time_window)
            if windows is None:
                return fills

            all_fills = await asyncio.gather(
                *(self.get_user_fills(user, win) for win in windows)
            )
            fills = list(chain.from_iterable(all_fills))

        return fills
