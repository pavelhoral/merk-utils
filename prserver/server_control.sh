#!/bin/bash
#
# Control script for running PR server and its components.
#
# Main idea behind the script is that a single server instance is being run in its own daemon 
# screen and attached server components (Murmur, Mumo, ...) are running under the same screen 
# in their own separate windows (see `man screen` for more details).
#
# Screens are named based on $SCREEN_NAME variable (see bellow). Every window has its symbolic 
# title based on the running component (e.g. SERVER, MURMUR, MUMO, ...).
#
# Connecting to the screen is as easy as writing `screen -x $SCREEN_NAME`. To switch between
# screen's windows push CTRL-A followed by ".
#
# Script setup:
#
# - This script is intended to be included inside server init script.
#
# Supported variables:
#
# - SERVER_BASE = Base directory for the server (defaults to script's dirname).
# - SERVER_NAME = Symbolic name of the server (defaults to basename of `$SERVER_BASE`).
# - SCREEN_NAME = Name of the daemon screen (defaults to `pr-$SERVER_NAME`)
# - SERVER_USER = Name of the user to run the server's screen (defaults to 'pr'). 
#

if [ -z "$SERVER_BASE" ]; then
    SERVER_BASE=$(dirname "$0")
fi
if [ -z "$SERVER_NAME" ]; then
    SERVER_BASE=$(readlink -f "$SERVER_BASE")
    SERVER_NAME=$(basename "$SERVER_BASE")
fi
if [ -z "$SCREEN_NAME" ]; then
    SCREEN_NAME="pr-$SERVER_NAME"
fi
if [ -z "$SERVER_USER" ]; then
    SERVER_USER="pr"
fi

#
# Report script failure.
#
report_error() {
    echo "[ERROR] $@" 1>&2
}

#
# Report script action.
#
report_info() {
    echo "[INFO] $@"
}

#
# Run screen command under the correct user.
#
call_screen() {
    sudo -u "$SERVER_USER" screen "$@"
}

#
# Get PID of the server's daemon screen.
# Arguments: {required}.
#
get_screen_pid() {
    SCREEN_PIDS=($(call_screen -S "$SCREEN_NAME" -ls | grep -Po '^\t[0-9]+' | xargs))
    if [ ${#SCREEN_PIDS[@]} -gt 1 ]; then
        report_error "Multiple matching screen PIDs detected: ${SCREEN_PIDS[@]}."
        exit 1
    elif [ ${#SCREEN_PIDS[@]} -eq 1 ]; then
        echo "${SCREEN_PIDS[0]}"
    elif [ "$1" == 1 ]; then
        report_error "Can not find running screen with matching name '$SCREEN_NAME'."
        exit 1
    fi
}

#
# Start the server in a dedicated daemon screen and initialize its components.
# Arguments: {command}.
#
start_server() {
    # Prevent duplicate server startup
    SCREEN_PID=$(get_screen_pid)
    if [ ! -z "$SCREEN_PID" ]; then
        report_error "Detected running matching screen with PID "$SCREEN_PID"."
        exit 1
    fi
    # Start the server daemon screen
    cd "$SERVER_BASE"
    report_info "Running server screen under '$SERVER_BASE'."
    call_screen -dmUS "$SCREEN_NAME" -t SERVER "$@"
    sleep 2 # Wait for the screen to come up or crash
    SCREEN_PID=$(get_screen_pid)
    if [ -z "$SCREEN_PID" ]; then
        report_error "Failed to start the main server screen."
        exit 1
    else
        report_info "Started daemon screen '$SCREEN_NAME' with PID $SCREEN_PID."
    fi
}

#
# Stop server's daemon screen process (stops the server and components).
#
stop_server() {
    SCREEN_PID=$(get_screen_pid 1)
    if [ ! -z "$SCREEN_PID" ]; then
        report_info "Stopping matched screen with PID "$SCREEN_PID"..."
        call_screen -S "$SCREEN_PID"."$SCREEN_NAME" -X quit
        # Wait for the screen to terminate.
        sleep 2 # TODO implement checking in loop
        report_info "Server daemon screen stopped."
    fi
}

#
# Start server component inside its daemon screen.
# Arguments: {name} {command}.
#
start_component() {
    COMPONENT_NAME="$1"
    report_info "Starting server component '"$COMPONENT_NAME"'."
    SCREEN_PID=$(get_screen_pid 1)
    if [ -z "$SCREEN_PID" ]; then
        exit 1
    fi
    # Create new window for the component
    call_screen -S "$SCREEN_PID"."$SCREEN_NAME" -X screen -t "$COMPONENT_NAME"
    # Start the component
    call_screen -S "$SCREEN_PID"."$SCREEN_NAME" -p "$COMPONENT_NAME" -X stuff "exec ${*:2}\r"
}

#
# Stop the specified server component.
# Arguments: {name}.
#
stop_component() {
    COMPONENT_NAME="$1"
    report_info "Stopping server component '$COMPONENT_NAME'."
    SCREEN_PID=$(get_screen_pid 1)
    if [ -z "$SCREEN_PID" ]; then
        exit 1
    fi
    call_screen -S "$SCREEN_PID"."$SCREEN_NAME" -p "$1" -X kill
}

#
# Get status of server daemon screen and its components (windows).
#
server_status() {
    SCREEN_PID=$(get_screen_pid)
    if [ -z "$SCREEN_PID" ]; then
        report_info "No running screen matches '$SCREEN_NAME'."
    else
        SCREEN_COMPONENTS=$(screen -S "$SCREEN_PID"."$SCREEN_NAME" -Q windows)
		report_info "Running components: $SCREEN_COMPONENTS."
    fi
}

