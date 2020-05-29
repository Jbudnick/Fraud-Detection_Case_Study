from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime

app = Flask(__name__)
PORT = 8000

# routing blocks - note there is only one in this case - @app.route('/')

# home page - the first place your app will go
# GET is the default, more about GET and POST below
@app.route('/', methods=['GET', 'POST'])
# the function below will be executed at the host and port followed by '/'
# the name of the function that will be executed at '/'. Its name is arbitrary.
def index():
    return 'Hello!'

# no more routing blocks


if __name__ == '__main__':
    #AWS Instance - start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
