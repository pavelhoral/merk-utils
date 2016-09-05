#!/bin/bash
### BEGIN INIT INFO
# Provides:          pr-main
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Project Reality server instance.
# Description: This is a skeleton init script for running Project Reality
#              server and their components. Modify common parameters
#              at the beginning of the script and path to the shared
#              server_control.sh stub. You can add or remove any components
#              inside the `start` case.
### END INIT INFO

SERVER_USER=pr
SERVER_BASE=/opt/pr/main

. /opt/pr/utils/prserver/server_control.sh

case "$1" in
    start)
        set -e
        start_server ./start_server.sh
        start_component MURMUR 'bash -c "cd mods/pr/bin/PRMurmur; ./prmurmurd.x64 -fg"'
        start_component MUMO 'bash -c "cd mods/pr/bin/PRMurmur; ./startmumo.sh"'
        start_component PROXY 'bash -c "shared/nodejs/bin/node shared/proxy/src | tee proxy.log"'
    ;;
    stop)
        stop_server
    ;;
    restart)
        stop_server
        start_server
    ;;
    status)
        server_status
    ;;
    *)
        echo "Usage: $0 (start|stop|restart|status)" 1>&2
    ;;
esac

