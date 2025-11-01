from abc import ABC, abstractmethod
from pathlib import Path

from .metadata import *
from .task import TaskDetails
from ..utils.string import format_string


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
    async def get_metadata(cls, item_id: str, type_: str, task_details: TaskDetails) -> MetadataType:
        """
        Get the processed metadata according to the item type.

        Args:
            item_id: track | album | artist | playlist ID from the provider.
            type_: track | album | artist | playlist. 
            task_details: Details of the User task.

        """
        pass


    @classmethod
    @abstractmethod
    async def download_track(cls, metadata: TrackMetadata, task_details: TaskDetails, download_path: Optional[Path]) -> Optional[Path]:
        pass

    @classmethod
    @abstractmethod
    async def download_album(cls, metadata: AlbumMetadata, task_details: TaskDetails):
        pass

    @classmethod
    @abstractmethod
    async def download_artist(cls, metadata: ArtistMetadata, task_details: TaskDetails):
        pass

    @classmethod
    @abstractmethod
    async def download_playlist(cls, metadata: PlaylistMetadata, task_details: TaskDetails):
        pass

    @staticmethod
    def get_track_path(task_details: TaskDetails, track: TrackMetadata) -> Path:
        """Generate the full path for a track file (without extension)."""
        artist = format_string('artist', track)
        album = format_string('album', track)
        track_name = format_string('track', track)
        
        path = (
            task_details.dl_folder / 
            track.provider.title() /
            artist / 
            album / 
            f"{track_name}"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_album_dir(task_details: TaskDetails, album: AlbumMetadata) -> Path:
        """Generate the directory path for an album."""
        artist = format_string('artist', album)
        album_name = format_string('album', album)
        
        path = task_details.dl_folder / album.provider.title() / artist / album_name
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_artist_dir(task_details: TaskDetails, artist: ArtistMetadata) -> Path:
        """Generate the directory path for an artist."""
        artist_name = format_string('artist', artist)
        
        path = task_details.dl_folder / artist.provider.title() / artist_name
        path.mkdir(parents=True, exist_ok=True)
        return path




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
    async def get_cover(cls, cover_id: str, cover_folder: Path, thumbnail: bool = False) -> Path:
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