import copy

from datetime import datetime

from ..models.metadata import TrackMetadata, AlbumMetadata, ArtistMetadata
from ..utils.downloader import downloader



async def get_track_metadata(track_id, track_data, cover=None, thumbnail=None):
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
    )

    if track_data['version']:
        metadata.title += f' ({track_data["version"]})'

    parsed_date = datetime.strptime(track_data['streamStartDate'], '%Y-%m-%dT%H:%M:%S.%f%z')
    metadata.date = str(parsed_date.date())
    metadata.cover = await get_cover(track_data['album'].get('cover'), cover)
    metadata.thumbnail = await get_cover(track_data['album'].get('cover'), thumbnail, True)

    return metadata


async def get_album_metadata(album_id, a_meta, track_data, r_id):
    metadata = copy.deepcopy(base_meta)

    metadata['tempfolder'] += f"{r_id}-temp/"

    metadata['itemid'] = album_id
    metadata['albumartist'] = a_meta['artist']['name']
    metadata['upc'] = a_meta['upc']
    metadata['title'] = a_meta['title']
    if a_meta['version']:
        metadata['title'] += f' ({a_meta["version"]})'
    metadata['album'] = a_meta['title']
    metadata['artist'] = get_artists_name(a_meta)
    metadata['date'] = a_meta['releaseDate']
    metadata['totaltracks'] = a_meta['numberOfTracks']
    metadata['duration'] = a_meta['duration']
    metadata['copyright'] = a_meta['copyright']
    metadata['explicit'] = a_meta['explicit']
    metadata['totalvolume'] = a_meta['numberOfVolumes']
    metadata['provider'] = 'Tidal'
    metadata['type'] = 'album'

    metadata['cover'] = await get_cover(a_meta.get('cover'), metadata)
    metadata['thumbnail'] = await get_cover(a_meta.get('cover'), metadata, True)


    metadata['tracks'] = []
    for track in track_data['items']:
        track_meta = await get_track_metadata(track['id'], track, r_id, metadata['cover'], metadata['thumbnail'])
        metadata['tracks'].append(track_meta)
    
    return metadata


async def get_artistrack_datadata(a_meta:dict, r_id):
    metadata = copy.deepcopy(base_meta)

    metadata['tempfolder'] += f"{r_id}-temp/"

    metadata['artist'] = a_meta['name']
    metadata['title'] = a_meta['name']
    metadata['provider'] = 'Tidal'
    metadata['type'] = 'artist'
    metadata['cover'] = await get_cover(a_meta.get('picture'), metadata)
    metadata['thumbnail'] = await get_cover(a_meta.get('picture'), metadata, True)
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