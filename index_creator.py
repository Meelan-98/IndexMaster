import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from random import randint
import random

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['PeopleCatalog']

collection.create_index("name")
collection.create_index([("job_title", 1), ("company", 1)])
collection.create_index([("address", "text")])

client.close()