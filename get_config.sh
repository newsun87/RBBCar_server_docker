#!/bin/bsah
r1=`hostname -I | awk -F ' '  '{print $1}'`
r2=`iwconfig wlan0 | grep wlan0 | awk -F '"'  '{print $2}'`
r3=`cat RBBCar_server.conf | grep device_num | awk -F '=' '{print $2}'`
r4=`cat ngrok_url.txt`
printf '{"hostname":"%s","ap":"%s", "device_num":"%s", "ngrok_url":"%s"}\n' "$r1" "$r2" "$r3" "$r4"> config.json
#./start_mjpg-streamer.sh
