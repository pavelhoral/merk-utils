#!/bin/bash
#
# Change start map for the PR server. 
# This script can be directly linked as `on_before_start.sh` event script. 
#
# Supported variables:
#  
# - SERVER_BASE = Base directory for the server (defaults to script's dirname).
# - STARTUP_MAPS = Array with startup maps (defaults to a predefined list).

if [ -z "$SERVER_BASE" ]; then
   SERVER_BASE=$(dirname "$0")
fi

if [[ ! -v STARTUP_MAPS ]]; then
	STARTUP_MAPS=()
	STARTUP_MAPS+=('jabal gpm_skirmish 16')
	STARTUP_MAPS+=('qwai1 gpm_skirmish 16')
	STARTUP_MAPS+=('sbeneh_outskirts gpm_skirmish 16')
	STARTUP_MAPS+=('hill_488 gpm_skirmish 16')
	STARTUP_MAPS+=('nuijamaa gpm_skirmish 16')
	STARTUP_MAPS+=('lashkar_valley gpm_skirmish 16')
	STARTUP_MAPS+=('kokan gpm_skirmish 16')
	STARTUP_MAPS+=('shijiavalley gpm_skirmish 16')
	STARTUP_MAPS+=('bijar_canyons gpm_skirmish 16')
	STARTUP_MAPS+=('burning_sands gpm_skirmish 16')
	STARTUP_MAPS+=('silent_eagle gpm_skirmish 16')
	STARTUP_MAPS+=('gaza gpm_skirmish 16')
	STARTUP_MAPS+=('vadso_city gpm_skirmish 16')
	STARTUP_MAPS+=('dragon_fly gpm_skirmish 16')
	STARTUP_MAPS+=('xiangshan gpm_skirmish 16')
	STARTUP_MAPS+=('black_gold gpm_vehicles 64')
	STARTUP_MAPS+=('sbeneh_outskirts gpm_vehicles 64')
	STARTUP_MAPS+=('black_gold gpm_skirmish 16')
	STARTUP_MAPS+=('operation_marlin gpm_skirmish 16')
	STARTUP_MAPS+=('ulyanovsk gpm_skirmish 16')
	STARTUP_MAPS+=('khamisiyah gpm_skirmish 16')
	STARTUP_MAPS+=('asad_khal gpm_skirmish 16')
fi

# Pick random startup map
STARTUP_MAP=${STARTUP_MAPS[$RANDOM % ${#STARTUP_MAPS[@]}]}

# Log selection if possible
if [ "$(type -t log_message)" = "function" ]; then
    log_message "Changing start-up map to '$STARTUP_MAP'."
fi

# Replace the startup map
sed -e "19s/.*/mapList.append $STARTUP_MAP/" -i "$SERVER_BASE/mods/pr/settings/maplist.con"  
