from abc import ABC, abstractmethod
from pathlib import Path
from .task import TaskDetails
from .metadata import MetadataType


class Uploader(ABC):
    @classmethod
    @abstractmethod
    async def upload(cls, task_details: TaskDetails, filepath: Path, metadata: MetadataType) -> Optional[str]:
        """
        Upload a single file / folder.
        
        Args:
            task_details: Task details
            filepath: Path to upload (can be audio file, folder or zip)
            metadata: Metadata for the file / folder
        """
        pass