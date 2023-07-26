#!/bin/bash

paths=("/net/em-support3/Krios1/" "/net/em-support3/Krios2/" "/net/em-support3/Krios3/" "/net/cista1/Krios4Falcon/" "/net/em-support3/Glacios/")

for i in ${!paths[@]}
do
	path=${paths[$i]}
	find $path -maxdepth 4 -type f -newermt 20230101 -not -newermt 20240101 -name EpuSession.dm 2>/dev/null > scope$i
	#python3 parse_epu_session.py scope$i
done

