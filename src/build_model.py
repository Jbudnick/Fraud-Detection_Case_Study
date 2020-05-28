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

from imblearn.over_sampling import SMOTE

from feature_engineering import clean_pipeline

def roc():
    # Plot the ROC
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
    plt.show()

def random_search(X_train,y_train):
    
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


if __name__ == "__main__":

    one_hot_cols = [
        "domain_country_code",
        "delivery_method",
        "payout_type",
        "currency"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(), 'description'),
            ('category', OneHotEncoder(handle_unknown='ignore'), one_hot_cols),
        ],
    )
    pipe = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100)),
        ],
    )
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 1000, num = 20)]
    max_features = ['auto', 'sqrt']
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    min_samples_split = [2, 5, 10]
    min_samples_leaf = [1, 2, 4]
    bootstrap = [True, False]

    random_grid = {'classifier__n_estimators': n_estimators,
                'classifier__max_features': max_features,
                'classifier__max_depth': max_depth,
                'classifier__min_samples_split': min_samples_split,
                'classifier__min_samples_leaf': min_samples_leaf,
                'classifier__bootstrap': bootstrap}
    rf_random = RandomizedSearchCV(pipe, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
  
    total_df = pd.read_json('data/data.json')
    clean_df = clean_pipeline(total_df)
    X = clean_df.drop(["target"], axis=1)
    y = clean_df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)
    # X_pre_sample_train, X_test, y_pre_sample_train, y_test = train_test_split(X, y)
    # X_train, y_train = SMOTE().fit_resample(X_pre_sample_train,y_pre_sample_train)
    
    rf_random.fit(X_train, y_train)
    print(rf_random.best_params_)

    pipe.fit(X_train, y_train)
    
    probs = pipe.predict_proba(X_test)[:, 1]

    theshold = 0.2

    y_hat = (probs >= theshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_test, y_hat).ravel()

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

    # pipe.fit(X, y)
    # train_columns = list(X.columns)
    # with open('models/column_list.pkl', 'wb') as f:
    #     pickle.dump(train_columns, f)
    # dump(pipe, 'models/randomforest.joblib')