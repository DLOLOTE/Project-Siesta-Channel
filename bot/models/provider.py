from abc import ABC, abstractmethod
from pathlib import Path

from .metadata import *
from .task import TaskDetails


class Provider(ABC):

    @classmethod
    @abstractmethod
    def parse_url(cls, url: str) -> tuple[str, str]:
        """
        Get item id and type from the URL 
        
        Returns:
            item_id: Item ID
            type_: Type of URL
        """
        pass


    @classmethod
    @abstractmethod
    async def get_track_metadata(cls, item_id: str, task_details: TaskDetails) -> TrackMetadata:
        pass

    @classmethod
    @abstractmethod
    async def get_album_metadata(cls, item_id: str, task_details: TaskDetails) -> AlbumMetadata:
        pass

    @classmethod
    @abstractmethod
    async def get_artist_metadata(cls, item_id: str, task_details: TaskDetails) -> ArtistMetadata:
        pass

    @classmethod
    @abstractmethod
    async def get_playlist_metadata(cls, item_id: str, task_details: TaskDetails) -> PlaylistMetadata:
        pass


    @classmethod
    @abstractmethod
    async def download_track(cls, metadata: TrackMetadata, task_details: TaskDetails, download_path: Path) -> Path:
        pass




class MetadataHandler(ABC):
    @classmethod
    @abstractmethod
    async def process_track_metadata(cls, track_id: str, track_data: dict, cover_folder: Path) -> MetadataType:
        """
        Processes track metadata from raw track data from provider.

        Args:
            track_id: track ID from the provider.
            track_data: raw data in dict.
            cover_folder: folder to save the cover / thumbnail files.

        """
        pass


    @classmethod
    @abstractmethod
    async def process_album_metadata(cls, album_id: str, album_data: dict, track_datas: list[dict], cover_folder: Path) -> MetadataType:
        """
        Processes album metadata from raw album data from provider.

        Args:
            album_id: track ID from the provider.
            album_data: raw data in dict.
            track_datas: list of raw track data
            cover_folder: folder to save the cover / thumbnail files.

        """
        pass


    @classmethod
    @abstractmethod
    async def process_artist_metadata(cls, artist_data: dict, album_datas: list[dict], cover_folder: Path) -> MetadataType:
        """
        Processes artist metadata from raw artist data from provider.

        Args:
            artist_data: raw data in dict.
            album_datas: list of raw album datas
            cover_folder: folder to save the cover / thumbnail files.

        """
        pass


    @classmethod
    @abstractmethod
    async def process_playlist_metadata(cls, track_datas: list[dict], cover_folder: Path) -> MetadataType:
        """
        Processes track metadata from raw playlist data from provider.

        Args:
            track_datas: list of raw track data in dict.
            cover_folder: folder to save the cover / thumbnail files.

        """
        pass


    @classmethod
    @abstractmethod
    async def get_cover(cls, cover_id: str, cover_folder: Path, cover_type: str = 'track') -> Path:
        """
        Fetches or creates a cover file for the given cover ID.
        
        Args:
            cover_id: Service-specific cover identifier or URL.
            cover_folder: Local folder to save the cover.
            thumbnail: Whether to save as thumbnail version.
        
        Returns:
            Path to the saved cover file.
        """
        pass