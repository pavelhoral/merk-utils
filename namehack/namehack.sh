#!/bin/bash
#
# Name Hack IPTABLES rule management script.
#
# Supported variables:
#  
# - SERVER_PORT = Server port (defaults to 16567).
# - CHECK_CHAIN = Name of the checking IPTABLES chain (defaults to NAMEHACK).
# - CHECK_PREFIX = Log prefix for checking chain (defaults to "$CHECK_CHAIN: ").
# - CHECK_FILTER = Rule for u32 netfilter (not intended to be modified).
# - REJECT_CHAIN = Name of the rejecting IPTABLES chain (defaults to "$CHECK_CHAIN"_REJECT).
# - REJECT_PREFIX = Log prefix for rejection chain (defaults to "$REJECT_CHAIN: ").
#

if [ -z "$SERVER_PORT" ]; then
    SERVER_PORT="16567"
fi

if [ -z "$CHECK_CHAIN" ]; then
    CHECK_CHAIN="NAMEHACK"
fi
CHECK_PREFIX="$CHECK_CHAIN: "
CHECK_FILTER="0>>22&0x3C@8>>24&0xEF=0x0F && 0>>22&0x3C@20=0x01000000 && 0>>22&0x3C@25=0x00000004"

if [ -z "$REJECT_CHAIN" ]; then
    REJECT_CHAIN="$CHECK_CHAIN"_REJECT
fi
REJECT_PREFIX="$REJECT_CHAIN: "

# Play it safe from this point
set -e

#
# Clean-up all custom IPTABLES rules and chains.
#
function cleanup {
    # Delete existing INPUT rules 
    iptables -n -L INPUT --line-numbers | awk "\$2==\"$CHECK_CHAIN\" { print \$1 }" | tac | xargs -r iptables -D INPUT
    # Flush and delete the CHECK chain
    if iptables -n -L $CHECK_CHAIN 2&> /dev/null; then
        iptables -F $CHECK_CHAIN
        iptables -X $CHECK_CHAIN
    fi
    # Flush and delete the REJECT chain
    if iptables -n -L $REJECT_CHAIN 2&> /dev/null; then
        iptables -F $REJECT_CHAIN
        iptables -X $REJECT_CHAIN
    fi 
}

#
# Re-initialize CHECK and REJECT chains.
#
function reinit {
    cleanup
    iptables -N "$CHECK_CHAIN"
    iptables -A "$CHECK_CHAIN" -j LOG --log-prefix "$CHECK_PREFIX" --log-level 6
    iptables -A INPUT -p udp --dport $SERVER_PORT \! -f -m u32 --u32 "$CHECK_FILTER" -j "$CHECK_CHAIN" 
    iptables -N "$REJECT_CHAIN"
    iptables -A "$REJECT_CHAIN" -j LOG --log-prefix "$REJECT_PREFIX" --log-level 4
    iptables -A "$REJECT_CHAIN" -j DROP
}

#
# Append new CHECK chain rule for the specified player.
#
function append {
    PLAYER_NAME="$1"
    if [ -z "$PLAYER_NAME" ]; then
        echo "Missing player name."
        exit 1
    fi
    NAME_HEX=$(xxd -pu <<< "$PLAYER_NAME")
    # Standard check
    NAME_LENGTH=$(printf "%02x\n" ${#PLAYER_NAME})
    iptables -A "$CHECK_CHAIN" -j "$REJECT_CHAIN" \
            -m string --hex-string "$NAME_LENGTH$NAME_HEX" --from 50 --to 51 --algo bm \
            -m comment --comment "$PLAYER_NAME"
    # Null-terminated check
    iptables -A "$CHECK_CHAIN" -j "$REJECT_CHAIN" \
            -m string --hex-string "$NAME_HEX"00 --from 51 --to 52 --algo bm \
            -m comment --comment "$PLAYER_NAME"
}

case "${1:-''}" in
    cleanup)
        cleanup
        ;;
    reinit)
        reinit
        ;;
    append)
        append "$2"
        ;;
    *)
        echo "Usage: $SELF cleanup|reinig"
        exit 1
        ;;
esac
