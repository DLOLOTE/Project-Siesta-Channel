from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from bot.helpers.translations import L

from bot.settings import bot_settings
from bot.utils.message import check_user, edit_message
from bot.buttons.settings import core_buttons
from bot.helpers.database.pg_impl import settings_db
from bot.models.uploader import UploaderTypes



@Client.on_callback_query(filters.regex(pattern=r"^corePanel"))
async def core_cb(c, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        await edit_message(
            cb.message,
            L.CORE_PANEL,
            core_buttons()
        )


@Client.on_callback_query(filters.regex(r"^upload"))
async def upload_mode_cb(client, cb: CallbackQuery):
    if not await check_user(cb.from_user.id, restricted=True):
        return

    modes = [UploaderTypes.LOCAL, UploaderTypes.TELEGRAM]
    if bot_settings.rclone:
        modes.append(UploaderTypes.RCLONE)

    current_index = (
        modes.index(bot_settings.upload_mode)
        if bot_settings.upload_mode in modes
        else 0
    )

    next_index = (current_index + 1) % len(modes)
    next_mode = modes[next_index]
    bot_settings.upload_mode = next_mode
    settings_db.set_variable('UPLOAD_MODE', next_mode.value)

    try:
        await core_cb(client, cb)
    except Exception:
        pass


@Client.on_callback_query(filters.regex(pattern=r"^linkOption"))
async def link_option_cb(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        options = ['False', 'Index', 'RCLONE', 'Both']
        current = options.index(bot_settings.link_options)
        nexti = (current + 1) % len(options)
        bot_settings.link_options = options[nexti]
        settings_db.set_variable('RCLONE_LINK_OPTIONS', options[nexti])
        try:
            await core_cb(client, cb)
        except:
            pass


@Client.on_callback_query(filters.regex(pattern=r"^albArt"))
async def alb_art_cb(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        art_post = bot_settings.art_poster
        art_post = False if art_post else True
        bot_settings.art_poster = art_post
        settings_db.set_variable('ART_POSTER', art_post)
        try:
            await core_cb(client, cb)
        except:
            pass

@Client.on_callback_query(filters.regex(pattern=r"^playCONC"))
async def playlist_conc_cb(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        play_conc = bot_settings.playlist_conc
        play_conc = False if play_conc else True
        bot_settings.playlist_conc = play_conc
        settings_db.set_variable('PLAYLIST_CONCURRENT', play_conc)
        try:
            await core_cb(client, cb)
        except:
            pass

@Client.on_callback_query(filters.regex(pattern=r"^artBATCH"))
async def artist_conc_cb(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        artist_batch = bot_settings.artist_batch
        artist_batch = False if artist_batch else True
        bot_settings.artist_batch = artist_batch
        settings_db.set_variable('ARTIST_BATCH_UPLOAD', artist_batch)
        try:
            await core_cb(client, cb)
        except:
            pass

@Client.on_callback_query(filters.regex(pattern=r"^sortPlay"))
async def playlist_sort_cb(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        sort = bot_settings.playlist_sort
        sort = False if sort else True
        bot_settings.playlist_sort = sort
        settings_db.set_variable('PLAYLIST_SORT', sort)
        try:
            await core_cb(client, cb)
        except:
            pass


@Client.on_callback_query(filters.regex(pattern=r"^playZip"))
async def playlist_zip_cb(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        option = bot_settings.playlist_zip
        option = False if option else True
        bot_settings.playlist_zip = option
        settings_db.set_variable('PLAYLIST_ZIP', option)
        try:
            await core_cb(client, cb)
        except:
            pass


@Client.on_callback_query(filters.regex(pattern=r"^sortLinkPlay"))
async def playlist_disable_zip_link(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        option = bot_settings.disable_sort_link
        option = False if option else True
        bot_settings.disable_sort_link = option
        settings_db.set_variable('PLAYLIST_LINK_DISABLE', option)
        try:
            await core_cb(client, cb)
        except:
            pass


@Client.on_callback_query(filters.regex(pattern=r"^artZip"))
async def artist_zip_cb(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        option = bot_settings.artist_zip
        option = False if option else True
        bot_settings.artist_zip = option
        settings_db.set_variable('ARTIST_ZIP', option)
        try:
            await core_cb(client, cb)
        except:
            pass


@Client.on_callback_query(filters.regex(pattern=r"^albZip"))
async def album_zip_cb(client, cb:CallbackQuery):
    if await check_user(cb.from_user.id, restricted=True):
        option = bot_settings.album_zip
        option = False if option else True
        bot_settings.album_zip = option
        settings_db.set_variable('ALBUM_ZIP', option)
        try:
            await core_cb(client, cb)
        except:
            pass