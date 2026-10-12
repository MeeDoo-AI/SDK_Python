"""Exception classes for the MeeDoo AI SDK."""


class MeeDooError(Exception):
    """Base exception for all MeeDoo SDK errors."""
    def __init__(self, message: str = "", status_code: int = 0, body: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body or {}


class AuthenticationError(MeeDooError):
    """Raised when authentication fails (401)."""


class RateLimitError(MeeDooError):
    """Raised when rate limit is exceeded (429)."""


class InsufficientCreditsError(MeeDooError):
    """Raised when API credits are insufficient."""
    def __init__(self, message: str = "", balance: float = 0, status_code: int = 400, body: dict | None = None):
        super().__init__(message, status_code, body)
        self.balance = balance


class ModelNotFoundError(MeeDooError):
    """Raised when the specified model is not found."""


class APIError(MeeDooError):
    """Raised for other API errors (500, etc.)."""