from urllib.request import urlopen
from flask import Flask, request, render_template
import pandas as pd
import json
import requests
import socket
import time
from datetime import datetime
from pymongo import MongoClient
import requests
from src.feature_engineering import clean_pipeline
from src.predict import predict_one


app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['web_scraped']
table = db['new_data_pt']

# home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/stream_data', methods = ['GET'])
def get_data():
    '''
    Return new data through webscraping
    '''
    # Parsing JSON file from url
    url = 'http://galvanize-case-study-on-fraud.herokuapp.com/data_point'

    # This returns a dataframe with that datapoint
    r = requests.get(url)
    json_data = r.json()
    datapoint_df = pd.DataFrame.from_dict(json_data, orient='index').transpose()
    prob, pred = predict_one(datapoint_df)

    pred_dict = {
        0: "Legitimate",
        1: "Fraud"
    }

    if prob < 0.1:
        risk = "Low"
    elif prob >= 0.1 and prob <= 0.4:
        risk = "Medium"
    else:
        risk = "High"

    json_data['prediction'] = int(pred)
    json_data['prediction_probability'] = float(prob)
    json_data['fraud_risk'] = risk
    json_data['prediction_timestamp'] = int(time.time())

    if db.new_data.count_documents({"object_id": json_data['object_id']}) == 0:
        db_add_string = f"Added to DB with object_id: {json_data['object_id']}"
    else:
        db_add_string = f"Object already in DB with object_id: {json_data['object_id']}"
        db.new_data.delete_one({"object_id": json_data['object_id']})

    db.new_data.insert_one(json_data)

    data_dict = {
        "Event_Name": json_data['name'],
        "Event_Org": json_data['org_name'],
        "Event_Country": json_data['country'],
        "Prediction": pred_dict[pred],
        "Fraud_Probability": round(prob, 2),
        "Fraud_Risk": risk
    }

    return render_template('stream_data.html', data=data_dict, db_add_string=db_add_string)


@app.route('/view_data')
def view_data():
    data = db.new_data.find({"object_id": {"$exists": True}}).sort([("prediction_timestamp", -1)]).limit(10)
    df_results = pd.DataFrame(data, columns=['prediction', 'prediction_probability', 'fraud_risk', 'object_id', 'name', 'email_domain']).round(2)
    df_results.columns = ['Prediction', 'Fraud Probability', 'Fraud Risk', 'Event ID', 'Event Name', 'Email Domain']
    return render_template('view_data.html', data=df_results.to_html(index=False, justify='left', border=2, classes='table table-hover', header="true"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
