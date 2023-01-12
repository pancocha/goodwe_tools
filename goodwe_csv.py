#!/usr/bin/python3
import asyncio
import goodwe
import argparse

parser = argparse.ArgumentParser(usage=" ./goodwe_csv.py -ip 192.168.0.103")
parser.add_argument('-ip', '--ip-address', required=True, help='Invertor IP address')
parser.add_argument('-f', '--field-names', action='store_true', help='Add CSV header')
parser.add_argument('-t', '--table', action='store_true', help='Tabular output')

args = parser.parse_args()


async def get_runtime_data():
    inverter = await goodwe.connect(args.ip_address)
    runtime_data = await inverter.read_runtime_data()

    if args.table:
        for sensor in inverter.sensors():
            if sensor.id_ in runtime_data:
                print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")
    else:
        header=''
        if args.field_names:
            for sensor in inverter.sensors():
                if sensor.id_ in runtime_data:
                    header += sensor.id_
                    header += ';'
            print(header[0:-1])

        data=''
        for sensor in inverter.sensors():
            if sensor.id_ in runtime_data:
                data += str(runtime_data[sensor.id_])
                data += ';'
        print(data[0:-1])

asyncio.run(get_runtime_data())
