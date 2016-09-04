# Python Extension Base

Module with common shared components for other Python extensions.

## Installation

Inside `$SERVER_BASE/python/bf2/__init__.py` at the beginning of the `init_module` method replace `sys.out` and `sys.err` initialization with:

    import pyebase
    pyebase.initLogging(False) # `True` to enable debug logging

