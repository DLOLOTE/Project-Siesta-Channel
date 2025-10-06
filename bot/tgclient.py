from config import Config

from pyrogram import Client

from bot import LOGGER

plugins = dict(
    root="bot/telegram"
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Project-Siesta",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.TG_BOT_TOKEN,
            plugins=plugins,
            workdir=Config.WORK_DIR,
            workers=100
        )

    async def start(self):
        await super().start()
        LOGGER.info("BOT : Started Successfully")

    async def stop(self, *args):
        await super().stop()
        LOGGER.info('BOT : Exited Successfully ! Bye..........')

aio = Bot()