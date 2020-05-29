from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split,RandomizedSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score, recall_score, f1_score
from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from joblib import dump
import pickle

from feature_engineering import clean_pipeline

def roc(fpr,tpr,auc):
    # Plot the ROC curve
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='k',
            label='Luck')
    ax.plot(fpr, tpr, color='b', lw=2, label='Model')
    ax.set_xlabel("False Positive Rate", fontsize=20)
    ax.set_ylabel("True Postive Rate", fontsize=20)
    ax.set_title("ROC curve", fontsize=24)
    ax.text(0.3, 0.7, " ".join(["AUC:",str(auc.round(3))]), fontsize=20)
    ax.legend(fontsize=24)
    # plt.show()
    plt.savefig('images/rf_roc.png')

def random_search(X_train,y_train):
    #random search params
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 1000, num = 20)]
    max_features = ['auto', 'sqrt']
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    min_samples_split = [2, 5, 10]
    min_samples_leaf = [1, 2, 4]
    bootstrap = [True, False]

    random_grid = {'n_estimators': n_estimators,
                'max_features': max_features,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split,
                'min_samples_leaf': min_samples_leaf,
                'bootstrap': bootstrap}

    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    rf_random.fit(X_train, y_train)

    print(rf_random.best_params_)
    # {'classifier__n_estimators': 368, 'classifier__min_samples_split': 2, 'classifier__min_samples_leaf': 1, 'classifier__max_features': 'sqrt', 'classifier__max_depth': None, 'classifier__bootstrap': False}

def update_df_with_new(df):
    '''
    Update current df with new data from app feature?
    '''
    pass

if __name__ == "__main__":

    # Every column in this list will be one-hot-encoded
    one_hot_cols = [
        "domain_country_code",
        "delivery_method",
        "payout_type",
        "currency"
    ]

    # Assemble pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(), 'description'),
            ('category', OneHotEncoder(handle_unknown='ignore'), one_hot_cols),
        ],
    )
    pipe = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=368, min_samples_split=2, max_features='sqrt', bootstrap=False)),
        ]
    )
  
    # Load in data
    total_df = pd.read_json('data/data.json')

    # Run whole data through feature engineering pipeline
    clean_df = clean_pipeline(total_df)

    # Split X and y
    X = clean_df.drop(["target"], axis=1)
    y = clean_df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123, stratify=y)

    # Fit training data to pipeline
    pipe.fit(X_train, y_train)
    
    # Get probailities of fraud
    probs = pipe.predict_proba(X_test)[:, 1]

    # Make predictions based on specified threshold
    threshold = 0.15
    y_hat = (probs >= threshold).astype(int)

    # Evaluate model
    tn, fp, fn, tp = confusion_matrix(y_test, y_hat).ravel()
    fpr = fp/(fp+tn)
    tpr = tp/(tp+fn)
    

    print(pd.DataFrame({
        "pred:fraud": [tp, fp],
        "pred:not_fraud": [fn, tn]
    }, index=['actual:fraud', 'actual:not_fraud']))

    class_rept_dict = classification_report(y_test, y_hat, output_dict=True) 
    class_rept_df = pd.DataFrame(class_rept_dict).transpose()
    print(class_rept_df)

    fpr, tpr, thresholds = roc_curve(y_test, probs, pos_label=1)
    auc = roc_auc_score(y_test, probs)
    print("AUC:", auc)
    roc(fpr,tpr,auc)

    # Fit on whole dataset and save model
    pipe.fit(X, y)
    train_columns = list(X.columns)
    with open('models/column_list.pkl', 'wb') as f:
        pickle.dump(train_columns, f)
    dump(pipe, 'models/randomforest.joblib')
