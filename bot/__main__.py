import asyncio
import os

from config import Config, DYNAMIC_VARS

from .tgclient import siesta
from .loader import load_clients
from .helpers.database.pg_impl import settings_db



def load_dynamic_vars():
    for var in DYNAMIC_VARS:
        if not getattr(Config, var):
            setattr(Config, var, settings_db.get_variable(var)[0])

async def main():
    if not os.path.isdir(Config.DOWNLOAD_BASE_DIR):
        os.makedirs(Config.DOWNLOAD_BASE_DIR)

    load_dynamic_vars()

    await siesta.start()
    await load_clients()     
    await siesta.idle()        
    await siesta.stop()

asyncio.run(main())