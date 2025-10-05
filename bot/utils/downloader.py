import os
import asyncio

from pathlib import Path
from aiohttp import ClientSession, ClientTimeout, ClientError

from .errors import DownloadError, DownloadTimeout, DownloadExceedMaxRetry


class Downloader:
    def __init__(self):
        pass

    async def download_file(self, url: str, path: Path, retries=3, timeout=30):
        path.parent.mkdir(parents=True, exist_ok=True)
        
        for attempt in range(1, retries + 1):
            try:
                async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            with path.open("wb") as f:
                                while True:
                                    chunk = await response.content.read(1024 * 4)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                            return
                        else:
                            raise DownloadError(f"HTTP Status: {response.status}")
            except ClientError as e:
                if attempt == retries:
                    raise DownloadExceedMaxRetry("Connection failed after {retries} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except TimeoutError:
                if attempt == retries:
                    raise DownloadTimeout()
                await asyncio.sleep(2 ** attempt)