#!/usr/bin/python

print("Starting sitegen")

import board
import datetime
import jinja2
import subprocess
import time
from adafruit_lc709203f import LC709203F

sensor = LC709203F(board.I2C())
print("Battery monitor chip version:", hex(sensor.ic_version))

while True:
    try:
        print("reading template...")
        with open('index.html', 'r') as the_file:
            template = the_file.read()

        print("rendering...")

        uptime = subprocess.run(["/usr/bin/uptime", "-p"], capture_output=True).stdout.decode('utf-8')[3:]
        temp = subprocess.run(["/opt/vc/bin/vcgencmd", "measure_temp"], capture_output=True).stdout.decode('utf-8')[5:-1].replace('\'', '°')

        try:
            battery = "%0.1f%% (%0.3fv)" % (sensor.cell_percent, sensor.cell_voltage)
        except Exception as err:
            battery = err

        data = {
            "temp": temp,
            "uptime": uptime,
            "battery": battery,
            "time": time.ctime()
        }
        rendered = jinja2.Template(template).render(data)

        print("writing to file...")
        with open('/var/www/html/index.html', 'w') as the_file:
            the_file.write(rendered)

        print("done")
        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(30)
