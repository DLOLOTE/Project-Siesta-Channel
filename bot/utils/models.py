from dataclasses import dataclass, field
from typing import Optional
from pyrogram.types import Message
from pathlib import Path

from bot import Config


@dataclass
class TaskDetails:
    def __init__(self, message: Message, url):
        self.message: Message = message
        self.url: str = url

        self.bot_msg: Optional[Message] = None
        self.provider: Optional[str] = None
        self.tempfolder: Path = Path(Config.DOWNLOAD_BASE_DIR) / str(self.reply_to_message_id)
        self.tempfolder.mkdir(parents=True, exist_ok=True)


    @property
    def user_id(self) -> int:
        return self.message.from_user.id


    @property
    def chat_id(self) -> int:
        return self.message.chat.id


    @property
    def user_name(self) -> str:
        if self.message.from_user.username:
            return self.message.from_user.username 
        else:
            return self.message.from_user.first_name


    @property
    def reply_to_message_id(self) -> int:
        if self.message.reply_to_message:
            return self.message.reply_to_message.id
        else:
            return self.message.id



@dataclass
class _Metadata:
    itemid: int = 0
    title: str = ''
    provider: str = ''
    cover: Optional[Path] = None
    thumbnail: Optional[Path] = None


@dataclass
class _AudioMetadata(_Metadata):
    album: str = ''
    artist: str = ''
    duration: int = 0
    lyrics: str = ''
    tracknumber: int = 0
    totaltracks: int = 1
    albumartist: str = ''
    quality: str = ''
    explicit: str = ''
    genre: str = ''
    copyright: str = ''
    date: str = ''
    volume: int = 1


@dataclass
class TrackMetadata(_AudioMetadata):
    isrc: str = ''
    type_: str = 'track'


@dataclass
class AlbumMetadata(_AudioMetadata):
    upc: str = ''
    tracks: list[TrackMetadata] = field(default_factory=list)
    type_: str = 'album'


@dataclass
class ArtistMetadata(_Metadata):
    albums: list[AlbumMetadata] = field(default_factory=list)
    type_: str = 'artist'


@dataclass
class PlaylistMetadata(_Metadata):
    tracks: list[TrackMetadata] = field(default_factory=list)
    type_: str = 'playlist'


@dataclass
class ItemDirectories:
    filepath: Optional[Path] = None
    folderpath: Optional[Path] = None
    cover_path: Optional[Path] = None
    thumb_path: Optional[Path] = None