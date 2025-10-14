from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


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