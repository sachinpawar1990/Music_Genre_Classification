# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 22:44:54 2022

@author: Sachin S. Pawar
"""

from fastapi import FastAPI
import uvicorn
from databases import Database
import os
from model_prediction import classify_genres
import sqlite3 as db

app = FastAPI()
database = Database("sqlite:///./pythonsqlite.db")

#if not os.path.isfile(r'pythonsqlite.db'):
    #execfile("model_prediction.py")
    #exec(open("model_prediction.py").read())

test_results = classify_genres()
test_results_dict = test_results.to_dict('index')

@app.get('/')
def index():
    return {'message': 'This is the homepage of the API '}

@app.on_event("startup")
async def database_connect():
    await database.connect()
    
@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()

@app.get("/get_all_genres")
async def fetch_all_genres():
    query = "SELECT trackid, genre FROM results"
    results = await database.fetch_all(query=query)

    return  results

@app.get("/get_title_from_genre")
async def fetch_title_from_genre(genre: str):
    query = "SELECT title FROM results WHERE genre='{}'".format(str(genre))
    results = await database.fetch_all(query=query)

    return  results

@app.post("/upload_classified_results")
async def put_results():
    #query = "INSERT INTO results(trackid, title, genre) VALUES (:trackid, :title, :genre)"
    #await database.execute_many(query=query, values=test_results_dict)
    db_conn = db.connect('/app/pythonsqlite.db')
    test_results.to_sql(name='results', con=db_conn, if_exists='append')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)