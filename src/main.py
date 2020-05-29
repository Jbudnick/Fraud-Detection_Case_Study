from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime

app = Flask(__name__)
PORT = 8000
REGISTER_URL = "http://50.17.242.215"


#AWS Instance - start Flask app
app.run(host='0.0.0.0', port = PORT, debug = True)
