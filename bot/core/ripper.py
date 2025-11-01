from bot import Config
from ..models.task import TaskDetails
from ..models.provider import Provider
from ..models.metadata import *
from ..providers.tidal.handler import TidalHandler
from .uploader import get_uploader

PROVIDERS = {
    'tidal': TidalHandler
}


class Ripper:
    @classmethod
    async def start(cls, url: str, task_details: TaskDetails):
        provider = cls._get_provider(url)

        item_id, type_ = provider.parse_url(url)
        metadata = await provider.get_metadata(item_id, type_, task_details)

        if type_ == 'track':
            await cls._handle_track(provider, metadata, task_details)



    @classmethod
    def _get_provider(cls, url):
        for provider, prefixes in Config.PROVIDERS_LINK_FORMAT.items():
            if url.startswith(prefixes):
                provider_cls = PROVIDERS[provider]
                return provider_cls
        raise Exception('RIPPER: No handlers found for the link')


    @classmethod
    async def _handle_track(cls, provider: type[Provider], metadata: TrackMetadata, task_details: TaskDetails):
        track_path = await provider.download_track(metadata, task_details, None)
        if track_path:
            uploader = get_uploader()
            await uploader.upload(task_details, track_path, metadata)