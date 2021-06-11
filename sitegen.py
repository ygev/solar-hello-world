#!/usr/bin/python

import datetime
import jinja2
import subprocess
import time

def uptime_sec():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return int(uptime_seconds)

uptime = str(datetime.timedelta(seconds=uptime_sec()))
temp = subprocess.run(["/opt/vc/bin/vcgencmd", "measure_temp"], capture_output=True).stdout.decode('utf-8')[5:-1]

template = """
<html lang="en">
<head>
    <title>kians solar panel</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        html {
            background: LemonChiffon;

        }
        body {
            background: LemonChiffon;
            color: #333;
            padding: 2em 1em;
            font-size: 2em;
        }
    </style>
</head>
<body>
    <h1>kians solar panel</h1>
    <p>temperature: {{ temp }}</p>
    <p>uptime: {{ uptime }}</p>
    <p>last updated: {{ time }} UTC</p>
</body>
</html>
"""

data = {
    "temp": temp,
    "uptime": uptime,
    "time": time.ctime()
}
rendered = jinja2.Template(template).render(data)

#print(rendered)
with open('/var/www/html/index.html', 'w') as the_file:
    the_file.write(rendered)
