from bot.helpers.translations import L

from bot.settings import bot_settings
from pyrogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup

main_button = [[Button(text=L.MAIN_MENU_BUTTON, callback_data="main_menu")]]
close_button = [[Button(text=L.CLOSE_BUTTON, callback_data="close")]]

def tidal_buttons():
    inline_keyboard = [
        [Button(text=L.AUTHORIZATION, callback_data='tdAuth')]
    ]

    if bot_settings.tidal:
        inline_keyboard.append(
            [Button(text=L.QUALITY, callback_data='tdQ')])

    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)

def tidal_auth_buttons():
    inline_keyboard = []
    if bot_settings.tidal:
        inline_keyboard += [
            [Button(text=L.TIDAL_REMOVE_LOGIN, callback_data=f'tdRemove')],
            [Button(text=L.TIDAL_REFRESH_SESSION, callback_data=f'tdFresh')]
        ]
    elif bot_settings.can_enable_tidal:
        inline_keyboard.append(
            [Button(text=L.TIDAL_LOGIN_TV, callback_data=f'tdLogin')]
        )
    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)


def tidal_quality_button(qualities:dict):
    inline_keyboard = []
    for quality in qualities.values():
        inline_keyboard.append(
            [Button(text=quality,callback_data=f"tdSQ_{quality.replace('✅', '')}")]
        )

    inline_keyboard.append(
        [Button(text=F'SPATIAL : {bot_settings.tidal.spatial}',callback_data=f"tdSQ_spatial")]
    )
    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)