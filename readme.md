
<p>
<img src="images/CardFraud.jpg" width="600">
<p>

# Fraud Case Study

Deploying flask-
    Got AWS Instance created, 
    Docker image built 
        - having truoble with dockerfile and getting app to run through docker/AWS, 
        - example file doesn't seem to work, keeps timing out, don't understand register URL

postgres/mongo to pull in examples from webserver, make predictions from model off of that, store results in that DB,

Readme

which can be accessed by flask


#use link to get new data points?
#   Web scrape instead of using data included in repo?

#Take first hour, look at data, which columns are useful/dropped


# Sam - columns approx payout date to gts
# Jacob - columns has_analytics to payout type
# Joe - previous payouts to end
    
# {'classifier__n_estimators': 368, 'classifier__min_samples_split': 2, 'classifier__min_samples_leaf': 1, 'classifier__max_features': 'sqrt', 'classifier__max_depth': None, 'classifier__bootstrap': False}
# len(df['previous_payouts'][1]) == 0
# no previous payouts, suspicious

# user age = 0 or <100
#some outliers with 800+

# user type
# 70% fraud events user type =1
# 25% all events user type =1


{'classifier__n_estimators': 368, 'classifier__min_samples_split': 2, 'classifier__min_samples_leaf': 1,
    'classifier__max_features': 'sqrt', 'classifier__max_depth': None, 'classifier__bootstrap': False}

#TODO
    #DATABASE
        '''
        Set up a Postgres or MongoDB database that will store each example that the script runs on. 
        You should create a database schema that reflects the form of the raw example data and add a 
        column for the predicted probability of fraud.

        predict.py 
            loads model, loads example(example.json), runs example through feature engineering pipeline,
            adds columns from original training data to match the structure,gets probability of fraud,
            makes prediction based on a specified threshold
        
        for each example calculate the probability of fraud and add to database along with event info
        
        '''
    #WEB APP
    '''
        Hello world flask app tutorial?
        
        Set up a route POST /score and have it execute the logic in your prediction script. 
        You should import the script as a module and call functions defined therein. (predict.py)
    There are two things we'll do to make this all more efficient:

We only want to unpickle the model once
We only want to connect to the database once.
    '''

Sources:
https://www.veridiancu.org/news/advice/fraud-101-credit-debit-security