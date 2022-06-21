"""
grit.core
"""
import logging
import traceback
from typing import Any, Callable, Dict, Optional, Sequence, Type, Union

AnyException = Union[BaseException, Exception]

ExceptionType = Type[Exception]
# ExceptionType = Union[Type[Exception], Type[BaseException]]

GRIT_LOGGER = logging.getLogger("grit")


def format_traceback(ex: AnyException) -> str:
    """Generate a full exception traceback string from an exception."""
    tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    return "".join(tb_lines)


def log_traceback(ex: AnyException, logger: logging.Logger, level: int):
    """Log the full exception traceback of an exception."""
    logger.log(level, format_traceback(ex))


# pylint: disable=fixme

# TODO: call async or standard sync handlers


class Grit:
    """Grit context manager for dealing with exceptions less badly."""

    def log_debug_traceback(self, ex: AnyException):
        """Log a full stacktrace at the DEBUG level."""
        self.logger.debug(format_traceback(ex))

    def __init__(
        self,
        dnr_list: Optional[Union[Sequence[AnyException], Sequence]] = None,
        handlers: Optional[Dict[ExceptionType, Callable[[AnyException], Any]]] = None,
        fallback_handler: Optional[Callable[[AnyException], Any]] = None,
        logger: logging.Logger = GRIT_LOGGER,
    ) -> None:
        """
        Parameters
        ----------
        dnr_list
            Sequence of exceptions that should not be ignored.
            `Grit` will call the `fallback_handler` function and then propagate these
            exceptions (and children) if encountered.
            by default `None`
        handlers
            Mapping of `Exception` to handler functions. Function will be passed the
            exception instance. Function return value will be saved to `self.result`.
            by default None
        fallback_handler
            Function to call if not specific handler is found.
            by default `self.log_debug_traceback`
        logger
            logger used be Grit. by default GRIT_LOGGER
        """
        self.dnr_list = tuple(dnr_list) if dnr_list else tuple()

        self.logger = logger
        self.handlers = handlers or {}
        self.exception: Optional[AnyException] = None
        self.fallback_handler = fallback_handler or self.log_debug_traceback
        self.result: Any = None

    def __enter__(self) -> "Grit":
        return self

    def __exit__(
        self,
        exc_type: Optional[ExceptionType],
        exc_value: Optional[AnyException],
        exc_tb,
    ):
        if exc_value:
            # TODO: make this work with exception child types
            # use the fallback_handler if no other handler is found
            exc_handler = self.handlers.get(exc_type, self.fallback_handler)  # type: ignore
            if exc_handler:
                # TODO: log the name of the handler and deal with unnamed functions (lambdas)
                self.logger.info(
                    f"Encountered {exc_type} handling with {exc_handler} ..."
                )
                # TODO: inspect to determine if handler takes arguments/no args and treat it
                # appropriately
                # https://docs.python.org/3/library/inspect.html
                self.result = exc_handler(exc_value)

        if isinstance(exc_value, self.dnr_list):
            # Returning False will cause the original exception to be propogated up
            # the stack and processed normally
            # https://docs.python.org/3/reference/datamodel.html#object.__exit__
            return False
        # Returning True swallows the original exception
        return True

    def __repr__(self) -> str:
        dnr_list = ", ".join((e.__name__ for e in self.dnr_list))
        handlers = ", ".join(
            (f"{e.__name__}: {fn.__name__}" for e, fn in self.handlers.items())
        )
        return (
            f"{self.__class__.__name__}(dnr_list=[{dnr_list}], handlers={{{handlers}}})"
        )
