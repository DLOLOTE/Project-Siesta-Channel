import base64

from dataclasses import asdict

from config import Config
from ..models.metadata import MetadataType


def sanitize_string(name: str) -> str:
    """Remove invalid characters from filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip()



def encrypt_string(string: str):
    s = bytes(string, 'utf-8')
    s = base64.b64encode(s)
    return s

def decrypt_string(string):
    try:
        s = base64.b64decode(string)
        s = s.decode()
        return s
    except:
        return string


def format_string(type_, metadata: MetadataType) -> str:
        """
        Format a template string with metadata values.
        Also sanitizes the result string.
        
        Args:
            type_: track | album | artist | playlist
            metadata: Dataclass of metadata values to substitute
            
        Returns:
            Formatted string
        """
        metadata_dict = asdict(metadata)
        
        templates = {
            'track': Config.TRACK_NAMING,
            'album': Config.ALBUM_NAMING,
            'artist': Config.ARTIST_NAMING,
            'playlist': Config.PLAYLIST_NAMING
        }

        string = templates[type_]
        formatted = string.format(**metadata_dict)
        formatted = ' '.join(formatted.split())  # Remove extra whitespace
        formatted = formatted.strip(' -')  # Remove leading/trailing spaces and dashes
        clean_string = sanitize_string(formatted)
        return clean_string