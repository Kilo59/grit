"""
tests.test_basic.py
"""
from grit import Grit
import pytest


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


if __name__ == "__main__":
    pytest.main(["-vv"])
