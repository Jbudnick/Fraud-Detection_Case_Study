#Try to get to a model today
    #
#dedicate one person to start flask app
#Divide and Conquer

#use link to get new data points?
#   Web scrape instead of using data included in repo?

#Take first hour, look at data, which columns are useful/dropped


# Sam - columns approx payout date to gts
# Jacob - columns has_analytics to payout type
# Joe - previous payouts to end
    

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
    