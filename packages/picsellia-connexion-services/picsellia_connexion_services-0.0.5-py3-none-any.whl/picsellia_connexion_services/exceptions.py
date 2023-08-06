
class NetworkError(Exception):
    """Raised when an HTTPError occurs."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnauthorizedError(Exception):
    """Raised when user is not authorized."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
