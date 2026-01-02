import shutil

from pyrogram.types import Message
from pyrogram import Client, filters

from bot import LOGGER, CMD, Config

from ..helpers.translations import L
from ..utils.message import send_text, antiSpam, check_user
from ..models.task import TaskDetails
from ..core.ripper import Ripper


@Client.on_message(filters.command(CMD.DOWNLOAD))
async def download_track(c, msg: Message):
    if await check_user(msg=msg):
        try:
            if msg.reply_to_message:
                url = msg.reply_to_message.text
            else:
                url = msg.text.split(" ", maxsplit=1)[1]
        except:
            return await msg.reply_text(L.ERR_NO_LINK, reply_to_message_id=msg.id)

        if not url:
            return await msg.reply_text(L.ERR_LINK_RECOGNITION, reply_to_message_id=msg.id)
    
        spam = await antiSpam(msg.from_user.id, msg.chat.id)
        if not spam:
            task_details = TaskDetails(msg, url)
            task_details.bot_msg = await send_text(L.DOWNLOADING, task_details)

            try:
                await Ripper.start(url, task_details)
                await send_text(L.TASK_COMPLETED, task_details)
            except Exception as e:
                LOGGER.error(e)

            try:
                await c.delete_messages(msg.chat.id, task_details.bot_msg.id)
            except:
                pass

            shutil.rmtree(f"{Config.DOWNLOAD_BASE_DIR}/{task_details.reply_to_message_id}/", ignore_errors=True)
            shutil.rmtree(f"{Config.DOWNLOAD_BASE_DIR}/{task_details.reply_to_message_id}-temp/", ignore_errors=True)

            await antiSpam(msg.from_user.id, msg.chat.id, True)