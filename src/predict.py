from joblib import load
import pickle

from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np
import json

from feature_engineering import clean_pipeline

if __name__ == "__main__":
    
    pipe = load("models/randomforest.joblib")
    
    with open('models/column_list.pkl', 'rb') as f:
        train_columns = pickle.load(f)

    df = pd.DataFrame(pd.read_json('example.json'), columns=train_columns)

    pipe.predict(df)