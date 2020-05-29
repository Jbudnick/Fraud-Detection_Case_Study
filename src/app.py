from urllib.request import urlopen
from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db = client['web_scraped']
table = db['new_data_pt']
from feature_engineering import clean_pipeline
# from build_model import update_df_with_new

PORT = 8080
app = Flask(__name__)
REGISTER_URL = "http://50.17.242.215:80"
DATA = []
TIMESTAMP = []


@app.route('/')
def welcome():
    return 'Welcome'


@app.route('/score', methods=['POST'])
def score():
    '''
    Return score from prediction script (import script as module and call functions therein)
    '''
    DATA.append(json.dumps(request.json, sort_keys=True,
                           indent=4, separators=(',', ': ')))
    TIMESTAMP.append(time.time())
    return ""

@app.route('/hello', methods = ['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/update_data', methods = ['GET'])
def get_data():
    '''
    Return new data through webscraping
    '''
    url = 'http://galvanize-case-study-on-fraud.herokuapp.com/data_point'
    data_point = urlopen(url)
    contents = data_point.read()
    soup = BeautifulSoup(contents, 'html.parser')
    clean_new_data = clean_pipeline(soup)
    '''
    Need to convert Beautifulsoup data into dataframe, merge it with the existing dataframe -
    Thinking of calling update_df_with_new(df) function that is listed in build_models script to do this
    '''
    return 'Added New Data'

@app.route('/check')
def check():
    line1 = "Number of data points: {0}".format(len(DATA))
    if DATA and TIMESTAMP:
        dt = datetime.fromtimestamp(TIMESTAMP[-1])
        data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        line2 = "Latest datapoint received at: {0}".format(data_time)
        line3 = DATA[-1]
        output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
    else:
        output = line1
    return output, 200, {'Content-Type': 'text/css; charset=utf-8'}


def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)


if __name__ == '__main__':
    # Register for pinging service ( Can't get pinging service to work - need help)

    '''
    ip_address = socket.gethostbyname(socket.gethostname())
    print("attempting to register {}:{}".format(ip_address, PORT))
    register_for_ping(ip_address, str(PORT))

    '''

    # Start Flask app
    # Connect to database once
    # Unpickle model once
    app.run(host='0.0.0.0', port=PORT, debug=True)
