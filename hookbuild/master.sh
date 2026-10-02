#!/bin/bash
# usage: master.sh in.wav out.m4a
FF=ffmpeg
J=$($FF -hide_banner -i "$1" -af loudnorm=I=-14:TP=-2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
$FF -v error -y -i "$1" -af "loudnorm=I=-14:TP=-2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,alimiter=limit=0.70:level=false,aresample=48000" -c:a aac -b:a 192k "$2"
$FF -hide_banner -i "$2" -af ebur128=peak=true -f null - 2>&1 | grep -A1 "Integrated loudness" | grep "I:" ; $FF -hide_banner -i "$2" -af ebur128=peak=true -f null - 2>&1 | grep -A1 "True peak" | grep Peak
