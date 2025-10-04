from config import Config
from .logger import LOGGER

plugins = dict(
    root="bot/modules"
)

def _cmd(command: str) -> list[str]:
    return [command, f"{command}@{Config.BOT_USERNAME}"]

class CMD:
    START = _cmd("start")
    HELP = _cmd("help")
    SETTINGS = _cmd("settings")
    DOWNLOAD = _cmd("download")
    BAN = _cmd("ban")
    AUTH = _cmd("auth")
    LOG = _cmd("log")
    SETVAR = _cmd("setvar")

cmd = CMD()