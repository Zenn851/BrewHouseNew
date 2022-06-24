import time
import paho.mqtt.client as mqtt
import json
from random import randint
import pandas as pd


class ThingsBoardData():
    def __init__(
                self,
                iot_hub="demo.thingsboard.io",
                username= "uvrGfmOoDWd4b7aEvOzn",
                password="",
                topic="v1/devices/me/telemetry",
                port = 1883):

        #self.name = name
        self.iot_hub = iot_hub
        self.username = username
        self.password = password
        self.topic = topic
        self.port = port
        self.client=mqtt.Client()
        self.client.username_pw_set(self.username,self.password)

    def thingsConnect(self):
        try:
            self.client.connect(self.iot_hub,self.port)
        except Exception:
            print("connection failed")

    def thingsData(self,data_out):
        try:
            self.client.publish(self.topic,data_out,0)

        except Exception:
            print("publish failed")

        #print(data_out)

    def thingsDisconnect(self):
        self.client.disconnect()



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
