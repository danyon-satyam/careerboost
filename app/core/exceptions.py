from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    """Resource not found — 404."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class UnauthorizedError(HTTPException):
    """Not authenticated — 401."""
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenError(HTTPException):
    """Authenticated but not allowed — 403."""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ConflictError(HTTPException):
    """Resource already exists — 409."""
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class BadRequestError(HTTPException):
    """Invalid request data — 400."""
    def __init__(self, detail: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
        