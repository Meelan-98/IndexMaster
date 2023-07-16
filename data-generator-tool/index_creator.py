import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from random import randint
import random

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['TestCatalog']

collection.create_index("phone_number")
collection.create_index("email")
collection.create_index([("first_name", 1), ("last_name", 1)])
collection.create_index([("job_title", 1), ("company", 1)])
collection.create_index([("title", 1), ("first_name", 1)])

client.close()