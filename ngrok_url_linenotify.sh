#!/bin/bash
sudo kill $(pidof ngrok)
ngrok http 8085 > /dev/null& 
sleep 3
#���o���浲�G(��})���ܼ�
URL4040=$(curl -s localhost:4040/api/tunnels | awk -F"https" '{print $2}' | awk -F"//" '{print $2}' | awk -F'"' '{print $1}')
ACCESS_TOKEN="OyXZt3qv2S4erlzd7EkSq8dRPioaCZc5rMAAS4v5aOn" #Line Notify �����ҽX
message="RBBCar_CAM-URL https://"$URL4040"/?action=stream"  #�ǤJCUPS server ���}
echo $URL4040"/?action=stream" > ngrok_url.txt
curl https://notify-api.line.me/api/notify -X POST \
   -H "Authorization: Bearer $ACCESS_TOKEN" \
   -F "message=$message"  
