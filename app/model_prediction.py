# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 22:18:07 2022

@author: Sachin Pawar
"""

# Import Packages required
import pickle
import pandas as pd
import numpy as np
import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pathlib import Path
import sqlite3 as db

def classify_genres():
    # load the models and objects from disk
    filename = '/app/objects/finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    filename2 = '/app/objects/ord_encoder.obj'
    loaded_enc = pickle.load(open(filename2, 'rb'))
    filename3 = '/app/objects/scaler.obj'
    loaded_scaler = pickle.load(open(filename3, 'rb'))

    # Load the Test data
    test_data = pd.read_csv('/app/input_data/test.csv')
    test_data_org = test_data
    #Reload initial columns to use on deploy dataset
    initial_column_df = pd.read_csv('/app/objects/model_columns.csv')

    vds = SentimentIntensityAnalyzer()
    # Get the Sentiment Score for test data
    test_data['tags_sentiment_score'] = test_data['tags'].apply(lambda x: vds.polarity_scores(str(x)).get('compound'))
    columns1 = initial_column_df['Features']

    # Preprocessing the test data similar to features data of training
    cols = ["time_signature", "key", "mode"]
    test_data[cols]=test_data[cols].fillna(test_data.mode().iloc[0])
    test_data['mode'] = test_data['mode'].astype('int64')
    test_data['time_signature'] = test_data['time_signature'].astype('int64')
    test_data['key'] = test_data['key'].astype('int64')
    test_data = test_data.drop(columns=['tags'])
    test_data2 = test_data.drop(columns=['title'])
    test_data3 = pd.DataFrame(test_data2, columns=columns1)
    test_data3 = test_data3.drop(columns=['genre_code'])
    #test_data['genre_code'] = test_data['genre_code'].astype('int64')
    test_data3.fillna(test_data3.median(), inplace=True)

    # Get the Numeric Variables and scale the same
    numeric_df_test = test_data3.drop(columns=['trackID', 'time_signature','key', 'mode'])
    # transform data
    scaled_test = loaded_scaler.fit_transform(numeric_df_test)
    scaled_df_test = pd.DataFrame(scaled_test, columns=numeric_df_test.columns)

    # Apply One Hot encoding to categorical variables of test data
    cat_df_test = test_data3[['time_signature','key','mode']]
    cat_df_test['mode'] = cat_df_test['mode'].astype('category')
    cat_df_test['key'] = cat_df_test['key'].astype('category')
    cat_df_test['time_signature'] = cat_df_test['time_signature'].astype('category')
    cat_df_test = pd.get_dummies(data=cat_df_test, columns=['time_signature', 'key', 'mode'])

    # Combine the numeric and categorical variables of test data
    combined_data_test = pd.concat([test_data3[['trackID']], scaled_df_test, cat_df_test], axis=1)
    test_data_org['genre_code'] = loaded_model.predict(combined_data_test)

    # Convert Genre Code into Genre from encoding
    test_data_org["genre"] = loaded_enc.inverse_transform(test_data_org[["genre_code"]])

    # Remove Genre Code and save the result in CSV file
    test_data_org = test_data_org.drop(columns=['genre_code'])
    #test_data_org.head()
    test_data_org.to_csv('/app/output_data/test_with_labels.csv',index=False)

    test_results = test_data_org[['trackID','title','genre']]
    test_results = test_results.rename(str.lower, axis='columns')
    
    return test_results


# Create your connection.
#db_conn = db.connect('pythonsqlite.db')
#test_results.to_sql(name='results', con=db_conn)
