# Project Reality Server Scripts

All you need to get the Project Reality server up and running. Every script contains a brief description inside its header.

Scripts should not be modified directly, but rather customized through symbolic links and environment variables.

## Start-up Script (`start_server.sh`)

The main script regarding server's start-up logic is `start_server.sh`. This script runs the server and automatically restarts it in case of a crash. Every start and restart is logged inside `server.log` file. In addition to the standard operation the script also auto-detects and runs two hook scripts:

* `on_before_start.sh` - run just before the server is started
* `on_after_crash.sh` - run just after the server crashes

The standard set-up is that the `start_server.sh` is linked inside server's base directory. Example *BEFORE START* script is `change_startmap.sh`. Example *AFTER CRASH* script is `collect_debug.sh`.

## Systemv Init Scripts (`init`)

This folder contains SystemV init scripts for running PR as a service. Check script comments for more information.

SystemV is deprecated in favor of SystemD and the scripts are not maintained.

## Systemd Init Scripts (`system`)

Template systemd unit configurations. To use copy these files with appropriate instance name into `/etc/systemd/system` folder (e.g. `pr-server@.service` as `pr-service@main.service`) and modify the contents as needed.

