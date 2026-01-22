import os
import shutil
import asyncio

from ..settings import bot_set
from .message import send_message, edit_message
from .utils import *
from ..config import Config  # Config file ကို ခေါ်သုံးဖို့ လိုပါတယ်

#
#  TASK HANDLER
#

async def track_upload(metadata, user, disable_link=False):
    if bot_set.upload_mode == 'Local':
        await local_upload(metadata, user)
    elif bot_set.upload_mode == 'Telegram':
        await telegram_upload(metadata, user)
    else:
        rclone_link, index_link = await rclone_upload(user, metadata['filepath'])
        if not disable_link:
            await post_simple_message(user, metadata, rclone_link, index_link)

    try:
        os.remove(metadata['filepath'])
    except FileNotFoundError:
        pass

async def album_upload(metadata, user):
    if bot_set.upload_mode == 'Local':
        await local_upload(metadata, user)
    elif bot_set.upload_mode == 'Telegram':
        if bot_set.album_zip:
            for item in metadata['folderpath']:
                # User ဆီ ပို့ခြင်း
                await send_message(user, item, 'doc', caption=await create_simple_text(metadata, user))
                # Channel Dump ဆီ ပို့ခြင်း (Zip file ဖြစ်လျှင်)
                if hasattr(Config, 'DUMP_CHANNEL_ID') and Config.DUMP_CHANNEL_ID:
                    await send_message(user, item, 'doc', caption=await create_simple_text(metadata, user), chat_id=Config.DUMP_CHANNEL_ID)
        else:
            await batch_telegram_upload(metadata, user)
    else:
        rclone_link, index_link = await rclone_upload(user, metadata['folderpath'])
        if metadata['poster_msg']:
            try:
                await edit_art_poster(metadata, user, rclone_link, index_link, await format_string(lang.s.ALBUM_TEMPLATE, metadata, user))
            except MessageNotModified:
                pass
        else:
            await post_simple_message(user, metadata, rclone_link, index_link)

    await cleanup(None, metadata)

async def artist_upload(metadata, user):
    if bot_set.upload_mode == 'Local':
        await local_upload(metadata, user)
    elif bot_set.upload_mode == 'Telegram':
        if bot_set.artist_zip:
            for item in metadata['folderpath']:
                await send_message(user, item, 'doc', caption=await create_simple_text(metadata, user))
                # Channel Dump ဆီ ပို့ခြင်း
                if hasattr(Config, 'DUMP_CHANNEL_ID') and Config.DUMP_CHANNEL_ID:
                    await send_message(user, item, 'doc', caption=await create_simple_text(metadata, user), chat_id=Config.DUMP_CHANNEL_ID)
        else:
            pass # artist telegram uploads are handled by album function
    else:
        rclone_link, index_link = await rclone_upload(user, metadata['folderpath'])
        if metadata['poster_msg']:
            try:
                await edit_art_poster(metadata, user, rclone_link, index_link, await format_string(lang.s.ARTIST_TEMPLATE, metadata, user))
            except MessageNotModified:
                pass
        else:
            await post_simple_message(user, metadata, rclone_link, index_link)

    await cleanup(None, metadata)

async def playlist_upload(metadata, user):
    if bot_set.upload_mode == 'Local':
        await local_upload(metadata, user)
    elif bot_set.upload_mode == 'Telegram':
        if bot_set.playlist_zip:
            for item in metadata['folderpath']:
                await send_message(user, item, 'doc', caption=await create_simple_text(metadata, user))
                if hasattr(Config, 'DUMP_CHANNEL_ID') and Config.DUMP_CHANNEL_ID:
                    await send_message(user, item, 'doc', caption=await create_simple_text(metadata, user), chat_id=Config.DUMP_CHANNEL_ID)
        else:
            await batch_telegram_upload(metadata, user)
    else:
        # Rclone logic များကို မပြင်ဘဲ ထားရှိပါသည်
        rclone_link, index_link = await rclone_upload(user, metadata['folderpath'])
        await post_simple_message(user, metadata, rclone_link, index_link)

#
#  CORE
#

async def telegram_upload(track, user):
    """
    သီချင်းတစ်ပုဒ်ချင်းစီကို User ဆီရော၊ Channel Dump ဆီရော ပို့ပေးမည်။
    """
    # ၁။ User ဆီ အရင်ပို့မည်
    await send_message(user, track['filepath'], 'audio', meta=track)
    
    # ၂။ Channel Dump ID ရှိခဲ့လျှင် Channel ဆီ ထပ်ပို့မည်
    if hasattr(Config, 'DUMP_CHANNEL_ID') and Config.DUMP_CHANNEL_ID:
        try:
            # chat_id parameter သုံးပြီး dump channel ဆီ လှမ်းပို့ခြင်း
            await send_message(user, track['filepath'], 'audio', meta=track, chat_id=Config.DUMP_CHANNEL_ID)
        except Exception as e:
            print(f"Dump Error: {e}")

async def batch_telegram_upload(metadata, user):
    if metadata['type'] == 'album' or metadata['type'] == 'playlist':
        for track in metadata['tracks']:
            try:
                await telegram_upload(track, user)
            except FileNotFoundError:
                pass
    elif metadata['type'] == 'artist':
        for album in metadata['albums']:
            for track in album['tracks']:
                await telegram_upload(track, user)

async def rclone_upload(user, realpath):
    path = f"{Config.DOWNLOAD_BASE_DIR}/{user['r_id']}/"
    cmd = f'rclone copy --config ./rclone.conf "{path}" "{Config.RCLONE_DEST}"'
    task = await asyncio.create_subprocess_shell(cmd)
    await task.wait()
    r_link, i_link = await create_link(realpath, Config.DOWNLOAD_BASE_DIR + f"/{user['r_id']}/")
    return r_link, i_link

async def local_upload(metadata, user):
    to_move = f"{Config.DOWNLOAD_BASE_DIR}/{user['r_id']}/{metadata['provider']}"
    destination = os.path.join(Config.LOCAL_STORAGE, os.path.basename(to_move))
    if os.path.exists(destination):
        for item in os.listdir(to_move):
            src_item = os.path.join(to_move, item)
            dest_item = os.path.join(destination, item)
            if os.path.isdir(src_item):
                if not os.path.exists(dest_item):
                    shutil.copytree(src_item, dest_item)
            else:
                shutil.copy2(src_item, dest_item)
    else:
        shutil.copytree(to_move, destination)
    shutil.rmtree(to_move)
