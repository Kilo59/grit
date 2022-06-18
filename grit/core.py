"""
grit.core
"""
import logging
import traceback
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Type, Union

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


class Grit:
    """Grit context manager for dealing with exceptions less badly."""

    def __init__(
        self,
        dnr_list: Optional[Union[Sequence[AnyException], Sequence]] = None,
        handlers: Optional[Dict[ExceptionType, Callable[[AnyException], Any]]] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        if not dnr_list:
            self.dnr_list: Tuple = tuple()
        else:
            self.dnr_list = tuple(dnr_list)

        if not logger:
            logger = GRIT_LOGGER
        self.logger = logger
        self.handlers = handlers or dict()
        self.exception: Optional[AnyException] = None
        self.result: Any = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type: ExceptionType, exc_value: AnyException, exc_tb):
        # print(f"{type(exc_type)} {exc_type=}")
        # print(f"{type(exc_value)} {exc_value=}")
        # print(f"{type(exc_tb)} {exc_tb.__class__.__name__} {exc_tb=}")
        if exc_value:
            log_traceback(exc_value, self.logger, logging.DEBUG)

        # TODO: make this work with exeception child types
        exc_handler = self.handlers.get(exc_type)
        if exc_handler:
            # TODO: log the name of the handler and deal with unnamed functions (lambdas)
            self.logger.info(f"Ecountered {exc_type} handling ...")
            # TODO: inspect to determine if handler takes arguments/no args and treat it
            # appropriatly
            # https://docs.python.org/3/library/inspect.html
            self.result = exc_handler(exc_value)

        if isinstance(exc_value, self.dnr_list):
            # Returning False will cause the original exception to be propogated up
            # the stack and processed normally
            # https://docs.python.org/3/reference/datamodel.html#object.__exit__
            return False
        # Returning True swallows the original exception
        return True
