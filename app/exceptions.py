"""Custom exceptions for the application."""


class ImmersiVerseException(Exception):
    """Base exception for ImmersiVerse application."""
    pass


class ValidationError(ImmersiVerseException):
    """Raised when data validation fails."""
    pass


class NotFoundError(ImmersiVerseException):
    """Raised when a requested resource is not found."""
    pass


class AuthenticationError(ImmersiVerseException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(ImmersiVerseException):
    """Raised when authorization fails."""
    pass


class WorldGenerationError(ImmersiVerseException):
    """Raised when world generation fails."""
    pass


class PrefabCatalogError(ImmersiVerseException):
    """Raised when prefab catalog operations fail."""
    pass


class TelemetryError(ImmersiVerseException):
    """Raised when telemetry operations fail."""
    pass
