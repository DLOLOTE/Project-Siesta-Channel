class InvalidAPIResponse(Exception):
    pass


class RegionLocked(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class AuthError(Exception):
    pass