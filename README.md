# MeRk Project Reality Server Utils

![MeRk](header.png)

*MeRk Utils* is a project with various utility scripts for running and managing Linux based Project Reality servers.
This document gives a brief description of each project component.
Some components might contain a more detailed description as a separate README in their own directory.

## Common Properties

Most of the tools use the following common dictionary:

* *server base* - base directory of PR server installation
* *server name* - symbolic name of the running PR server
* *utils base* - base directory containing this project

Each component is usually configured via environment variables so there is no need to modify any files inside this project.
Some components can autodetect their configuration or infer from other other variables (e.g. `SERVER_NAME` is taken as dirname of `SERVER_BASE`).

## GDB Tools (gdbtools)

Set of useful GDB commands to help with analyzing server core dumps, mainly oriented at segfaults inside Python code.
When imported it gives you ability to use `less` as GDB pager and also access CPython objects in a more friendly manner via `pyp` command.

See component's [README.md](gdbtools/README.md) for more details.

## Iptables Name Hack Protection (namehack)

Iptables based protection against so called *name hack* (when some player connects with faked name of already connected player, which causes mass CTD).

## Net Dump (netdump)

TCPDUMP wrapper for capturing network activity in a space limited fashion. Script `netdump.sh` runs the *tcpdump* to collect packets in 10 minute based segments (PR can generate 1~2 GB during that period) and `cleanup.sh` drops old capture files.

## Project Reality Folder (prfolder)

Guide how to setup Project Reality servers in a well defined environment called *Project Reality Folder*.
You should follow the [suggested structure](prfolder/README.md) to get the most out of the scripts inside this project and to get nice stable server deployment.

## Project Reality Server Scripts (prserver)

Collection of scripts for running, managing and customizing Project Reality server deployment.
These include modified server start-up script (handling restarts) and system init scripts (running server with its components - murmur, mumo, proxy).

See component's [README.md](prserver/README.md) for more details.

## Python Extension Base (pyebase)

Game Python extension base module with shared components.
See component's [README.md](pyebase/README.md) for more details.

## Reality Python Fixes (realityfix)

Fixes of various Project Reality Python bugs.
See component's [README.md](realityfix/README.md) for more details.

## Python Sandbox Module (sandbox)

Module with various scripts in more or less mature state.
See component's [README.md](sandbox/README.md) for more details.

## Python Trace Module (tracemod)

Module providing verbose debug logging to help solving server crashes or other gameplay issues.
See component's [README.md](tracemod/README.md) for more details.
