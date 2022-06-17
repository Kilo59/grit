# grit

Context manager for shrugging off exceptions less badly.

Subtitle: exception handling for lazy people.

## Quick start

```
pip install grit
```

```python
>>> from grit import Grit
>>> with Grit():
...     raise RunTimeError("something broke")
>>> print("Uh, everything is under control. Situation normal")
Uh, everything is under control. Situation normal

```
