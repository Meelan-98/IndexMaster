import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import csv
import time

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['DatasetCatalog']

def test_workload_base(load_name,export_name):

    test_result = [["Query","Execution Time (ms)","Index Used"]]

    load_path = load_name

    with open(load_path) as file:
        queries = json.load(file)


    print("Running : ",len(queries), "Find queries")
    for index in range(0,len(queries)):
        
        query = queries[index]

        try:
            start_time = time.time()

            query_result = collection.find(query)

            end_time = time.time()

            elapsed_time = round((end_time - start_time)*1000000)

            # stats = query_result.explain()["executionStats"]

            keys_string = ', '.join([key for key in query])
            test_result.append([keys_string,elapsed_time])#,stats["executionStages"]["inputStage"]["indexName"]])

        except Exception as e:
            print(query)
            print("Exception occurred:", str(e))

    path_to_export = "workloads/results/base_" + export_name + ".csv"
    export_to_csv(test_result,path_to_export)
    


def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)


work_load_path = "workloads/train_workload_0.json"
test_workload_base(work_load_path,"train_workload_0")


