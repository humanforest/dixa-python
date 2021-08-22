"""Errors that can be raised by this SDK"""


class DixaClientError(Exception):
    """Base class for Client errors."""


class DixaRequestError(DixaClientError):
    """Error raised when there's a problem with the request that's being submitted."""


class DixaApiError(DixaClientError):
    """Error raised when Dixa does not send the expected response."""

    def __init__(self, message, response):
        msg = f"{message}\nThe server responded with: {response}"
        self.response = response
        super(DixaApiError, self).__init__(msg)
