# Python Extension Base

Module with common shared components for other Python extensions.

## Installation

Inside `$SERVER_BASE/python/bf2/__init__.py` at the end of `init_module` method add:

    import pyebase
    pyebase.initLogging(False) # `True` to enable debug logging
