#!/usr/bin/env python3

import csv
import os
import time

sensors = ["28-0721705c2caa", "28-0207924579fa"]  # multiple sensors    sensors = ["28-0721705c2caa", "28-0207924579fa"]
sensors_map = { sensors[0]: "FV1  = ",
                sensors[1]: "FV2 = "}

def read_temp(id):
  sensor = "/sys/devices/w1_bus_master1/" + id + "/w1_slave"
  temp = -125.0 # error value
  try:
    f = open(sensor, "r")
    data = f.read()
    f.close()
    if "YES" in data:
      partitioned = data.partition(' t=')
      temp = float(partitioned[2]) / 1000.0
      temp = temp * 9.0 / 5.0 + 32.0
      temp = round(temp, 2)
      #temp_f = temp_c * 9.0 / 5.0 + 32.0
  except Exception:
    pass

  return temp

temps = {}
timenow = time.asctime
for sensor in sensors:
  temp = read_temp(sensor)
  print('%s%.2f' % (sensors_map[sensor], temp))
  temps[sensor]=temp


with open('ds18b20temps.csv', 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow([timenow(), temps[sensors[0]], temps[sensors[1]]])
  
print(read_temp("28-0721705c2caa"))
