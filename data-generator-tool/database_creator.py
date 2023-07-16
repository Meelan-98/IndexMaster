from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker
import random

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['TestCatalog']

fake = Faker()
fake.seed(0)
# Define the number of documents to generate
num_documents = 10000
num_of_elements = [5000, 6000, 5, 8000, 10000, 50, 1000, 10000 ]
names_of_elements = ["first_name", "last_name", "prefix", "address", "phone_number", "job_title", "company", "email"]

first_name = []
last_name = []
prefix = []
address = []
phone_number = []
job = []
company = []
email = []

for i in range(8):
    for j in range(num_of_elements[i]):
        if i == 0:
            first_name.append(fake.first_name())
        elif i == 1:
            last_name.append(fake.last_name())
        elif i == 2:
            prefix.append(fake.prefix())
        elif i == 3:
            address.append(fake.address())
        elif i == 4:
            phone_number.append(fake.phone_number())
        elif i == 5:
            job.append(fake.job())
        elif i == 6:
            company.append(fake.company())
        elif i == 7:
            email.append(fake.email())

print(len(first_name))
print(len(last_name))
print(len(prefix))

for i in range(num_documents):
    print(i)
    document = {
        'first_name': random.choice(first_name),
        'last_name': random.choice(last_name),
        'title': random.choice(prefix),
        'address': random.choice(address),
        'phone_number': random.choice(phone_number),
        'job_title': random.choice(job),
        'company': random.choice(company),
        'email': random.choice(email)
    }
    if(i%1000==0):
        print("collection inserted")
        print(document)
    collection.insert_one(document)
     

# Close the MongoDB connection
client.close()