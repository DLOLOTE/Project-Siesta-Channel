from bot.utils.errors import CustomError


class InvalidAPIResponse(CustomError):
    pass


class RegionLocked(CustomError):
    pass


class InvalidCredentials(CustomError):
    pass


class AuthError(CustomError):
    pass