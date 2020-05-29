from joblib import load
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

model = load("models/randomforest.joblib")
importances = model.steps[1][1].feature_importances_
std = np.std([tree.feature_importances_ for tree in model.steps[1][1].estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
# print("Feature ranking:")
feature_names = model.steps[0][1].get_feature_names()

# for f in range(10):
#     print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# sorted(zip(map(lambda x: round(x,4), model.steps[1][1].feature_importances_),  

important_features = pd.Series(data=importances,index=feature_names)
important_features.sort_values(ascending=False,inplace=True)
important_features.nlargest(15).plot(kind = 'barh')
plt.title("Top 15 important features")
plt.savefig('images/feat_import.png')
print(important_features.nlargest(15))