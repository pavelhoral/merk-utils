# GDB Tools

GDB command scripts to aid working with core dump files.

## Instalation

Preferred way of installation is loading both the GDB command script and the Python script inside `~/.gdbinit` file (substitute `$UTILS_BASE` with the correct path):

    source $UTILS_BASE/gdbtools/gdbtools
    source $UTILS_BASE/gdbtools/gdbtools.py

# Using LESS

When analyzing long output, not being able to scroll back or actively search is quite painful. You can prefix any command with `less` to use LESS as the output pager.

Usage:

    less {gdb command}

Example:

    less info types


# Accessing CPython Structures

Working with CPython structures can be tedious when it comes to never ending type discovery and type casting. Via `pyp` (python print) command  you can enable automatic type discovery and in some cases a direct value extraction.

Usage:

    pyp {variable} {struct path}

Example:

    pyp player ma_table[0].me_key

**NOTE:** This command is simple in its current form and does not allow much when it comes to dictionaries.
