#!/usr/bin/python

print("Starting sitegen")

import board
import datetime
import jinja2
import subprocess
import time
import os
import pytz
from datetime import datetime
from adafruit_lc709203f import LC709203F
import rrdtool

# create new rrd database
#rrdtool.create("battery.rrd", "--step", "300", "DS:battery:GAUGE:600:0:100", "RRA:AVERAGE:0.5:1:288", "RRA:AVERAGE:0.5:1:2016")

sensor = LC709203F(board.I2C())
print("Battery monitor chip version:", hex(sensor.ic_version))

outdir = "/var/www/html"

while True:
    try:
        print("reading template...")
        with open('index.html', 'r') as the_file:
            template = the_file.read()

        print("rendering...")

        uptime = subprocess.run(["/usr/bin/uptime", "-p"], capture_output=True).stdout.decode('utf-8')[3:]
        temp = subprocess.run(["/opt/vc/bin/vcgencmd", "measure_temp"], capture_output=True).stdout.decode('utf-8')[5:-1].replace('\'', '°')

        tz = pytz.timezone('America/Los_Angeles')
        dt = datetime.now(tz)
        now = dt.strftime('%c %Z')

        # display rrd graph in correct timezone
        os.environ['TZ'] = 'America/Los_Angeles'
        time.tzset()

        try:
            battery = "%0.1f%% (%0.3fv)" % (sensor.cell_percent, sensor.cell_voltage)
            rrdtool.update("battery.rrd", f"N:{sensor.cell_percent}")
            rrdtool.graph(f"{outdir}/battery-24h.png", "DEF:bat=battery.rrd:battery:AVERAGE", "LINE2:bat#FF0000", "-l", "0", "-u", "100", "-v", "percent", "-t", "battery level (24h)", "--zoom", "1.5")
            rrdtool.graph(f"{outdir}/battery-7d.png", "DEF:bat=battery.rrd:battery:AVERAGE", "LINE2:bat#FF0000", "-l", "0", "-u", "100", "-v", "percent", "-t", "battery level (7d)", "--zoom", "1.5", "--end", "now", "--start", "end-7d")
        except Exception as err:
            battery = err

        data = {
            "temp": temp,
            "uptime": uptime,
            "battery": battery,
            "time": now
        }
        print(data)
        rendered = jinja2.Template(template).render(data)

        print("writing to file...")
        with open(f"{outdir}/index.html", "w") as the_file:
            the_file.write(rendered)

        print("done")
        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(30)
