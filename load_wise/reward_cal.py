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
import asyncio

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['DatasetCatalog']

def get_reward(index_choice):

    with open('workloads/test_workload_1.json') as file:
        queries = json.load(file)

    if (index_choice==0):
        index_name = "passport_number_1"
    elif (index_choice==1):
        index_name = "email_1"
    elif (index_choice==2):
        index_name = "first_name_1_last_name_1"
    else:
        print("came here")
        return(math.exp(-100))
    
    start_time = time.time()

    for query in queries:
        query_result = collection.find(query).hint(index_name)

    end_time = time.time()

    elapsed_time = (end_time - start_time)*1000

    return(math.exp(-elapsed_time))
    

