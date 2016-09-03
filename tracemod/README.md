# Python Trace Module

Python game module with verbose debug logging routines to aid debugging server crashes. Some parts of this module are specific for Project Reality 1.3 and will break with the new version. Use with caution.

This module requires [pyebase](../pyebase/README.md).

## Installation

To initialize the module place the following lines at the end of `$SERVER_BASE python/bf2/__init__.py` (on the global scope, **not** inside `init_module`):

    import tracemod
