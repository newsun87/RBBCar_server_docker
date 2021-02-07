#!/bin/bash
sudo kill $(pidof ngrok)
ngrok http 8085 > /dev/null& 
sleep 3
#取得執行結果(位址)當變數
URL4040=$(curl -s localhost:4040/api/tunnels | awk -F"https" '{print $2}' | awk -F"//" '{print $2}' | awk -F'"' '{print $1}')
ACCESS_TOKEN="OyXZt3qv2S4erlzd7EkSq8dRPioaCZc5rMAAS4v5aOn" #Line Notify 的驗證碼
message="RBBCar_CAM-URL https://"$URL4040"/?action=stream"  #傳入CUPS server 網址
echo $URL4040"/?action=stream" > ngrok_url.txt
curl https://notify-api.line.me/api/notify -X POST \
   -H "Authorization: Bearer $ACCESS_TOKEN" \
   -F "message=$message"  
