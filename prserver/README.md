# Project Reality Server Scripts

All you need to get the Project Reality server up and running. Every script contains a brief description inside its header.

Scripts should not be modified directly, but rather customized through symbolic links and environment variables.

## Server Start-up

The main script regarding server's start-up is `start_server.sh`. This script runs the server and can automatically restart it in case of a crash. Every start and restart is logged inside `server.log` file. In addition to the standard operation the script also auto-detects and runs two hook scripts:

* `on_before_start.sh` - run just before the server is started
* `on_after_crash.sh` - run just after the server crashes

The standard set-up is that the `start_server.sh` is linked inside server's base directory. Example *BEFORE START* script is `change_startmap.sh`. Example *AFTER CRASH* script is `collect_debug.sh`.

## Init Script

Base script for running the server as a system service is `server_control.sh`. This script contains shared functions for writing init scripts. Example init script is `server_init.sh`.

Every server instance should have its own copy of `server_init.sh` inside `/etc/init.d`. The base `server_control.sh` should be shared. For more information read script comments.
