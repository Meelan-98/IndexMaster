from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random
from datetime import datetime

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['TestCatalog']

unique_values = collection.distinct('first_name')
query_result = collection.find({'first_name': 'Andrew'})

name_list = ['Andrew', 'Jay', 'Brittany', 'Margaret', 'Nathan', 'Daniel', 'Gabrielle', 'Matthew', 'Amber', 'Joseph']

for i in range(10):
    query = { 'first_name': name_list[i], "last_name": 'Rosales'}
    mongodb_selected_index = random.choice(['passport_number_1', 'email_1', 'first_name_1_last_name_1','address_text','job_title_1_company_1'])
    query_result = collection.find(query)
    time1  = datetime.now() 
    time1ms = int(time1.timestamp() * 1000)
    performance_metric = query_result.explain()["executionStats"]["executionTimeMillis"]
    time2  = datetime.now() 
    time2ms = int(time2.timestamp() * 1000)

    count = 0
    for document in query_result:
        count += 1
    print("time calculated", (time2ms - time1ms))
    print("performance metric", performance_metric)
