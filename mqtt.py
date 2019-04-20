from clearblade.ClearBladeCore import System, Query, Developer
import time
import psutil
import json
import datetime
from datetime import datetime


def get_resource():
    svmem = psutil.virtual_memory()
    batt = psutil.sensors_battery()
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if batt[2]:
        power = 1
    else:
        power = 0
    dic = {"time": t, "vm_percent": svmem[2], "battery_percent": batt[0], "secsleft": batt[1],"power_plugged": power}
    js = json.dumps(dic)
    return js

SystemKey = "dce7d4cb0b80c1eec1bbbaa9a262"
SystemSecret = "DCE7D4CB0BC2A092D3E1FFC3D831"

mySystem = System(SystemKey, SystemSecret)
email = "jiang50@tamu.edu"
password = "jyc19961007"


jiang = mySystem.User(email, password)
mqtt = mySystem.Messaging(jiang)


def on_connect(client, userdata, flags, rc):
    # When we connect to the broker, start publishing our data to the keelhauled channel
    for i in range(10):
        payload = get_resource()
        print payload
        client.publish("jiang/info", payload)
        time.sleep(3)


#Connect callback to client
mqtt.on_connect = on_connect

# Connect and spin for 30 seconds before disconnecting
mqtt.connect()
time.sleep(30)
mqtt.disconnect()




