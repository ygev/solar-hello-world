#!/usr/bin/python

print("Importing modules...")

import datetime
import jinja2
import subprocess
import time

def uptime_sec():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return int(uptime_seconds)

print("reading template...")
with open('index.html', 'r') as the_file:
    template = the_file.read()

print("rendering...")

uptime = str(datetime.timedelta(seconds=uptime_sec()))
temp = subprocess.run(["/opt/vc/bin/vcgencmd", "measure_temp"], capture_output=True).stdout.decode('utf-8')[5:-1]

data = {
    "temp": temp,
    "uptime": uptime,
    "time": time.ctime()
}
rendered = jinja2.Template(template).render(data)

print("writing to file...")
with open('/var/www/html/index.html', 'w') as the_file:
    the_file.write(rendered)

print("done")
