from bot import CMD
from pyrogram import Client, filters
from pyrogram.types import Message

from ..helpers.translations import L

@Client.on_message(filters.command(CMD.START))
async def start(bot, msg: Message):
    await msg.reply_text(
        L.WELCOME_MSG.format(
            msg.from_user.first_name
        ),
        reply_to_message_id=msg.id
    )