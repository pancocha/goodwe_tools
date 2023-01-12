#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import asyncio
import goodwe

hostName = "192.168.0.1"
serverPort = 8080
inverter = 0
runtime_data = 0
brief_sensors = {'timestamp',
                'ppv',
                'load_ptotal',
                'house_consumption',
                'battery_soc',
                'active_power',
                'pbattery1',
                'battery_mode_label',
                'e_day_exp',
                'e_day_imp',
                'e_bat_charge_day',
                'e_bat_discharge_day',
                'e_load_day',
                'e_day',
                'battery_temperature'
                }

async def inverter_init():
    global inverter
    ip_address = '192.168.0.103'
    inverter = await goodwe.connect(ip_address)

async def get_runtime_data():
    global inverter
    global runtime_data
    ip_address = '192.168.0.103'

#    inverter = await goodwe.connect(ip_address)
    runtime_data = await inverter.read_runtime_data()

#    for sensor in inverter.sensors():
#        if sensor.id_ in runtime_data:
#            print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")

class exporter(BaseHTTPRequestHandler):
    def do_GET(self):
        global inverter
        global runtime_data
        global brief_sensors
        asyncio.run(get_runtime_data())
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Goodwe stats</title></head><style>table { font-size: 2em; } </style>\n", "utf-8"))
        self.wfile.write(bytes("<body>\n", "utf-8"))
        #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<table>\n", "utf-8"))
        for sensor in inverter.sensors():
            if sensor.id_ in runtime_data and ((self.path == "/all") or (sensor.id_ in brief_sensors)):
                line=f"<tr><td>{sensor.id_}</td><td>{sensor.name}</td><td>{runtime_data[sensor.id_]} {sensor.unit}</td></tr>\n"
                #print(line)
                self.wfile.write(bytes(line,"utf-8"))

        self.wfile.write(bytes("</table>\n", "utf-8"))
        self.wfile.write(bytes("</body></html>\n", "utf-8"))

if __name__ == "__main__":        
    asyncio.run(inverter_init())
    webServer = HTTPServer((hostName, serverPort), exporter)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
