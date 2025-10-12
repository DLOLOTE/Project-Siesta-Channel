import asyncio

from pathlib import Path
from aiohttp import ClientSession, ClientTimeout, ClientError

from .errors import DownloadError, DownloadTimeout, DownloadExceedMaxRetry
from .models import TrackMetadata


class Downloader:
    def __init__(self):
        self.default_cover = Path('./project-siesta.png')

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


    async def create_cover_file(self, url: str, cover_id, filepath: Path, suffix=''):
        """
        Create JPEG files from URL
        Args:
            url (str): URL to be downloaded.
            data (Metadata): Metadata object.
            filepath (Path): Where to save the file.
            suffix (str): Use '-thumb' for thumbnails
        """
        cover_file = filepath / f"{cover_id}{suffix}.jpg"
        
        if not cover_file.exists():
            try:
                await self.download_file(url, cover_file, 1, 5)
            except:
                return self.default_cover
        return cover_file


downloader = Downloader()