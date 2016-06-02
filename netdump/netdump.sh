#!/bin/bash
#
# Listen for server related network traffic and store it in PCAP files.
#
# Supported variables:
#  
# - SERVER_BASE = Base directory for the server (defaults to script's dirname).
# - TCPDUMP_BASE = Base directory for PCAP files (defaults to `$SERVER_BASE/netdump`).
# - TCPDUMP_FILTER = Filter for tcpdump (defaults to UDP 29900/16567 and TCP 4712).
#

if [ -z "$TCPDUMP_BASE" ]; then
    if [ -z "$SERVER_BASE" ]; then
        SERVER_BASE=$(dirname "$0")
    fi
    TCPDUMP_BASE="$SERVER_BASE/netdump"
fi
if [ -z "$TCPDUMP_FILTER" ]; then
    TCPDUMP_FILTER="udp port 29900 or udp port 16567 or tcp port 4712"
fi

tcpdump -pni eth0 -s65535 -G 600 -w "$TCPDUMP_BASE/trace_%Y-%m-%d_%H:%M:%S.pcap" "$TCPDUMP_FILTER"

