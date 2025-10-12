import shutil

from pyrogram.types import Message
from pyrogram import Client, filters

from bot import LOGGER, CMD, Config

from ..helpers.translations import L
from ..helpers.qobuz.handler import start_qobuz
from ..tidal.handler import start_tidal
from ..helpers.deezer.handler import start_deezer
from ..utils.message import send_message, antiSpam, check_user
from ..utils.models import TaskDetails



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
            task_details.bot_msg = await send_message(task_details,'text', text=L.DOWNLOADING)

            try:
                await start_link(url, task_details)
                await send_message(task_details, 'text', text=L.TASK_COMPLETED)
            except Exception as e:
                LOGGER.error(e)

            await c.delete_messages(msg.chat.id, task_details.bot_msg.id)

            shutil.rmtree(f"{Config.DOWNLOAD_BASE_DIR}/{task_details.reply_to_message_id}/", ignore_errors=True)
            shutil.rmtree(f"{Config.DOWNLOAD_BASE_DIR}/{task_details.reply_to_message_id}-temp/", ignore_errors=True)

            await antiSpam(msg.from_user.id, msg.chat.id, True)


async def start_link(url: str, task_details: TaskDetails):
    for provider, prefixes in Config.PROVIDERS_LINK_FORMAT.items():
        if url.startswith(prefixes):
            task_details.provider = provider.capitalize()
            return await globals()[f"start_{provider}"](url, task_details)

    return None