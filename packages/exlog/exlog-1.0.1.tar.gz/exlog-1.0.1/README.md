# exception-logging
Exception logging decorator, class decorator and metaclass generator. Some usage examples are shown below, and the corresponding log files generated.

---


```py
"""Standard decorator example."""

from src.exlog.exceptlog import exception_logger

log = exception_logger("./tests/log.log", "US/Eastern")


@log
def no_return():
    raise Exception("DO NOT PASS GO DO NOT COLLECT $200.")


if __name__ == "__main__":
    try:
        no_return()
    except:
        pass
```
Logs the following in `log.log`.
```
ERROR:root:no_return
  raised Exception: DO NOT PASS GO DO NOT COLLECT $200.
    called with args = (), kwargs = {}
    at 2022-03-08 14:07:54.325358-05:00
Traceback (most recent call last):
  File "/home/ryan/exception-logging/src/exlog/exceptlog.py", line 58, in wrapper
    output = function(*args, **kwargs)
  File "/home/ryan/exception-logging/./tests/test_logger.py", line 20, in no_return
    raise Exception("DO NOT PASS GO DO NOT COLLECT $200.")
Exception: DO NOT PASS GO DO NOT COLLECT $200.
```


---


```py
"""Class decorator example."""

from src.exlog.exceptlog import exception_logger_cls

log = exception_logger_cls("./tests/cls.log", "US/Eastern")

@log
class Foo:
    @classmethod
    def bar1(cls):
        raise Exception("BAR1!")
    @staticmethod
    def bar2():
        raise Exception("BAR2!")
    def bar3(self):
        raise Exception("BAR3!")


if __name__ == "__main__":
    foo = Foo()
    for method in (foo.bar1, foo.bar2, foo.bar3):
        try:
            method()
        except:
            pass
```
Logs the following in `cls.log`.
```
ERROR:root:Foo.bar1
  raised Exception: BAR1!
    called with args = ("<class '__main__.Foo'>",), kwargs = {}
    at 2022-03-08 14:07:54.365631-05:00
Traceback (most recent call last):
  File "/home/ryan/exception-logging/src/exlog/exceptlog.py", line 58, in wrapper
    output = function(*args, **kwargs)
  File "/home/ryan/exception-logging/./tests/test_cls.py", line 21, in bar1
    raise Exception("BAR1!")
Exception: BAR1!
ERROR:root:Foo.bar2
  raised TypeError: Foo.bar2() takes 0 positional arguments but 1 was given
    called with args = ('<__main__.Foo object at 0x7f656343dd20>',), kwargs = {}
    at 2022-03-08 14:07:54.366143-05:00
Traceback (most recent call last):
  File "/home/ryan/exception-logging/src/exlog/exceptlog.py", line 58, in wrapper
    output = function(*args, **kwargs)
TypeError: Foo.bar2() takes 0 positional arguments but 1 was given
ERROR:root:Foo.bar3
  raised Exception: BAR3!
    called with args = ('<__main__.Foo object at 0x7f656343dd20>',), kwargs = {}
    at 2022-03-08 14:07:54.366307-05:00
Traceback (most recent call last):
  File "/home/ryan/exception-logging/src/exlog/exceptlog.py", line 58, in wrapper
    output = function(*args, **kwargs)
  File "/home/ryan/exception-logging/./tests/test_cls.py", line 26, in bar3
    raise Exception("BAR3!")
Exception: BAR3!
```


---


```py
"""Metaclass example."""

from src.exlog.exceptlog import exception_logger_meta

log = exception_logger_meta("./tests/meta.log", "US/Eastern")


class Base(metaclass=log):
    pass

class Foo(Base):
    @classmethod
    def bar1(cls):
        raise Exception("METABAR1!")
    @staticmethod
    def bar2():
        raise Exception("METABAR2!")
    def bar3(self):
        raise Exception("METABAR3!")


if __name__ == "__main__":
    foo = Foo()
    for method in (foo.bar1, foo.bar2, foo.bar3):
        try:
            method()
        except:
            pass
```
Logs the following in `meta.log`.
```
ERROR:root:Foo.bar1
  raised Exception: METABAR1!
    called with args = ("<class '__main__.Foo'>",), kwargs = {}
    at 2022-03-08 14:07:54.406422-05:00
Traceback (most recent call last):
  File "/home/ryan/exception-logging/src/exlog/exceptlog.py", line 58, in wrapper
    output = function(*args, **kwargs)
  File "/home/ryan/exception-logging/./tests/test_meta.py", line 24, in bar1
    raise Exception("METABAR1!")
Exception: METABAR1!
ERROR:root:Foo.bar2
  raised TypeError: Foo.bar2() takes 0 positional arguments but 1 was given
    called with args = ('<__main__.Foo object at 0x7fc127ddda50>',), kwargs = {}
    at 2022-03-08 14:07:54.406884-05:00
Traceback (most recent call last):
  File "/home/ryan/exception-logging/src/exlog/exceptlog.py", line 58, in wrapper
    output = function(*args, **kwargs)
TypeError: Foo.bar2() takes 0 positional arguments but 1 was given
ERROR:root:Foo.bar3
  raised Exception: METABAR3!
    called with args = ('<__main__.Foo object at 0x7fc127ddda50>',), kwargs = {}
    at 2022-03-08 14:07:54.407025-05:00
Traceback (most recent call last):
  File "/home/ryan/exception-logging/src/exlog/exceptlog.py", line 58, in wrapper
    output = function(*args, **kwargs)
  File "/home/ryan/exception-logging/./tests/test_meta.py", line 29, in bar3
    raise Exception("METABAR3!")
Exception: METABAR3!
```
