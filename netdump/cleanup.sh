#!/bin/bash
#
# Delete all PCAP files older than 4 hours. This script should be run by CRON.
#
# Supported variables:
#
# - SERVER_BASE = Base directory for the server (defaults to script's dirname).
# - TCPDUMP_BASE = Base directory for PCAP files (defaults to `$SERVER_BASE/netdump`).
#

if [ -z "$TCPDUMP_BASE" ]; then
    if [ -z "$SERVER_BASE" ]; then
        SERVER_BASE=$(dirname "$0")
    fi
    TCPDUMP_BASE="$SERVER_BASE/netdump"
fi

find $TCPDUMP_BASE -maxdepth 1 -name '*.pcap' -mmin +240 -exec rm '{}' \;
