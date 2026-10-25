class AuthServiceError(RuntimeError):
    """Base error raised when the upstream auth service cannot fulfil a call."""


class InvalidCredentialsError(AuthServiceError):
    """The supplied credentials are not valid."""


class UpstreamAuthError(AuthServiceError):
    """The upstream auth service is unavailable or returned an invalid reply."""


class UserAlreadyExistsError(AuthServiceError):
    """Registration was rejected because the email is already registered."""
