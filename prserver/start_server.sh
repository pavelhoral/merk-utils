#!/bin/bash
#
# Start PR server and handle restarts in case of a server crash.
#
# Script setup:
#
# - This script is intended to be symlinked or copied under the server's base directory.
# - For any additional startup logic link or create additional event script (see bellow).
# - Script creates and maintains server (re)start log file as defined by $LOG_FILE.
#
# Supported variables:
#
# - SERVER_BASE = Base directory for the server (defaults to script's dirname).
# - SERVER_NAME = Symbolic name of the server (defaults to basename of `$SERVER_BASE`).
# - LOG_FILE = Path to the script's log file (defaults to `$SERVER_BASE/server.log`).
#
# Supported event scripts are:
#
# - on_before_start.sh = Executed before the server is being started.
# - on_after_crash.sh = Executed when server crash is detected.
#

if [ -z "$SERVER_BASE" ]; then
    SERVER_BASE=$(dirname "$0")
fi
if [ -z "$SERVER_NAME" ]; then
    SERVER_BASE=$(readlink -f "$SERVER_BASE")
    SERVER_NAME=$(basename "$SERVER_BASE")
fi
if [ -z "$LOG_FILE" ]; then
    LOG_FILE="$SERVER_BASE/server.log"
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

# Handle server crash
handle_crash() {
    if [ -f "$SERVER_BASE/on_after_crash.sh" ]; then
        . "$SERVER_BASE/on_after_crash.sh"
    fi
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
    RESTART_COUNTER=$((RESTART_COUNTER+=1))
    log_message "Server stopped [CODE=$EXIT_CODE] and will be restarted [COUNTER=$RESTART_COUNTER]."
    if [ $EXIT_CODE -eq 139 -o $EXIT_CODE -eq 134 ]; then
        handle_crash
    fi
    sleep 10
done
