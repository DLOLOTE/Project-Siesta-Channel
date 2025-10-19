from ...models.errors import CustomError


class FreeAccountError(CustomError):
    default_message = 'QOBUZ : Free accounts are not eligible to download tracks'

class NoValidSecret(CustomError):
    default_message = "QOBUZ : Cant find any valid app secret"

class InvalidQualityId(CustomError):
    default_message = 'QOBUZ : Invalid quality id'

class InvalidCredentials(Exception):
    pass