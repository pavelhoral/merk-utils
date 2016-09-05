#!/bin/bash
#
# Collect debug data in case of a server crash for later inspection.
# This script can be directly linked as `on_after_crash.sh` event script.
#
# Supported variables:
#
# - SERVER_BASE = Base directory for the server (defaults to script's dirname).
# - SERVER_NAME = Symbolic name of the server (defaults to basename of `$SERVER_BASE`).
# - TCPDUMP_BASE = Base directory for PCAP files (defaults to `$SERVER_BASE/netdump`).
# - BACKUP_BASE = Base directory for data backup (defaults to `$SERVER_BASE/backup/crash`).
# - LOG_FILE = Path to the script's log file (defaults to `$SERVER_BASE/server.log`).
#

if [ -z "$SERVER_BASE" ]; then
   SERVER_BASE=$(dirname "$0")
fi
if [ -z "$SERVER_NAME" ]; then
    SERVER_BASE=$(readlink -f "$SERVER_BASE")
    SERVER_NAME=$(basename "$SERVER_BASE")
fi
if [ -z "$BACKUP_BASE" ]; then
    BACKUP_BASE="$SERVER_BASE/backup/crash"
fi
if [ -z "$TCPDUMP_BASE" ]; then
    TCPDUMP_BASE="$SERVER_BASE/netdump"
fi
if [ -z "$LOG_FILE" ]; then
    LOG_FILE="$SERVER_BASE/server.log"
fi

# Prefix for collected data files
DATA_PREFIX="$(date +"%Y-%m-%d_%H:%M:%S")_$SERVER_NAME"

#
# Backup core dump
#
backup_core() {
    mv core "$BACKUP_BASE/$PREFIX"_core
}

#
# Backup net dump
#
backup_netdump() {
    if [ ! -d "$TCPDUMP_BASE" ]; then
        exit 0
    fi
    local TCPDUMP_FILE =$(ls -1t "$TCPDUMP_BASE" | head -1)
    if [ ! -z "$TCPDUMP_FILE" ]; then
        cp "$TCPDUMP_BASE"/"$TCPDUMP_FILE" "$BACKUP_BASE/$PREFIX"_tcpdump
    fi
}

#
# Backup server output
#
backup_output() {
    if [ -f "$SERVER_BASE/server.out" ]; then
        tail -n 1 "$LOG_FILE" >> "$SERVER_BASE/server.out"
        mv "$SERVER_BASE/server.out" "$BACKUP_BASE/$PREFIX"_server.out
    fi
}

# Call the backupt routines
backup_core
backup_netdump
backup_output
