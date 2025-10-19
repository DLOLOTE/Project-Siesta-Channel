from datetime import datetime

from ..models.metadata import TrackMetadata, AlbumMetadata, ArtistMetadata
from ..utils.downloader import downloader

from .utils import sort_album_from_artist

from .tidal_api import tidalapi
from ..models.provider import MetadataHandler
from .errors import MetadataTypeError



class TidalMetadata(MetadataHandler):
    @classmethod
    async def get_metadata(cls, item_id, type_, task_details):
        if type_ == 'track':
            raw_data = await tidalapi.get_track(item_id)
            return await cls.process_track_metadata(item_id, raw_data, task_details.tempfolder)
        
        elif type_ == 'album':
            raw_data = await tidalapi.get_album(item_id)
            track_datas = await tidalapi.get_album_tracks(item_id)
            return await cls.process_album_metadata(item_id, raw_data, track_datas['items'], task_details.tempfolder)

        elif type_ == 'artist':
            raw_data = await tidalapi.get_artist(item_id)
            _album_datas = await tidalapi.get_artist_albums(item_id)
            _artist_eps = await tidalapi.get_artist_albums_ep_singles(item_id)
            album_datas = await sort_album_from_artist(_album_datas['items'])
            album_datas.extend(await sort_album_from_artist(_artist_eps['items']))
            return await cls.process_artist_metadata(raw_data, album_datas, task_details.tempfolder)

        else:
            raise MetadataTypeError


    @classmethod
    async def process_track_metadata(cls, track_id, track_data, cover_folder):
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
        metadata.cover = await cls.get_cover(track_data['album'].get('cover'), cover_folder)
        metadata.thumbnail = await cls.get_cover(track_data['album'].get('cover'), cover_folder, True)

        metadata._extra['media_tags'] = track_data['mediaMetadata']['tags']

        return metadata


    @classmethod
    async def process_album_metadata(cls, album_id, album_data, track_datas, cover_folder):
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
        metadata.cover = await cls.get_cover(album_data.get('cover'), cover_folder)
        metadata.thumbnail = await cls.get_cover(album_data.get('cover'), cover_folder, True)

        for track in track_datas:
            track_meta = await cls.process_track_metadata(track['id'], track, cover_folder)
            metadata.tracks.append(track_meta)
        
        return metadata


    @classmethod
    async def process_artist_metadata(cls, artist_data, album_datas, cover_folder):
        metadata = ArtistMetadata(
            artist=artist_data['name'],
            provider='tidal'
        )
        metadata.cover = await cls.get_cover(artist_data.get('picture'), cover_folder)
        metadata.thumbnail = await cls.get_cover(artist_data.get('picture'), cover_folder, True)
        metadata._extra['albums'] = album_datas
        return metadata


    @classmethod
    async def process_playlist_metadata(cls, track_datas, cover_folder):
        return await super().process_playlist_metadata(track_datas, cover_folder)


    @classmethod
    async def get_cover(cls, cover_id, cover_folder, thumbnail=False):
        if thumbnail:
            url = f'https://resources.tidal.com/images/{cover_id.replace("-", "/")}/80x80.jpg'
            suffix = '-thumb'
        else:
            url = f'https://resources.tidal.com/images/{cover_id.replace("-", "/")}/1280x1280.jpg'
            suffix = ''
        return await downloader.create_cover_file(url, cover_id, cover_folder, suffix)














def get_artists_name(meta:dict):
    artists = []
    for a in meta['artists']:
        artists.append(a['name'])
    return ', '.join([str(artist) for artist in artists])