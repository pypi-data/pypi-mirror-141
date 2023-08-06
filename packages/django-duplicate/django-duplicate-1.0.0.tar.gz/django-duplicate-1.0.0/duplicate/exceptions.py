class DuplicationException(Exception):
    """Exception raised when duplication failed."""


class NotAllRelatedInstancesSaved(DuplicationException):
    """Exception raised when not all collected duplicated instances were saved."""


class NotNullableCircularRelation(DuplicationException):
    """Raised when there is not nullable circular relation."""
