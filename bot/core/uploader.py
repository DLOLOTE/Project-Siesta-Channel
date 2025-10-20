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
        if filepath.is_dir():
            # simple hack to ensure the folder structure is preserved
            filepath = Config.DOWNLOAD_BASE_DIR / str(task_details.reply_to_message_id)
        await cls._rclone_upload(filepath)
    

    @staticmethod
    async def _rclone_upload(local_path: Path):
        """Execute rclone upload command."""
        if local_path.is_dir():
            cmd = [
                "rclone", 
                "copy", 
                "--config",
                "./rclone.conf",
                str(local_path), 
                Config.RCLONE_DEST
            ]
        else:
            cmd = [
                "rclone", 
                "copyto", 
                "--config",
                "./rclone.conf",
                str(local_path), 
                f"{Config.RCLONE_DEST}/{local_path.name}"
            ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()




class TelegramUploader(Uploader):
    @classmethod
    async def upload(cls, task_details, filepath, metadata):
        if filepath.suffix == '.zip':
            caption = None
        else:
            pass



def get_uploader() -> type[Uploader]:
    uploaders = {
        'rclone': RcloneUploader,
        'telegram': TelegramUploader,
        'local': LocalUploader,
    }
    return uploaders.get(bot_settings.upload_mode, TelegramUploader)