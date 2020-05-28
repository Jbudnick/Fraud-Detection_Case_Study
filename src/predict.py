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
    
    # Load in model that was created in build_model.py
    pipe = load("models/randomforest.joblib")
    
    # Load training data columns to match structure before running through the pipeline
    with open('models/column_list.pkl', 'rb') as f:
        train_columns = pickle.load(f)

    # Load example data point
    df = pd.read_json('example.json')

    # Run through feature engineering pipeline
    df_clean = clean_pipeline(df)

    # Add columns from original training data to match the structure
    df_clean_structured = pd.DataFrame(df_clean, columns=train_columns)

    # Get probability of fraud
    probs = pipe.predict_proba(df_clean_structured)[:, 1]

    # Make prediction based on a specified threshold
    threshold = 0.15
    y_hat = (probs >= threshold).astype(int)

    print("Prediction:", y_hat)
    print("Probability of Fraud:", probs)
