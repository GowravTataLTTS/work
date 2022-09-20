class RecordExistenceError(Exception):
    """exception to be raised when the record already exists"""


class RecordInExistenceError(Exception):
    """exception to be raised when the record is not found in the database"""


class InvalidPayloadException(Exception):
    """exception to be raised when the payload sent is invalid"""

