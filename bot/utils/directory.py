from config import Config
from ..models.task import TaskDetails



def get_task_dir(task_details: TaskDetails):
    folderpath = Config.DOWNLOAD_BASE_DIR / str(task_details.reply_to_message_id)
    return folderpath