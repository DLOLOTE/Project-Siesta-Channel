from bot.helpers.translations import L

from bot.settings import bot_settings
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_button = [[InlineKeyboardButton(text=L.MAIN_MENU_BUTTON, callback_data="main_menu")]]
close_button = [[InlineKeyboardButton(text=L.CLOSE_BUTTON, callback_data="close")]]

def main_menu():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=L.CORE,
                callback_data='corePanel'
            )
        ],
        [
            InlineKeyboardButton(
                text=L.TELEGRAM,
                callback_data='tgPanel'
            )
        ],
        [
            InlineKeyboardButton(
                text=L.PROVIDERS,
                callback_data='providerPanel'
            )
        ]
    ]
    inline_keyboard += close_button
    return InlineKeyboardMarkup(inline_keyboard)

def providers_button():
    inline_keyboard = []
    if bot_settings.qobuz:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=L.QOBUZ,
                    callback_data='qbP'
                )
            ]
        )
    if bot_settings.deezer:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=L.DEEZER,
                    callback_data='dzP'
                )
            ]
        )
    if bot_settings.can_enable_tidal:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=L.TIDAL,
                    callback_data='tdP'
                )
            ]
        )
    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)


def tg_button():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=L.BOT_PUBLIC.format(bot_settings.bot_public),
                callback_data='botPublic'
            )
        ],
        [
            InlineKeyboardButton(
                text=L.ANTI_SPAM.format(bot_settings.anti_spam),
                callback_data='antiSpam'
            )
        ],
        [
            InlineKeyboardButton(
                text=L.LANGUAGE,
                callback_data='langPanel'
            )
        ]
    ]

    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)


def core_buttons():
    inline_keyboard = []

    if bot_settings.rclone:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Return Link : {bot_settings.link_options}",
                    callback_data='linkOptions'
                )
            ]
        )

    inline_keyboard += [
        [
            InlineKeyboardButton(
                text=f"Upload : {bot_settings.upload_mode}",
                callback_data='upload'
            )
        ],
        [
            InlineKeyboardButton(
                text=L.SORT_PLAYLIST.format(bot_settings.playlist_sort),
                callback_data='sortPlay'
            ),
            InlineKeyboardButton(
                text=L.DISABLE_SORT_LINK.format(bot_settings.disable_sort_link),
                callback_data='sortLinkPlay'
            )
        ],
        [
            InlineKeyboardButton(
                text=L.PLAYLIST_ZIP.format(bot_settings.playlist_zip),
                callback_data='playZip'
            ),
            InlineKeyboardButton(
                text=L.PLAYLIST_CONC_BUT.format(bot_settings.playlist_conc),
                callback_data='playCONC'
            )
        ],
        [
            InlineKeyboardButton(
                text=L.ARTIST_BATCH_BUT.format(bot_settings.artist_batch),
                callback_data='artBATCH'
            ),
            InlineKeyboardButton(
                text=L.ARTIST_ZIP.format(bot_settings.artist_zip),
                callback_data='artZip'
            )
        ],
        [
            InlineKeyboardButton(
                text=L.ALBUM_ZIP.format(bot_settings.album_zip),
                callback_data='albZip'
            ),
            InlineKeyboardButton(
                text=L.POST_ART_BUT.format(bot_settings.art_poster),
                callback_data='albArt'
            )
        ]
    ]
    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)



def language_buttons(languages, selected):
    inline_keyboard = []
    for item in languages:
        text = f"{item.__language__} ✅" if item.__language__ == selected else item.__language__
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=text.upper(),
                    callback_data=f'langSet_{item.__language__}'
                )
            ]
        )
    inline_keyboard += main_button+ close_button
    return InlineKeyboardMarkup(inline_keyboard)


# tidal panel
def tidal_buttons():
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=L.AUTHORIZATION,
                callback_data='tdAuth'
            )
        ]
    ]

    if bot_settings.tidal:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=L.QUALITY,
                    callback_data='tdQ'
                )
            ]
        )

    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)

def tidal_auth_buttons():
    inline_keyboard = []
    if bot_settings.tidal:
        inline_keyboard += [
            [
                InlineKeyboardButton(
                    text=L.TIDAL_REMOVE_LOGIN,
                    callback_data=f'tdRemove'
                )
            ],
            [
                InlineKeyboardButton(
                    text=L.TIDAL_REFRESH_SESSION,
                    callback_data=f'tdFresh'
                )
            ]
        ]
    elif bot_settings.can_enable_tidal:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=L.TIDAL_LOGIN_TV,
                    callback_data=f'tdLogin'
                )
            ]
        )
    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)
    


# qobuz qualities
def qb_button(qualities:dict):
    inline_keyboard = []
    for quality in qualities.values():
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=quality,
                    callback_data=f"qbQ_{quality.replace('✅', '')}"
                )
            ]
        )
    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)

def tidal_quality_button(qualities:dict):
    inline_keyboard = []
    for quality in qualities.values():
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=quality,
                    callback_data=f"tdSQ_{quality.replace('✅', '')}"
                )
            ]
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                    text=F'SPATIAL : {bot_settings.tidal.spatial}',
                    callback_data=f"tdSQ_spatial"
                )
        ]
    )
    inline_keyboard += main_button + close_button
    return InlineKeyboardMarkup(inline_keyboard)