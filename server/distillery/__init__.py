import os
import sqlite3
from flask import Flask
app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

import distillery.sensorGET
import distillery.sensorPOST
import distillery.actuator
