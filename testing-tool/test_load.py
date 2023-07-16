import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import csv
import time

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['TestCatalog']

def test_query_time(load_name):

    test_result = [["Query","Execution Time (ms)","Index Used"]]

    with open(load_name) as file:
        queries = json.load(file)

    print("Running : ",len(queries), "Find queries")

    for index in range(0,len(queries)):
        
        query = queries[index]

        try:
            start_time = time.time()

            query_result = collection.find(query)

            end_time = time.time()

            elapsed_time = round((end_time - start_time)*1000000)

            keys_string = ', '.join([key for key in query])
            test_result.append([keys_string,elapsed_time])

        except Exception as e:
            print(query)
            print("Exception occurred:", str(e))
        
    return(test_result)


def test_index_name(work_load_path,export_name):

    test_result = test_query_time(work_load_path)

    with open(work_load_path) as file:
        queries = json.load(file)

    print("Finding Index names")

    for index in range(0,len(queries)):
        
        query = queries[index]

        try:
            query_result = collection.find(query)
            stats = query_result.explain()["executionStats"]

            test_result[index+1].append(stats["executionStages"]["inputStage"]["indexName"])

        except Exception as e:
            print(query)
            print("Exception occurred:", str(e))

    path_to_export = "workloads/results/base_" + export_name + ".csv"
    export_to_csv(test_result,path_to_export)
    

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)


work_load_path = "workloads/train_workload.json"
test_index_name(work_load_path,"train_workload")
