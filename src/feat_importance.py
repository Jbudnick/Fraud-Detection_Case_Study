from joblib import load
import numpy as np
import pandas as pd
import matplotlib as plt

from src.feature_engineering import clean_pipeline

model = load("models/randomforest.joblib")
importances = model.steps[1][1].feature_importances_
std = np.std([tree.feature_importances_ for tree in model.steps[1][1].estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")
# Load in data
total_df = pd.read_json('data/data.json')

# Run whole data through feature engineering pipeline
clean_df = clean_pipeline(total_df)


X = clean_df.drop(["target"], axis=1)
names = [X.columns[i] for i in indices]

for f in range(10):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# sorted(zip(map(lambda x: round(x,4), model.steps[1][1].feature_importances_),  