import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from random import randint
import random

def query_type1(random_document):
    query_passport = random_document['passport_number']
    query_last_name = random_document['last_name']
    query = {'passport_number': query_passport, 'last_name': query_last_name}
    return query

def query_type2(random_document):
    query_email = random_document['email']
    query_phone_number = random_document['phone_number']
    query = {'email': query_email, 'phone_number': query_phone_number}
    return query

def query_type3(random_document):
    query_title = random_document['title']
    query_first_name = random_document['first_name']
    query_last_name = random_document['last_name']
    query_suffix = random_document['suffix']
    query = {'title': query_title, 'first_name': query_first_name, 'last_name': query_last_name, 'suffix' : query_suffix}
    return query

def query_type4(random_document):
    query_address = random_document['address']
    query_company = random_document['company']
    query = {'address': query_address, 'company': query_company}
    return query

def query_type5(random_document):
    query_first_name = random_document['first_name']
    query_job_title = random_document['job_title']
    query_company = random_document['company']
    query = {'first_name': query_first_name, 'job_title': query_job_title, 'company': query_company}
    return query

def query_type6(random_document):
    query_passport = random_document['passport_number']
    query_phone_number = random_document['phone_number']
    query = {'passport_number': query_passport, 'phone_number': query_phone_number}
    return query

def query_type7(random_document):
    query_email = random_document['email']
    query_last_name = random_document['last_name']
    query_phone_number = random_document['phone_number']
    query = {'email': query_email, 'last_name': query_last_name, 'phone_number': query_phone_number}
    return query

def query_type8(random_document):
    query_job_title = random_document['job_title']
    query_first_name = random_document['first_name']
    query_last_name = random_document['last_name']
    query = {'first_name': query_first_name, 'last_name': query_last_name, 'job_title': query_job_title}

def query_type9(random_document):
    query_address = random_document['address']
    query_phone_number = random_document['phone_number']
    query = {'address': query_address, 'phone_number': query_phone_number}
    return query

def query_type10(random_document):
    query_last_name = random_document['last_name']
    query_job_title = random_document['job_title']
    query_company = random_document['company']
    query_title = random_document['title']
    query = {'job_title': query_job_title, 'company': query_company, 'title': query_title, 'last_name': query_last_name}
    return query

def writeToFile(filename, queries):
    # Save queries to JSON file
    file_path = "workloads/" + filename + ".json"
    with open(file_path, 'w') as json_file:
        json.dump(queries, json_file, indent=4)

def writeToConfigFile(filename, data):
    # Open the file in write mode
    file_path = "workloads/" + filename + ".txt"
    with open(file_path, "a") as file:
        # Write the data to the file
        file.write(data + "\n")

def generate_queries(query_count, r, collection):
    queries = []
    if(sum(r) != query_count):
        print("Invalid Query Counts")
        return
    for i in range(query_count):
        num_documents = collection.count_documents({})
        random_index = random.randint(0, num_documents - 1)
        random_document = collection.find().limit(1).skip(random_index)[0]
        
        if i in range(0, r[0]):
            query = query_type1( random_document)
        elif i in range(r[0], r[0]+r[1] ):
            query = query_type2( random_document)
        elif i in range(r[0]+r[1], r[0]+r[1]+r[2]):
            query = query_type3( random_document)
        elif i in range(r[0]+r[1]+r[2], r[0]+r[1]+r[2]+r[3]):
            query = query_type4( random_document)
        else:
            query = query_type5( random_document)

        queries.append(query)
        print(i,"done")
    print(queries)
    return queries

def main():
    uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client['IndexMaster']
    collection = db['DatasetCatalog']

    # Update These
    query_count = 10
    r = [2 ,2 ,2, 2, 2]
    filename="workload"

    queries = generate_queries(query_count, r, collection)
    
    writeToFile(filename, queries)

    config_data = filename + " : " + str(r)
    config_filename = "workload_config"
    writeToConfigFile( config_filename, config_data)


main()