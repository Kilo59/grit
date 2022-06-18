"""
tests.test_basic.py
"""
import logging

import pytest

from grit import Grit

logging.basicConfig()


@pytest.mark.parametrize(
    "dnr_list",
    [
        None,
        [],
        # list
        [NotADirectoryError, ValueError, TypeError],
        # tuple
        (NotADirectoryError, ValueError, TypeError),
        # set
        {NotADirectoryError, ValueError, TypeError},
    ],
)
def test_exception_swallowing(dnr_list):
    with Grit(dnr_list):
        raise ZeroDivisionError("dont mind me")


@pytest.mark.parametrize(
    "dnr_list,exc_to_raise",
    [
        ([ValueError], ValueError),
        ([NotImplementedError, ValueError], ValueError),
        ([ArithmeticError], ZeroDivisionError),
    ],
)
def test_dnr_list_exception_propogation(dnr_list, exc_to_raise):

    with pytest.raises(exc_to_raise):

        with Grit(dnr_list=dnr_list):
            raise exc_to_raise("oops")


@pytest.mark.parametrize(
    "parent,child",
    [
        (Exception, ValueError),
        (ArithmeticError, ZeroDivisionError),
        (BaseException, Exception),
        # Not all exceptions inherit from `Exception`
        (BaseException, KeyboardInterrupt),
    ],
)
def test_dnr_list_exception_inheritance(parent, child):
    """
    Test that exception subclasses are correctly propagated given a parent class dnr
    exception.
    """
    assert issubclass(child, parent), f"{child} does not inherit from {parent}"

    with pytest.raises(child):

        with Grit(dnr_list=[parent]):
            raise child("Witness me!")


def test_handlers():
    def _get_exc_message(exc: Exception) -> str:
        print("Called!")
        return str(exc)

    with Grit(handlers={ValueError: _get_exc_message}) as ctx:
        raise ValueError("oops")

    assert "oops" == ctx.result


def _raise_runtime_error(exc: Exception):
    raise RuntimeError("raised from _raise_runtime_error") from exc


@pytest.mark.parametrize(
    "dnr_list,handlers,exc_to_raise,expected_exception,exp_result",
    [
        (
            # ZeroDivision is dnr but the ZeroDivisionError handler is called before
            # original error is propogated and so the error that propgates should be
            # a RunTimeError raised by the handler function
            [ZeroDivisionError],
            {ZeroDivisionError: _raise_runtime_error},
            ZeroDivisionError,
            RuntimeError,
            None,
        ),
        (
            [ZeroDivisionError],
            {ZeroDivisionError: lambda x: str(x)},
            ZeroDivisionError("whoops"),
            ZeroDivisionError,
            "whoops",
        ),
    ],
)
def test_exc_propagation(
    dnr_list, handlers, exc_to_raise, expected_exception, exp_result
):
    with pytest.raises(expected_exception):
        with Grit(dnr_list=dnr_list, handlers=handlers) as grt:
            raise exc_to_raise

    print(grt)
    assert exp_result == grt.result


if __name__ == "__main__":
    pytest.main(["-vv"])
