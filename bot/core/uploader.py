from pathlib import Path
from typing import Optional, AsyncIterator
import asyncio

from bot import Config
from ..models.uploader import Uploader
from ..settings import bot_settings
from ..utils.string import format_string





class RcloneUploader(Uploader):
    @classmethod
    async def upload(cls, task_details, filepath, metadata):
        relative_path = filepath.relative_to(task_details.dl_folder)
        await cls._rclone_upload(filepath)
    

    @staticmethod
    async def _rclone_upload(local_path: Path):
        cmd = f'rclone copy --config ./rclone.conf "{str(local_path)}" "{Config.RCLONE_DEST}"'
        task = await asyncio.create_subprocess_shell(cmd)
        await task.wait()




class TelegramUploader(Uploader):
    @classmethod
    async def upload(cls, task_details, filepath, metadata):
        if filepath.suffix == '.zip':
            caption = None
        else:
            pass

class LocalUploader:
    pass



def get_uploader() -> type[Uploader]:
    uploaders = {
        'rclone': RcloneUploader,
        'telegram': TelegramUploader,
        'local': LocalUploader,
    }
    return uploaders.get(bot_settings.upload_mode.lower(), TelegramUploader)