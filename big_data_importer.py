import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['big_data_journals']
collection = db['big_data_journals']


with open('scraped_data.json') as file:
    file_data = json.load(file)

collection.insert_many(file_data)

client.close()