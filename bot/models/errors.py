class CustomError(Exception):
    """Base class for all app-specific exceptions."""
    default_message = "An unexpected application error occurred."

    def __init__(self, message=None, *, code=None, **context):
        self.code = code
        self.context = context
        super().__init__(message or self.default_message)


class DownloadTimeout(CustomError):
    default_message = "DOWNLOADER: Download failed due to timeout"

class DownloadExceedMaxRetry(Exception):
    pass

class DownloadError(Exception):
    pass


class MetadataTypeError(CustomError):
    default_message = 'Metadata: Unidentified type of Item'


class NotAvailableForDownload(CustomError):
    default_message = 'Track not available to download.'