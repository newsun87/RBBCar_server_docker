# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template,Response
import requests
import json
import os, shutil
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess
import time
import configparser
import paho.mqtt.client as mqtt
import serial

config = configparser.ConfigParser()
config.read('RBBCar_server.conf')
RBBCar_num = config.get('RBBCar', 'device_num')
print('RBBCar_num', RBBCar_num)
MQTT_Broker_url = config.get('MQTT_broker', 'url')
MQTT_Broker_port = int(config.get('MQTT_broker', 'port'))
move_detector_flag = config.get('Move_Detect', 'move_detector_flag')
config.set('Move_Detect', "move_detector_flag", "1") # 寫入設定檔
config.write(open("RBBCar_server.conf", "w")) 


#取得通行憑證
cred = credentials.Certificate("serviceAccount.json")
database_url = config.get('firebase', 'database_url')
firebase_admin.initialize_app(cred, {
    'databaseURL' : database_url
})

ref = db.reference('/') # 參考路徑
cups_ref=ref.child('RBBCar_server/%s' % RBBCar_num.strip('"'))
app = Flask(__name__)

# import camera driver
"""if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_opencv import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

@app.route('/')
def index():
    #Video streaming home page.
    return render_template('index.html')


def gen(camera):
    #Video streaming generator function.
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag.
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
"""

# paho callbacks
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc)) 
  client.subscribe("RBBCar/control/" + RBBCar_num, qos=1) # 用戶訂閱主題
  
def on_message(client, userdata, msg): # 收到訂閱訊息的處理       
    print(msg.topic + " " + msg.payload.decode())       
    if msg.topic == "RBBCar/control/" + RBBCar_num :       
      receive_ctl(msg.payload.decode())      
      
def initial():  
  os.system("sh ngrok_url_linenotify.sh") 
  os.system("sh get_config.sh")  
  # 寫入 firebase realtimebase  
  with open("config.json", 'r')as f:
   for line in f.readlines():
    data = json.loads(line)
    print(data)    
    cups_ref.set(data)
    
def receive_ctl(ctl_data):
  serial_port = config.get('Arduino_communication', 'port')
  baud = int(config.get('Arduino_communication', 'baudrate'))
  #目前所在絕對路徑
  basepath = os.path.dirname(__file__)
  print(basepath)
  file_path = os.path.join(basepath, 'control_data.txt')  
  ser = serial.Serial(serial_port, baudrate=baud,timeout=3.0)
  if ser.isOpen():
    print(ser.name + ' is open...')
    with open(file_path, 'w', encoding="UTF-8") as f: # 打開文件
     f.write(ctl_data)  
    temp = ' '  #設定空字串
    with open(file_path, 'r') as f: # 打開文件
      data = f.read().strip("\n")  # 讀取控制字元        
      if data == 'exit':
        cmd = 's'
        ser.write(cmd.encode('UTF-8')+ b"\n")  #送出控制字元
        ser.close()
        print('port is closed')        
      else:  
        if data != temp:
          print(data) #印出控制字元
          ser.write(ctl_data.encode('UTF-8')+ b"\n") #送出控制字元
          temp = data 
  else: 
    print("cannot communicate with Arduino!")	     
                
    
if __name__ == "__main__":
 initial() 
 os.system("./start_mjpg-streamer.sh")
 client = mqtt.Client()  
 client.on_connect = on_connect  
 client.on_message = on_message  
 client.connect(MQTT_Broker_url, MQTT_Broker_port) 
 client.loop_start()     
 app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)          
