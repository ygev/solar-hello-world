#!/usr/bin/python

print("Starting sitegen")

import datetime
import jinja2
import subprocess
import time

while True:
    try:
        print("reading template...")
        with open('index.html', 'r') as the_file:
            template = the_file.read()

        print("rendering...")

        uptime = subprocess.run(["/usr/bin/uptime", "-p"], capture_output=True).stdout.decode('utf-8')[3:]
        temp = subprocess.run(["/opt/vc/bin/vcgencmd", "measure_temp"], capture_output=True).stdout.decode('utf-8')[5:-1].replace('\'', '°')

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
        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(30)
