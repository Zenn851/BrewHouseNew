import time
import paho.mqtt.client as mqtt
import json
from random import randint


class ThingsBoardData():
    def __init__(
                self,
                name,
                #iot_hub="thingsboard.cloud",
                iot_hub="demo.thingsboard.io",
                username= "7DUh4Kb6IbFgndXKpER3",
                password="",
                topic="v1/devices/me/telemetry",
                port = 1883):

        self.name = name
        self.iot_hub = iot_hub
        self.username = username
        self.password = password
        self.topic = topic
        self.port = port
        self.client=mqtt.Client()
        self.client.username_pw_set(self.username,self.password)

    def thingsConnect(self):
        self.client.connect(self.iot_hub,self.port)


    def thingsData(self,temp,setTemp,status):
        data=dict()
        data[self.name+" Temp"]= temp
        data[self.name+" Set Temp"]= setTemp
        #data[self.name+ " Status"] = status
        data_out = json.dumps(data)
        self.client.publish(self.topic,data_out,0)
        print(data_out)

    def thingsDisconnect(self):
        self.client.disconnect()

    def testName(self):
        print(self.name)


if __name__ == '__main__':
    x=ThingsBoardData("FV1")
    while True:
        x1 = randint(65,75)
        x2 = 68
        y1 = True
        time.sleep(1)
        x.thingsConnect()
        x.thingsData(x1,x2,y1)
        time.sleep(1)
        #x.thingsDisconnect()
