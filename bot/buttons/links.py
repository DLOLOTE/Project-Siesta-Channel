from config import Config
from bot.helpers.translations import L
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def links_button(rclone, index):
    inline_keyboard = []

    if rclone:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=L.RCLONE_LINK,
                    url=rclone
                )
            ]
        )

    if index:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=L.INDEX_LINK,
                    url=index
                )
            ]
        )
    if inline_keyboard == []:
        return None
    return InlineKeyboardMarkup(inline_keyboard)