import asyncio

from pathlib import Path
from pyrogram.types import Message
from pyrogram.errors import MessageNotModified, FloodWait

from bot.tgclient import siesta
from bot.settings import bot_settings

from ..models.task import TaskDetails

from bot import LOGGER


current_user = set()


async def check_user(uid=None, msg=None, restricted: bool = False) -> bool:
    """
    Check whether a user or chat has access.

    Args:
        uid (int, optional): User ID (used when `restricted` is True).
        msg (pyrogram.types.Message, optional): Pyrogram message object, used to extract chat/user IDs.
        restricted (bool, optional): If True, restricts access to bot admins only.

    Returns:
        bool: True if access is allowed, False otherwise.
    """
    if restricted:
        return uid in bot_settings.admins

    if bot_settings.bot_public:
        return True

    all_allowed = set(bot_settings.admins) | set(bot_settings.auth_chats) | set(bot_settings.auth_users)
    if not msg:
        return False

    return msg.from_user.id in all_allowed or msg.chat.id in all_allowed


async def antiSpam(uid: int = None, cid: int = None, revoke: bool = False) -> bool:
    """
    Check or update anti-spam status for a user or chat.

    Args:
        uid (int, optional): User ID (used if anti-spam mode is 'USER').
        cid (int, optional): Chat ID (used if anti-spam mode is 'CHAT+').
        revoke (bool, optional): If True, removes the ID from anti-spam tracking.

    Returns:
        bool: True if currently in spam/waiting mode, False otherwise.
    """
    mode = bot_settings.anti_spam
    key = cid if mode == "CHAT+" else uid

    if key is None:
        return False

    global current_user

    if revoke:
        current_user.discard(key)
        return False

    if key in current_user:
        return True

    current_user.add(key)
    return False



async def send_message(task_details: "TaskDetails", type_: str, chat_id: int | None = None, \
    markup=None, caption=None, metadata=None, **kwargs):
    """
    Unified sender for different content types.

    Args:
        task_details: TaskDetails object
        type_: One of 'text', 'doc', 'audio', etc.
        chat_id: Optional chat ID override
        markup: Optional reply markup
        caption: Optional caption
        metadata: Optional metadata (used for audio, etc.)
        kwargs: Any other Pyrogram send_* arguments
    """
    chat_id = chat_id or task_details.chat_id
    reply_to = task_details.reply_to_message_id

    send_map = {
        "text": "send_message",
        "doc": "send_document",
        "audio": "send_audio",
    }

    params = {
        "chat_id": chat_id,
        "reply_to_message_id": reply_to,
        "reply_markup": markup,
    }

    if type_ == "text":
        params.update(text=kwargs.get("text"), disable_web_page_preview=True)
    elif type_ == "doc":
        params.update(document=kwargs.get("doc"), caption=caption)
    elif type_ == "audio":
        params.update(
            audio=kwargs.get("audio"),
            caption=caption,
            duration=metadata.duration,
            performer=metadata.artist,
            title=metadata.title,
            thumb=metadata.thumbnail,
        )

    method = getattr(siesta, send_map[type_])

    retries = 3
    for attempt in range(retries):
        try:
            msg = await method(**params)
            return msg
        except FloodWait as e:
            wait_time = e.value
            LOGGER.info(f"TELEGRAM: [FloodWait] Sleeping for {wait_time}s before retrying (attempt {attempt+1}/{retries})")
            await asyncio.sleep(wait_time)
        except Exception as e:
            LOGGER.info(f"[Error] Failed to send {type_}: {e}")
            if attempt + 1 == retries:
                raise  # re-raise last error

    return None


async def edit_message(msg:Message, text, markup=None, antiflood=True):
    try:
        edited = await msg.edit_text(
            text=text,
            reply_markup=markup,
            disable_web_page_preview=True
        )
        return edited
    except MessageNotModified:
        return None
    except FloodWait as e:
        if antiflood:
            await asyncio.sleep(e.value)
            return await edit_message(msg, text, markup, antiflood)
        else:
            return None