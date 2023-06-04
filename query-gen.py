import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from random import randint
import random

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['PeopleCatalog']

# Generate 500 complex read queries
queries = []
for i in range(500):
    random_query_type = randint(1, 3)

    num_documents = collection.count_documents({})
    random_index = random.randint(0, num_documents - 1)
    random_document = collection.find().limit(1).skip(random_index)[0]
    
    if random_query_type == 1:
        query_name = random_document['name']
        query_job_title = random_document['job_title']
        query = {'name': query_name, 'job_title': query_job_title}
    elif random_query_type == 2:
        query_address = random_document['address']
        query_company = random_document['company']
        query = {'address': query_address, 'company': query_company}
    else:
        query_name = random_document['name']
        query_job_title = random_document['job_title']
        query_company = random_document['company']
        query = {'name': query_name, 'job_title': query_job_title, 'company': query_company}
    
    queries.append(query)
    print(i,"done")

# Save queries to JSON file
with open('queries.json', 'w') as json_file:
    json.dump(queries, json_file, indent=4)

# Close the MongoDB connection
client.close()

# import json

# def remove_duplicates(json_file):
#     with open(json_file, 'r') as file:
#         data = json.load(file)

#     unique_data = []
#     removed_duplicates = 0

#     for item in data:
#         if item not in unique_data:
#             unique_data.append(item)
#         else:
#             removed_duplicates += 1

#     with open('duplicate_removed.json', 'w') as file:
#         json.dump(unique_data, file, indent=4)

#     print(f"Number of removed duplicates: {removed_duplicates}")

# # Usage
# remove_duplicates('queries.json')
