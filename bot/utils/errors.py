class CustomError(Exception):
    """Base class for all app-specific exceptions."""
    default_message = "An unexpected application error occurred."

    def __init__(self, message=None, *, code=None, **context):
        self.code = code
        self.context = context
        super().__init__(message or self.default_message)