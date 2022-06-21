# grit

[![ci](https://github.com/Kilo59/grit/workflows/ci/badge.svg)](https://github.com/Kilo59/grit/actions)
[![pypi version](https://img.shields.io/pypi/v/grit.svg)](https://pypi.org/project/py-grit/)
![Python Versions](https://img.shields.io/pypi/pyversions/py-grit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Context manager for shrugging off exceptions less badly.

Subtitle: exception handling for lazy people.

## Description and Rationale

Does your code suffer from an overuse of bare exceptions?

What if you could still shrug off exceptions when needed but not be so cringe about it?

```python
try:
    foobar()
except Exception:
    pass
```

```python
from grit import Grit

# Full exception stacktrace is automatically logged
with Grit():
    foobar()
```

## Quick start

```
pip install py-grit
```

```python
>>> from grit import Grit
>>> with Grit():
...     raise RunTimeError("something bad")
>>> print("Uh, everything is under control. Situation normal")
Uh, everything is under control. Situation normal

```

Propagate the errors you care about, while ignoring the ones you don't.

```python
>>> from grit import Grit
>>> with Grit(dnr_list=[ZeroDivisionError]):
...     42 / 0
Traceback (most recent call last):
    ...
ZeroDivisionError: division by zero

```

And handle those that require special attention

```python
>>> from grit import Grit
>>> with Grit(handlers={ValueError: print}):
...     raise ValueError("what have you done?!")
what have you done?!

```

## Logging and results

`Grit()` accepts a `fallback_handler` callable which will be called on the exception if no specific
'handler' (`handlers`) is found.

By default the `fallback_handler` will log a full exception traceback at the debug level using `self.logger`.

To change this behavior, provide your own `fallback_handler`.

```python
>>> from grit import Grit
>>> with Grit(fallback_handler=print):
...     raise TypeError("what have I done?!")
what have I done?!

```

## Usage Examples

TODO ...
