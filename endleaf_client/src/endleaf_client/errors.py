"""One-line errors plus a fix. ENDLEAF-R53-ERROR."""

from __future__ import annotations


class ClientError(Exception):
    """Local refusal. str() is one line plus a Fix line."""

    def __init__(self, message: str, fix: str) -> None:
        self.message = message
        self.fix = fix
        super().__init__(f"{message}\nFix: {fix}")


def fail(message: str, fix: str) -> ClientError:
    return ClientError(message, fix)
