class MissingRegexRecogniserError(KeyError):
    """
    Exception raised when a regex recogniser is requested but not found in the supported regex_entities list.

    Attributes:
        message (str): The error message.
    """

    def __init__(
        self,
        message: str = "No regex settings could detected in pteredactyl.regex_entities",
    ):
        super().__init__(message)
        self.message = message
