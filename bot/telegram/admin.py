from bot import CMD
from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers.translations import L

from bot.settings import bot_settings
from bot.utils.message import check_user
from bot.helpers.database.pg_impl import settings_db

from config import DEEZER_VARS, TIDAL_VARS, QOBUZ_VARS, Config


@Client.on_message(filters.command(CMD.BAN))
async def ban(c:Client, msg:Message):
    if await check_user(msg.from_user.id, restricted=True):
        try:
            _id = int(msg.text.split(" ", maxsplit=1)[1])
        except:
            await c.send_message(msg.chat.id, L.BAN_AUTH_FORMAT, reply_to_message_id=msg.reply_to_message_id)
            return

        user = False if str(_id).startswith('-100') else True
        if user:
            if _id in bot_settings.auth_users:
                bot_settings.auth_users.remove(_id)
                settings_db.set_variable('AUTH_USERS', str(bot_settings.auth_users))
            else: await c.send_message(msg.chat.id, L.USER_DOEST_EXIST, reply_to_message_id=msg.reply_to_message.id)
        else:
            if _id in bot_settings.auth_chats:
                bot_settings.auth_chats.remove(_id)
                settings_db.set_variable('AUTH_CHATS', str(bot_settings.auth_chats))
            else: await c.send_message(msg.chat.id, L.USER_DOEST_EXIST, reply_to_message_id=msg.reply_to_message.id)
        await c.send_message(msg.chat.id, L.BAN_ID.format(_id), reply_to_message_id=msg.reply_to_message.id)
        

@Client.on_message(filters.command(CMD.AUTH))
async def auth(c:Client, msg:Message):
    if await check_user(msg.from_user.id, restricted=True):
        try:
            _id = int(msg.text.split(" ", maxsplit=1)[1])
        except:
            await c.send_message(msg.chat.id, L.BAN_AUTH_FORMAT, reply_to_message_id=msg.reply_to_message_id)
            return

        user = False if str(id).startswith('-100') else True
        if user:
            if _id not in bot_settings.auth_users:
                bot_settings.auth_users.append(_id)
                settings_db.set_variable('AUTH_USERS', str(bot_settings.auth_users))
            else: await c.send_message(msg.chat.id, L.USER_EXIST, reply_to_message_id=msg.reply_to_message.id)
        else:
            if id not in bot_settings.auth_chats:
                bot_settings.auth_chats.append(id)
                settings_db.set_variable('AUTH_CHATS', str(bot_settings.auth_chats))
            else: await c.send_message(msg.chat.id, L.USER_EXIST, reply_to_message_id=msg.reply_to_message.id)
        await c.send_message(msg.chat.id, L.AUTH_ID, reply_to_message_id=msg.reply_to_message.id)


@Client.on_message(filters.command(CMD.LOG))
async def send_log(c:Client, msg:Message):
    if await check_user(msg.from_user.id, restricted=True):
        await c.send_document(
            msg.chat.id,
            './bot/bot_logs.log',
            reply_to_message_id=msg.reply_to_message.id
        )


@Client.on_message(filters.command(CMD.SETVAR))
async def set_var(c: Client, msg: Message):
    if not await check_user(msg.from_user.id, restricted=True):
        return

    try:
        _, var_name, *var_value = msg.text.split(maxsplit=2)
        var_value = ' '.join(var_value).strip()

        if not var_value:
            return await msg.reply("Missing value. Usage: `/setvar VAR_NAME value`", quote=True)

        setattr(Config, var_name, var_value)
        settings_db.set_variable(var_name, var_value)

        if var_name in DEEZER_VARS:
            try:
                await bot_settings.deezer.session.close()
            except: pass
            await bot_settings.login_deezer()
        if var_name in TIDAL_VARS:
            try:
                await bot_settings.tidal.session.close()
            except: pass
            await bot_settings.login_tidal()
        if var_name in QOBUZ_VARS:
            try:
                await bot_settings.qobuz.session.close()
            except: pass
            await bot_settings.login_qobuz()

        await msg.reply(f"✅ `{var_name}` updated and changes applied.", quote=True)

    except Exception as e:
        await msg.reply("Missing value. Usage: `/setvar VAR_NAME value`", quote=True)
