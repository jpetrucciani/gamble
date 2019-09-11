"""
@desc custom exceptions and error handling
"""


class GambleException(Exception):  # pragma: no cover
    """
    @desc base gamble exception class
    """

    def __init__(self, *args, **kwargs):  # type: ignore
        """
        @cc 2
        @desc exception constructor
        @arg args: extra args to pass to the exception
        @arg kwargs: extra kwargs to parse
        """
        self.__dict__.update(kwargs)
        extra = ""
        if args:
            extra = '\n| extra info: "{extra}"'.format(extra=args[0])
        print(
            "[{exception}]: {doc}{extra}".format(
                exception=self.__class__.__name__, doc=self.__doc__, extra=extra
            )
        )
        Exception.__init__(self, *args)


class InvalidCard(GambleException):
    """
    @desc the given string is not a valid card
    """
