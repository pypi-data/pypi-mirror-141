class NeispyException(Exception):
    pass


class ArgumentError(NeispyException):
    def __init__(self):
        super().__init__("인자값이 틀립니다.")


class HTTPException(NeispyException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class MissingRequiredValues(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class AuthenticationKeyInvaild(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class ServiceNotFound(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class LocationValueTypeInvaild(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class CannotExceed1000(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class DailyTrafficLimit(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class ServerError(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class DatabaseConnectionError(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class SQLStatementError(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class LimitUseAuthenticationkey(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


class DataNotFound(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code} {message}")


ExceptionsMapping = {
    "INFO-200": DataNotFound,
    "INFO-300": LimitUseAuthenticationkey,
    "ERROR-290": AuthenticationKeyInvaild,
    "ERROR-300": MissingRequiredValues,
    "ERROR-310": ServiceNotFound,
    "ERROR-333": LocationValueTypeInvaild,
    "ERROR-336": CannotExceed1000,
    "ERROR-337": DailyTrafficLimit,
    "ERROR-500": ServerError,
    "ERROR-600": DatabaseConnectionError,
    "ERROR-601": SQLStatementError,
}
