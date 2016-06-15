#!/bin/bash
#
# Start PR server and watch handle restarts in case of a server crash.
#
# Supported variables:
#  
# - SERVER_BASE = Base directory for the server (defaults to script's dirname).
# - SERVER_NAME = Symbolic name of the server (defaults to basename of `$SERVER_BASE`).
# - BACKUP_BASE = Base directory for data backup (defaults to `$SERVER_BASE/backup`).
# - TCPDUMP_BASE = Base directory for PCAP files (defaults to `$SERVER_BASE/netdump`).
# - LOG_FILE = Path to the script's log file (defaults to `$SERVER_BASE/server.log`).
# - SCRIPT_BASE = Base path for shared scripts (defaults to dirname of script's real location).
#
# Supported event scripts are:
# - on_before_start.sh = Executed before the server is being started.

if [ -z "$SERVER_BASE" ]; then
   SERVER_BASE=$(dirname "$0")
fi
if [ -z "$SERVER_NAME" ]; then
   SERVER_BASE=$(readlink -f "$SERVER_BASE")
   SERVER_NAME=$(basename "$SERVER_BASE")
fi
if [ -z "$BACKUP_BASE" ]; then
    BACKUP_BASE="$SERVER_BASE/backup"
fi
if [ -z "$TCPDUMP_BASE" ]; then
    TCPDUMP_BASE="$SERVER_BASE/netdump"
fi
if [ -z "$LOG_FILE" ]; then
    LOG_FILE="$SERVER_BASE/server.log"
fi
if [ -z "$SCRIPT_BASE" ]; then
    SCRIPT_BASE=$(dirname "$(readlink -f "$0")")
fi

# Write message to a log file
log_message() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") [$SERVER_NAME] $1" >> "$LOG_FILE"
}

# Start the server
start_server() {
	if [ -f "$SERVER_BASE/on_before_start.sh" ]; then
	    . "$SERVER_BASE/on_before_start.sh"
	fi
    "$SERVER_BASE/start_pr.sh"
    return $?
}

# Collect debug information
collect_debug() {
    local PREFIX="$(date +"%Y-%m-%d_%H:%M:%S")_$SERVER_NAME"
    mv core "$BACKUP_BASE/$PREFIX"_core
    cp "$TCPDUMP_BASE"/$(ls -1t "$TCPDUMP_BASE" | head -1) "$BACKUP_BASE/$PREFIX"_tcpdump
}

# We need to switch to server directory
cd "$SERVER_BASE"

log_message "Running server start-up script."
echo "To stop the server press Ctrl+C..."
trap 'log_message "Server execution interrupted... aborting restart cycle."; exit 1' 2

RESTART_COUNTER=0
while true; do
    start_server
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 139 -o $EXIT_CODE -eq 134 ]; then
        collect_debug
    fi
    RESTART_COUNTER=$((RESTART_COUNTER+=1))
    log_message "Server stopped [CODE=$EXIT_CODE] and will be restarted [COUNTER=$RESTART_COUNTER]."
    sleep 10
done

