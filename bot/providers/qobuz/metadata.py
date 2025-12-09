import re
import hashlib

from bot.models.metadata import TrackMetadata, AlbumMetadata, ArtistMetadata
from bot.utils.downloader import downloader
from bot.models.provider import MetadataHandler



class QobuzMetadata(MetadataHandler):

    @classmethod
    async def process_track_metadata(cls, track_id, track_data, cover_folder):
        metadata = TrackMetadata(
            itemid=track_id,
            copyright=track_data['copyright'],
            albumartist=track_data['album']['artist']['name'],
            album=track_data['album']['title'],
            isrc=track_data['isrc'],
            title=track_data['title'],
            duration=track_data['duration'],
            explicit=track_data['parental_warning'],
            tracknumber=track_data['track_number'],
            date=track_data['release_date_original'],
            totaltracks=track_data['album']['tracks_count'],
            provider='Qobuz'
        )

        metadata.artist = cls.get_artists_name(track_data['album'])
        if track_data['version']:
            metadata.title += f' ({track_data["version"]})'

        metadata.cover = await cls.get_cover(track_data['album']['image']['large'], cover_folder)
        metadata.cover = await cls.get_cover(track_data['album']['image']['thumbnail'], cover_folder)

        return metadata



    @classmethod
    async def process_album_metadata(cls, album_id, album_data, cover_folder):
        metadata = AlbumMetadata(
            itemid=album_id,
            albumartist=
        )


    @staticmethod
    async def get_cover(cover_id, cover_folder, cover_type='track'):
        url = cover_id #qobuz directly gives url
        match = re.search(r"/covers/.+?/.+?/([a-zA-Z0-9]+)-", url)
        if match:
            cover_id = match.group(1)
        else:
            cover_id = hashlib.md5(url.encode()).hexdigest()
        return await downloader.create_cover_file(url, cover_id, cover_folder, '')


    @staticmethod
    def get_artists_name(meta:dict):
        artists = []
        try:
            for a in meta['artists']:
                artists.append(a['name'])
        except:
            artists.append(meta['artist']['name'])
        return ', '.join([str(artist) for artist in artists])