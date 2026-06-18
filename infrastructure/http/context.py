from dataclasses import dataclass
from logging import Logger

import aiohttp


@dataclass
class HttpContext:
    logger: Logger
    _session: aiohttp.ClientSession | None = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            try:
                timeout = aiohttp.ClientTimeout(total=10)
                self._session = aiohttp.ClientSession(timeout=timeout)
            except Exception as e:
                self.logger.error(f"Failed to create aiohttp session: {e}")
                raise RuntimeError("HTTP Client initialization failed") from e
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
