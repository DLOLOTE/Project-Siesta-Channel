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



if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_BASE_DIR):
        os.makedirs(Config.DOWNLOAD_BASE_DIR)
    load_dynamic_vars()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(load_clients())
    siesta.run()
    