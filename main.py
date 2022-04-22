print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
import subprocess as sp
import re
import serial.tools.list_ports

mess = ""
bbc_port = "COM8"
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    collect_data = {splitData[1]:splitData[2] }
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "hsqJnITnJGTtdBqzl5FX"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    cmd=1
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setLED":
            temp_data= {"valueLED":jsonobj['params']}
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            if jsonobj['params']:
                cmd=0
            else: cmd=1
        elif jsonobj['method'] == "setFAN":
            temp_data= {"valueFAN":jsonobj['params']}
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            if jsonobj['params']:
                cmd=2
            else: cmd=3
    except:
        pass
    if len(bbc_port) > 0:
        ser.write((str(cmd)+"#").encode())

def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+") #sau khi connect thanh cong thi subscribe vao. cai v1/... la theo dinh dang cua no
    else:
        print("Connection is failed")

# Get longitude latitude 
def getLocation():
    accuracy=3
    pshellcomm=["powershell"]
    pshellcomm.append('add-type -assemblyname system.device; ' \
        '$loc = new-object system.device.location.geocoordinatewatcher;' \
        '$loc.start(); ' \
        'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) ' \
        '{start-sleep -milliseconds 100}; ' \
        '$acc = %d; ' \
        'while($loc.position.location.horizontalaccuracy -gt $acc) ' \
        '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; ' \
        '$loc.position.location.latitude; ' \
        '$loc.position.location.longitude; ' \
        '$loc.position.location.horizontalaccuracy; ' \
        '$loc.stop()' % (accuracy))
    p = sp.Popen(pshellcomm, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
    (out, err) = p.communicate()
    out = re.split('\n', out)
    longitude = float(out[1])
    latitude = float(out[0])
    # print(out)
    return longitude,latitude




client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intesity = 50
counter = 0
    


longitude=106.6297
latitude=10.8231
x=True
while True:
    # collect_data = {'temperature': temp, 'humidity': humi, 'light':light_intesity,'longitude':longitude,'latitude':latitude}
    # temp += 1
    # humi += 1
    # longitude,latitude=getLocation()
    # light_intesity += 1
    # client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    # print(collect_data)
    # Lab 1



    if len(bbc_port)>0:
        readSerial()
    time.sleep(5)