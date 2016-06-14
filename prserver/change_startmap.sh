#!/bin/bash

#The script is used in $SERVER_BASE/start_pr.sh

maps[0]='mapList.append jabal gpm_skirmish 16'
maps[1]='mapList.append qwai1 gpm_skirmish 16'
maps[2]='mapList.append sbeneh_outskirts gpm_skirmish 16'
maps[3]='mapList.append hill_488 gpm_skirmish 16'
maps[4]='mapList.append nuijamaa gpm_skirmish 16'
maps[5]='mapList.append lashkar_valley gpm_skirmish 16'
maps[6]='mapList.append kokan gpm_skirmish 16'
maps[7]='mapList.append shijiavalley gpm_skirmish 16'
maps[8]='mapList.append bijar_canyons gpm_skirmish 16'
maps[9]='mapList.append burning_sands gpm_skirmish 16'
maps[10]='mapList.append silent_eagle gpm_skirmish 16'
maps[11]='mapList.append gaza gpm_skirmish 16'
maps[12]='mapList.append vadso_city gpm_skirmish 16'
maps[13]='mapList.append dragon_fly gpm_skirmish 16'
maps[14]='mapList.append xiangshan gpm_skirmish 16'
maps[15]='mapList.append black_gold gpm_vehicles 64'
maps[16]='mapList.append sbeneh_outskirts gpm_vehicles 64'
maps[17]='mapList.append black_gold gpm_skirmish 16'
maps[18]='mapList.append operation_marlin gpm_skirmish 16'
maps[19]='mapList.append ulyanovsk gpm_skirmish 16'
maps[20]='mapList.append khamisiyah gpm_skirmish 16'

rand=$(shuf -i 0-20 -n 1)
echo $(date)
echo ${maps[$rand]}
theMap=${maps[$rand]}

#Create temporary file with new line in place
cat /home/pr/prMain/mods/pr/settings/maplist.con | sed -e "19s/.*/${theMap}/" > /tmp/temp_maplist.con

#Copy the new file over the original file
mv /tmp/temp_maplist.con /home/pr/prMain/mods/pr/settings/maplist.con
