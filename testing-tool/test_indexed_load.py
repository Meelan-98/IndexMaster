import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import csv
import time

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['TestCatalog']

def get_query_time(load_name,index_path,export_name):

    with open(load_name) as file:
        queries = json.load(file)

    indexes = []
    with open(index_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            indexes.append(row)

    if (len(queries) + 1) != len(indexes):
        print("Unmatched data")
        return
    
    for i in range(0,len(queries)):

        query = queries[i]
        index = indexes[i+1][2]
        
        start_time = time.time()

        query_result = collection.find(query).hint(index)

        end_time = time.time()

        elapsed_time = round((end_time - start_time)*1000000)

        indexes[i+1][1] = elapsed_time
    
    path_to_export = "workloads/results/augmented_" + export_name + ".csv"
    export_to_csv(indexes,path_to_export)
    

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

w_type = "test_workload_1"

work_load_path = "workloads/" + w_type +".json"
index_path = "workloads/results/base_" + w_type + ".csv"
get_query_time(work_load_path,index_path,w_type)

