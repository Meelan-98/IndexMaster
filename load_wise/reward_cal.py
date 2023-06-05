import random
import math
import numpy as np
import json
import time
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from random import randint
import random

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['PeopleCatalog']

def get_reward(index_choices):

    with open('tData.json') as file:
        queries = json.load(file)

    if np.array_equal(index_choices, np.array([0,1,1])):
        index_name = "passport_number_1"
    elif np.array_equal(index_choices, np.array([1,0,1])):
        index_name = "email_1"
    elif np.array_equal(index_choices, np.array([1,1,0])):
        index_name = "first_name_1_last_name_1"
    else:
        print("came here")
        return(math.exp(-100))
    
    start_time = time.time()
    
    for query in queries:
        cursor = collection.find(query).hint(index_name)

    end_time = time.time()

    elapsed_time = (end_time - start_time)*1000

    print(elapsed_time)

    return(math.exp(-elapsed_time))
