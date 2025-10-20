from dataclasses import dataclass
from typing import Optional
from pyrogram.types import Message
from pathlib import Path
from bot import Config


class TaskDetails:
    def __init__(self, message: Message, url):
        self.message: Message = message
        self.url: str = url

        self.bot_msg: Optional[Message] = None
        self.provider: Optional[str] = None

        self.dl_folder: Path = Config.DOWNLOAD_BASE_DIR / str(self.reply_to_message_id)
        self.dl_folder.mkdir(parents=True, exist_ok=True)
        self.tempfolder: Path = Config.DOWNLOAD_BASE_DIR / f"{self.reply_to_message_id}-temp"
        self.tempfolder.mkdir(parents=True, exist_ok=True)
        self.type_: Optional[str] = None


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