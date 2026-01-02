from bot.helpers.translations import L

from pyrogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup

main_button = [[Button(text=L.MAIN_MENU_BUTTON, callback_data="main_menu")]]
close_button = [[Button(text=L.CLOSE_BUTTON, callback_data="close")]]


def qb_button(qualities:dict):
    inline_keyboard = []
    for quality in qualities.values():
        inline_keyboard.append(
            [Button(text=quality, callback_data=f"qbQ_{quality.replace('✅', '')}")]
        )
    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)