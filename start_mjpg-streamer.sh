#!/bin/bash
 
sudo kill $(pidof  mjpg_streamer)
/usr/local/bin/mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_uvc.so -n -f 10 -r 640x480" -o "/usr/local/lib/mjpg-streamer/output_http.so -p 8085 -w /usr/local/share/mjpg-streamer/www" > /dev/null&
echo "mjpg_streamer started"
