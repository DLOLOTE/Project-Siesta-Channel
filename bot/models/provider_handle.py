from abc import ABC, abstractmethod
from typing import Optional



class Provider(ABC):
    def __init__(self):
        self.provider: Optional[str] = None


    @abstractmethod
    async def start(self, url, task_details):
        pass


    @abstractmethod
    async def _download_track(self, metadata):
        pass


    @abstractmethod
    async def _download_album(self):
        pass

    
    @abstractmethod
    async def _download_artist(self):
        pass


    @abstractmethod
    async def _download_playlist(self):
        pass