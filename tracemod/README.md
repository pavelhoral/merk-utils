# Python Trace Module

Python game module with verbose debug logging routines to aid debugging server crashes. Some parts of this module are specific for Project Reality 1.3 and will break with the new version. Use with caution.

This module requires [pyebase](../pyebase/README.md).

## Installation

To initialize the module place the following lines at the beginning of `$SERVER_BASE/mods/pr/python/game/__init__.py` (before any module that should be traced):

    import tracemod

