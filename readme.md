
<p>
<img src="images/CardFraud.jpg" width="600">
<p>

# Fraud Case Study
As the world is getting more dependent on electronic forms of payment, unfortunately the rate of fraudulent charges are increasing as well. Fraudulent charges cost money and time and result in frustration for both the company and the consumer. With a model our team built, we are able to predict whether an incoming charge will be fraudulent or not based on many factors, so we can prevent the posting of a fraudulent event before people purchase tickets.

## Data and Cleaning

<p>
<img src="images/barsfraudvsnotfraud.png" width="600">
<p>

The following fields were dropped due to little correlation with fraud:
* venue_state
* venue_name
* has_header
* venue_latitude (refeaturized)
* venue_longitude
* venue_address*
* name_length*
* name
* object_id
* listed
* user_created
* num_payouts*
* org_desc*
* ticket_types*

\* Asterisk indicates feature may be reconsidered in the future

The following fields were dropped due to concerns they may be unavailable at time of prediction:
* gts
* approx_payout_date
* num_order
* sale_duration
* sale_duration2

Feature Engineering:
* user_age - Converted to binary : 0 or not 
* event_end, event_start - Changed into event length
* email_domain - Extracted as country code : One-hot encoded
* org_name - Converted to binary : Whether it had an organization name listed or not
* payee_name - Converted to binary : Exists or not
* user_type - Converted to binary : whether 1 or not (highly correlated with fraud)
* venue_country, country - Converted to binary : Do they match?
* org_twitter- Converted to binary : 0 or not
* org_facebook - Converted to binary : 0 or not
* previous_payouts - Converted to binary : empty list or not
* payout_type  - One hot encoded : CHECK, ACH, None
* venue_latitude - Converted to binary : whether lat/long coordinates were listed and non-zero
* description - TFIDF matrix

## Results

### Model

We initially started with a random forest model because we expected it to be a solid baseline. Given the time constraints we wanted something that we could get up and running quickly. The initial results were promising so we used RandomizedSearchCV to find more optimal hyperparameters.

Random Forest HyperParameters:
* n_estimators': 368
* min_samples_split': 2

These parameters resulted in an AUC of `0.983`.

<p>
<img src="images/rf_roc.png" width="600">
<p>

### Performance Metrics
We tuned and evaluated our model with the assumption that when we predict an event as fraud, there is a system in place to reach out to the event organizer via email and ask them to provide more information about their event.

This assumption implies it is a relatively low-cost to incorrectly flag an event as fraudulent. For this reason, we chose to evaluate our model with **recall**, airing on the side of predicting fraud.

With this assumption in mind, we ended up choosing a prediction threshold of **0.15**, meaning if we predicted a probability of fraud greater than or equal to 0.15, we classified it as fraud.

|            	| Precision 	| Recall 	| F-1   	|
|------------	|-----------	|--------	|-------	|
| Fraud      	| 0.766     	| 0.923  	| 0.837 	|
| Not-Fraud  	| 0.992     	| 0.972  	| 0.982 	|
| Macro Avg. 	| 0.879     	| 0.947  	| 0.909 	|

Accuracy: `0.967`

### Confusion Matrix
|                  	| pred:fraud 	| pred:not_fraud 	|
|------------------	|------------	|----------------	|
| actual:fraud     	| 298        	| 25             	|
| actual:not_fraud 	| 91        	| 3171           	|

Out of 323 actual fraud cases in our test set, we correctly identified 298 of them.

Out of 3,262 actual non-fraud cases, we incorrectly identified 91 of them as fraud.


[Our
Feature |  Importance |
| ----------- | ----------- |
|previous_payouts |     0.110899|
|category__x2_    |     0.036462
|num_order         |    0.032699
|user              |    0.018988
|has_org_name      |   0.017127
|suspicious_age    |    0.015334
|event_length  |        0.013162
|body_length    |       0.010333
|channels       |      0.009721
|match_country   |      0.009071
|category__x2_ACH  |    0.008448
|has_coords         |   0.006938
|org_facebook       |   0.0|06457
|has_payee_name     |  0.006033
|category__x2_CHECK    |0.006008


[Our App](http://ec2-3-21-232-66.us-east-2.compute.amazonaws.com:8080/)
ources:
https://www.veridiancu.org/news/advice/fraud-101-credit-debit-security