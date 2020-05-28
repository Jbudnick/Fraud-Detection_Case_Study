


    # has_analytics 
    # 100% of fraud events has_analyics = 0
    # 90% of events has_analytics =0
   
    
    # has_logo
    # 30% of fraud events has_logo =0
    # 15% of all events has_logo =0   

    # name
    # NLP?

import re
import pandas as pd
from bs4 import BeautifulSoup
import pickle
import numpy as np


def is_fraud(string):
    if re.match("fraud", string):
        return 1
    else:
        return 0


def remove_html_tags(html_string):
    soup = BeautifulSoup(html_string, features="lxml")
    return soup.get_text()


def get_domain_country_code(domain):
    return re.sub(r"^[^\.]+?(\..+$)", r"\1", domain)


def prev_payout_bool(prev_payout_list):
    if len(prev_payout_list) == 0:
        return 0
    else:
        return 1


def suspicious_age(age):
    if age == 0 or age == None:
        return 1
    else:
        return 0


def org_booleans(org_int):
    if org_int == 0:
        return 1
    else:
        return 0

def user_type(user):
    if user == 1:
        return 1
    else:
        return 0

def has_delivery_method(delivery_method):
    if delivery_method == np.nan or delivery_method == 0 or delivery_method == None:
        return 0
    else:
        return 1

def has_org_name(org_name):
    if org_name == np.nan or org_name == None or org_name == "":
        return 0
    else:
        return 1


def drop_cols(df, list_of_cols):
    return df.drop(labels=list_of_cols)


def clean_pipeline(original_df):
    df = original_df.copy()
    if 'acct_type' in df.columns:
        df['target'] = df['acct_type'].apply(is_fraud)
    df['description'] = df['description'].apply(remove_html_tags)
    df['domain_country_code'] = df['email_domain'].apply(get_domain_country_code)
    df['previous_payouts'] = df['previous_payouts'].apply(prev_payout_bool)
    df['suspicious_age'] = df['user_age'].apply(suspicious_age)
    df['org_twitter'] = df['org_twitter'].apply(org_booleans)
    df['org_facebook'] = df['org_facebook'].apply(org_booleans)
    df['delivery_method'] = df['delivery_method'].astype(str)
    df['has_org_name'] = df['org_name'].apply(has_org_name)
    df['has_payee_name'] = df['payee_name'].apply(has_org_name)

    df['venue_latitude'] = df['venue_latitude'].fillna(0)
    df['has_coords'] = (df['venue_latitude'] != 0).astype(int)

    df['match_country'] = (df['country'] == df['venue_country']).astype(int)

    df['event_length'] =  df['event_end'] - df['event_start']
    df['user'] = df['user_type'].apply(user_type)

    drop_cols = [
        "acct_type",
        "email_domain",
        "venue_state",
        "venue_name",
        "user_age",
        "has_header",
        "event_end",
        "event_start",
        "event_created",
        "event_published",
        "gts",
        "sale_duration",
        "sale_duration2",
        "venue_latitude",
        "venue_longitude",
        "object_id",
        "user_type",
        "approx_payout_date",
        "user_created",
        "listed",
        "num_payouts",

        # maybe tfidf?
        "org_desc",

        "org_name",

        "name",
        "name_length",
        "country",
        "venue_country",
        "venue_address",

        # maybe mess with this
        "ticket_types",

        "payee_name"
    ]

    df.drop(labels=drop_cols, axis=1, inplace=True, errors='ignore')

    return df

if __name__ == "__main__":
    df = pd.read_json('data/data.json')
    clean_df = clean_pipeline(df)