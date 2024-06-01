class BaseException(Exception):
    """
    Base exception
    """

    def __init__(self, message, error_key="error"):
        super().__init__(message, error_key)
        self.message = message
        self.error_key = error_key
