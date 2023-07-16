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

def get_reward(workload_path, tot_queries, rem_queries, index_choice):

    with open(workload_path, 'r') as json_file:
        data = json.load(json_file)

    query_index = tot_queries-rem_queries

    query = data[query_index]

    if (index_choice==0):
        index_name = "passport_number_1"
    elif (index_choice==1):
        index_name = "email_1"
    elif (index_choice==2):
        index_name = "first_name_1_last_name_1"
    elif (index_choice==3):
        index_name = "job_title_1_company_1"
    elif (index_choice==4):
        index_name = "first_name_1"
    elif (index_choice==5):
        index_name = "last_name_1"
    elif (index_choice==6):
        index_name = "job_title_1"
    elif (index_choice==7):
        index_name = "company_1"
    elif (index_choice==8):
        index_name = "title_1"
    else:
        print("came here")
        return(math.exp(-100))
    
    start_time = time.time()

    query_result = collection.find(query).hint(index_name)

    end_time = time.time()

    elapsed_time = round((end_time - start_time)*1000000)

    return([elapsed_time,math.exp(-elapsed_time)])
    

