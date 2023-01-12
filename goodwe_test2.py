#!/usr/bin/python3
import asyncio
import goodwe


ip_address = '192.168.0.103'

inverter = goodwe.connect(ip_address)
runtime_data = inverter.read_runtime_data()

for sensor in inverter.sensors():
    if sensor.id_ in runtime_data:
        print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")
