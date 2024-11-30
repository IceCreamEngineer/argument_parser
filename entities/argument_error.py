from enum import Enum, auto


class ArgumentError(RuntimeError):
    def __init__(self, error_code, argument_id=None):
        self._error_code = error_code
        self._error_argument_id = argument_id

    def get_error_argument_id(self):
        return self._error_argument_id

    def set_error_argument_id(self, argument_id):
        self._error_argument_id = argument_id

    def get_error_code(self):
        return self._error_code

    def error_message(self):
        if self._error_code == ArgumentErrorCode.UNEXPECTED_ARGUMENT:
            return f"Argument -{self._error_argument_id} unexpected."
        elif self._error_code == ArgumentErrorCode.MISSING_STRING:
            return f"Could not find string parameter for -{self._error_argument_id}"
        elif self._error_code == ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT:
            return f"Missing required argument: {self._error_argument_id}"
        elif self._error_code == ArgumentErrorCode.INVALID_ARGUMENT_NAME:
            return f"'{self._error_argument_id}' is not a valid argument name."
        elif self._error_code == ArgumentErrorCode.INVALID_ARGUMENT_FORMAT:
            return f"'{self._error_argument_id}' is not a valid argument format."
        return ''


class ArgumentErrorCode(Enum):
    UNEXPECTED_ARGUMENT = auto()
    INVALID_ARGUMENT_NAME = auto()
    INVALID_ARGUMENT_FORMAT = auto()
    MISSING_STRING = auto()
    MISSING_REQUIRED_ARGUMENT = auto()
