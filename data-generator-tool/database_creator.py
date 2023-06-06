from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['DatasetCatalog']

fake = Faker()

# Define the number of documents to generate
num_documents = 10000

# Generate and insert dummy data
for _ in range(num_documents):
    document = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'title': fake.prefix(),
        'address': fake.address(),
        'phone_number': fake.phone_number(),
        'job_title': fake.job(),
        'company': fake.company(),
        'email': fake.email(),
        'passport_number': fake.passport_number(),
        'suffix': fake.suffix()
    }
    print("collection inserted")
    collection.insert_one(document)

# Close the MongoDB connection
client.close()