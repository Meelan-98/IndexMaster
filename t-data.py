import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['DatasetCatalog']

with open('train_workload_1.json', 'r') as json_file:
    query_attributes_list = json.load(json_file)

training_dataset = []

for i in range(len(query_attributes_list)):

    query_attributes = query_attributes_list[i]
    
    selected_index = random.choice(['passport_number_1', 'email_1', 'first_name_1_last_name_1','address_text','job_title_1_company_1'])
    
    query_result = collection.find(query_attributes).hint(selected_index)

    performance_metric = query_result.explain()["executionStats"]["executionTimeMillis"]
    
    sample = {
        'state': query_attributes,
        'action': selected_index,
        'reward': performance_metric,
    }
    
    training_dataset.append(sample)

    print(i,"done")

with open('training_dataset1.json', 'w') as json_file:
    json.dump(training_dataset, json_file, indent=4)

client.close()
