"""
@author jacobi petrucciani
@desc custom exceptions and error handling
"""
from typing import Any


class GambleException(Exception):  # pragma: no cover
    """
    @desc base gamble exception class
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        @cc 2
        @desc exception constructor
        """
        self.__dict__.update(kwargs)
        extra = ""
        if args:
            extra = f'\n| extra info: "{args[0]}"'
        print(f"[{self.__class__.__name__}]: {self.__doc__}{extra}")
        Exception.__init__(self, *args)


class InvalidCard(GambleException):
    """
    @desc the given string is not a valid card
    """
