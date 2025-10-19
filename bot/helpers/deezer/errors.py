from ...models.errors import CustomError

class NotValidBfSecret(CustomError):
    default_message = 'DEEZER: Not a valid BF Secret given'


class InvalidCredentials(CustomError):
    default_message = 'DEEZER: Error while getting access tokem - Check your credentials'


class InvalidARL(CustomError):
    default_message = 'DEEZER: Invalid ARL provided'


class InvalidURL(Exception):
    pass


class APIError(Exception):
    def __init__(self, type, msg, payload):
        self.type = type
        self.msg = msg
        self.payload = payload

    def __str__(self):
        return f"DEEZER: {self.type}, {self.msg}, {str(self.payload)}"