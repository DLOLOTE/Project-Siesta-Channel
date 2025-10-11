from dataclasses import dataclass
from pyrogram.types import Message


@dataclass
class TaskDetails:
    def __init__(self, message: Message, url):
        self.message: Message = message
        self.url: str = url

        self.bot_msg: Message | None = None
        self.provider: str | None = None


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