import os
import json

import requests

from .helpers.translations import set_lang

from config import Config
from bot.logger import LOGGER

from .helpers.database.pg_impl import settings_db
from .helpers.tidal.tidal_api import tidalapi


# For simple boolean values
def __getvalue__(var: str) -> bool:
    value, _ = settings_db.get_variable(var)
    return True if value else False





class BotSettings:
    def __init__(self):
        self.deezer = False
        self.qobuz = False
        self.tidal = None
        self.admins = Config.ADMINS

        db_lang, _ = settings_db.get_variable('BOT_LANGUAGE')
        set_lang(db_lang)

        db_users, _ = settings_db.get_variable('AUTH_USERS')
        self.auth_users = json.loads(db_users) if db_users else []
        db_chats, _ = settings_db.get_variable('AUTH_CHATS')
        self.auth_chats = json.loads(db_chats) if db_chats else []

        self.rclone = False
        self.check_upload_mode()

        spam, _ = settings_db.get_variable('ANTI_SPAM') #string
        self.anti_spam = spam if spam else 'OFF'

        self.bot_public = __getvalue__('BOT_PUBLIC')

        # post photo of album/artist
        self.art_poster = __getvalue__('ART_POSTER')

        self.playlist_sort = __getvalue__('PLAYLIST_SORT')
        # disable returning links for sorted playlist for cleaner chat
        self.disable_sort_link = __getvalue__('PLAYLIST_LINK_DISABLE')

        # Multithreaded downloads
        self.artist_batch = __getvalue__('ARTIST_BATCH_UPLOAD')
        self.playlist_conc = __getvalue__('PLAYLIST_CONCURRENT')
        
        link_option, _ = settings_db.get_variable('RCLONE_LINK_OPTIONS') #str
        self.link_options = link_option if self.rclone and link_option else 'False'

        self.album_zip = __getvalue__('ALBUM_ZIP')
        self.playlist_zip = __getvalue__('PLAYLIST_ZIP')
        self.artist_zip = __getvalue__('ARTIST_ZIP')

        self.clients = []


    def check_upload_mode(self):
        if os.path.exists('rclone.conf'):
            self.rclone = True
        elif Config.RCLONE_CONFIG:
            if Config.RCLONE_CONFIG.startswith('http'):
                rclone = requests.get(Config.RCLONE_CONFIG, allow_redirects=True)
                if rclone.status_code != 200:
                    LOGGER.info("RCLONE : Error retreiving file from Config URL")
                    self.rclone = False
                else:
                    with open('rclone.conf', 'wb') as f:
                        f.write(rclone.content)
                    self.rclone = True
            
        db_upload, _ = settings_db.get_variable('UPLOAD_MODE')
        if self.rclone and db_upload == 'RCLONE':
            self.upload_mode = 'RCLONE'
        elif db_upload == 'Telegram' or db_upload == 'Local':
            self.upload_mode = db_upload
        else:
            self.upload_mode = 'Local'
    

    


    async def login_tidal(self):
        # Check if Tidal is enabled
        self.can_enable_tidal = Config.ENABLE_TIDAL
        if not self.can_enable_tidal:
            return

        data = None
        # Refresh token in env is given preference
        if Config.TIDAL_REFRESH_TOKEN:
            data = {
                'user_id': None, 
                'refresh_token': Config.TIDAL_REFRESH_TOKEN, 
                'country_code': Config.TIDAL_COUNTRY_CODE
            }
            LOGGER.debug("TIDAL: Using refresh token from environment")
        else:
            # Try to get saved authentication data
            _, saved_info = settings_db.get_variable("TIDAL_AUTH_DATA")
            if saved_info:
                try:
                    data = json.loads(__decrypt_string__(saved_info))
                    LOGGER.debug("TIDAL: Using saved authentication data from Database")
                except Exception as e:
                    LOGGER.error(f"TIDAL: Failed to decrypt/parse saved auth data: {e}")
                    return

        if not data:
            return

        # Attempt login
        await tidalapi.login_from_saved(data)
        
        # Set audio quality
        quality, _ = settings_db.get_variable('TIDAL_QUALITY')
        if quality:
            tidalapi.quality = quality
        
        # Set spatial audio
        spatial, _ = settings_db.get_variable('TIDAL_SPATIAL')
        if spatial:
            tidalapi.spatial = spatial
        
        # Set instance variables
        self.tidal = tidalapi 
        self.clients.append(tidalapi)


    async def save_tidal_login(self, session):
        data = {
            "user_id" : session.user_id,
            "refresh_token" : session.refresh_token,
            "country_code" : session.country_code
        }

        txt = json.dumps(data)
        settings_db.set_variable("TIDAL_AUTH_DATA", 0, True, __encrypt_string__(txt))


bot_set = BotSettings()