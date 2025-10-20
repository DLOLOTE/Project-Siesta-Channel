import asyncio
import zipfile
from pathlib import Path

from ..settings import bot_settings
from ..models.metadata import MetadataType

class ZipHandler:
    MAX_ZIP_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
    
    @classmethod
    async def should_zip(cls, metadata: MetadataType) -> bool:
        """Determine if content should be zipped based on type and settings."""
        if metadata.type_ == 'album':
            return bot_settings.album_zip
        elif metadata.type_ == 'playlist':
            return bot_settings.playlist_zip
        elif metadata.type_ == 'artist':
            return bot_settings.artist_zip
        return False
    

    @classmethod
    async def create_zip(cls, source_dir: Path, output_name: str, split: bool = False) -> list[Path]:
        """
        Create zip file(s) from source directory.
        
        Args:
            source_dir: Directory to zip
            output_name: Base name for zip file (without .zip extension)
            split: Whether to split into multiple files if size exceeds limit
        """
        if split:
            return await cls._create_split_zip(source_dir, output_name)
        else:
            return await cls._create_single_zip(source_dir, output_name)
    
    
    @classmethod
    async def _create_single_zip(cls, source_dir: Path, output_name: str) -> list[Path]:
        zip_path = source_dir.parent / f"{output_name}.zip"
        
        def _zip():
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in source_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(source_dir)
                        zipf.write(file_path, arcname)
        
        await asyncio.to_thread(_zip)
        return [zip_path]
    

    @classmethod
    async def _create_split_zip(cls, source_dir: Path, output_name: str) -> list[Path]:
        zip_parts = []
        current_part = 1
        current_size = 0
        current_zip_path = source_dir.parent / f"{output_name}_part{current_part}.zip"
        
        def _create_part():
            nonlocal current_part, current_size, current_zip_path
            
            zipf = zipfile.ZipFile(current_zip_path, 'w', zipfile.ZIP_DEFLATED)
            zip_parts.append(current_zip_path)
            
            for file_path in sorted(source_dir.rglob('*')):
                if not file_path.is_file():
                    continue
                
                file_size = file_path.stat().st_size
                
                if current_size + file_size > cls.MAX_ZIP_SIZE and current_size > 0:
                    zipf.close()
                    current_part += 1
                    current_size = 0
                    current_zip_path = source_dir.parent / f"{output_name}_part{current_part}.zip"
                    zipf = zipfile.ZipFile(current_zip_path, 'w', zipfile.ZIP_DEFLATED)
                    zip_parts.append(current_zip_path)
                
                arcname = file_path.relative_to(source_dir)
                zipf.write(file_path, arcname)
                current_size += file_size
            
            zipf.close()
        
        await asyncio.to_thread(_create_part)
        return zip_parts
    

    @staticmethod
    def get_zip_name(metadata: MetadataType) -> str:
        if metadata.type_ == 'album':
            return f"{metadata.artist} - {metadata.title}"
        elif metadata.type_ == 'playlist':
            return f"Playlist - {metadata.title}"
        elif metadata.type_ == 'artist':
            return f"Artist - {metadata.title}"
        return "download"