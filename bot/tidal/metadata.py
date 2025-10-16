from datetime import datetime

from ..models.metadata import TrackMetadata, AlbumMetadata, ArtistMetadata, MetadataType
from ..utils.downloader import downloader

from .utils import sort_album_from_artist

from .tidal_api import tidalapi



async def get_metadata(item_id, type_, task_details) -> MetadataType | None:
    if type_ == 'track':
        raw_data = await tidalapi.get_track(item_id)
        return await process_track_metadata(item_id, raw_data, task_details.tempfolder)
    
    if type_ == 'album':
        raw_data = await tidalapi.get_album(item_id)
        track_datas = await tidalapi.get_album_tracks(item_id)
        return await process_album_metadata(item_id, raw_data, track_datas, task_details.tempfolder)

    if type_ == 'artist':
        raw_data = await tidalapi.get_artist(item_id)
        _album_datas = await tidalapi.get_artist_albums(item_id)
        _artist_eps = await tidalapi.get_artist_albums_ep_singles(item_id)
        album_datas = await sort_album_from_artist(_album_datas['items'])
        album_datas.extend(await sort_album_from_artist(_artist_eps['items']))
        return await process_artist_metadata(raw_data, album_datas, task_details.tempfolder)




async def process_track_metadata(track_id, track_data, task_folder):
    """
    Args:
        track_id (int): track id from Tidal
        track_data (dict, None): raw metadata from tidal
    """
    metadata = TrackMetadata(
        itemid=track_id,
        title=track_data['title'],
        copyright=track_data['copyright'],
        albumartist=track_data['artist']['name'],
        artist=get_artists_name(track_data),
        album=track_data['album']['title'],
        isrc=track_data['isrc'],
        duration=track_data['duration'],
        explicit=track_data['explicit'],
        tracknumber=track_data['trackNumber'],
        provider='tidal'
    )

    if track_data['version']:
        metadata.title += f' ({track_data["version"]})'

    parsed_date = datetime.strptime(track_data['streamStartDate'], '%Y-%m-%dT%H:%M:%S.%f%z')
    metadata.date = str(parsed_date.date())
    metadata.cover = await get_cover(track_data['album'].get('cover'), task_folder)
    metadata.thumbnail = await get_cover(track_data['album'].get('cover'), task_folder, True)

    metadata._extra['media_tags'] = track_data['mediaMetadata']['tags']

    return metadata


async def process_album_metadata(album_id, album_data, track_data, task_folder):
    metadata = AlbumMetadata(
        itemid=album_id,
        albumartist=album_data['artist']['name'],
        upc=album_data['upc'],
        title=album_data['title'],
        album=album_data['title'],
        date=album_data['releaseDate'],
        totaltracks=album_data['numberOfTracks'],
        duration=album_data['duration'],
        copyright=album_data['copyright'],
        explicit=album_data['explicit'],
        totalvolume=album_data['numberOfVolumes'],
        provider='tidal'
    )

    if album_data['version']:
        metadata.title += f' ({album_data["version"]})'

    metadata.artist = get_artists_name(album_data)
    metadata.cover = await get_cover(album_data.get('cover'), task_folder)
    metadata.thumbnail = await get_cover(album_data.get('cover'), task_folder, True)

    for track in track_data['items']:
        track_meta = await process_track_metadata(track['id'], track, task_folder)
        metadata.tracks.append(track_meta)
    
    return metadata


async def process_artist_metadata(artist_data, albums_datas, task_folder):
    metadata = ArtistMetadata(
        title=artist_data['name'],
        provider='tidal'
    )
    metadata.cover = await get_cover(artist_data.get('picture'), task_folder)
    metadata.thumbnail = await get_cover(artist_data.get('picture'), task_folder, True)
    metadata._extra['albums'] = albums_datas
    return metadata


async def get_cover(cover_id, cover_path, thumbnail=False):
    if thumbnail:
        url = f'https://resources.tidal.com/images/{cover_id.replace("-", "/")}/80x80.jpg'
        suffix = '-thumb'
    else:
        url = f'https://resources.tidal.com/images/{cover_id.replace("-", "/")}/1280x1280.jpg'
        suffix = ''
    return await downloader.create_cover_file(url, cover_id, cover_path, suffix)


def get_artists_name(meta:dict):
    artists = []
    for a in meta['artists']:
        artists.append(a['name'])
    return ', '.join([str(artist) for artist in artists])