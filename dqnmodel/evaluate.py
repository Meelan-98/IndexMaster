import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random
import torch
from dqn import DQN, Agent
import json 

uri = "mongodb+srv://IMaster:Password@indexmaster.epnwmxt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['IndexMaster']
collection = db['DatasetCatalog']

with open('train_workload_1.json', 'r') as json_file:
    query_attributes_list = json.load(json_file)

training_dataset = []


state_dim = 5  # Dimension of the state/query
action_dim = 5  # Number of possible actions
    # Load the saved model architecture
model = DQN(state_dim, action_dim)
    # Load the model's state dictionary
model.load_state_dict(torch.load('trained_model.pth'))

model.eval()

state_dim = 5 # Dimension of the state/query
action_dim = 5  # Number of possible actions
learning_rate = 0.005
discount_factor = 0.95
    # Initialize the agent
agent = Agent(state_dim, action_dim, learning_rate, discount_factor)

for i in range(len(query_attributes_list)):

    query_attributes = query_attributes_list[i]
    
    try : 
        next_state = query_attributes_list[i+1]
    except IndexError:
        next_state = query_attributes_list[0]
    #query_list = [str(value) for value in query.values()]
    #query_list = [hash(value) % state_dim for value in query_list]
    mongodb_selected_index = random.choice(['passport_number_1', 'email_1', 'first_name_1_last_name_1','address_text','job_title_1_company_1'])
    model_selected_index = agent.select_action(query_attributes,mongodb_selected_index)

    query_result = collection.find(query_attributes).hint(mongodb_selected_index)

    performance_metric = query_result.explain()["executionStats"]["executionTimeMillis"]
    
    query_result = collection.find(query_attributes).hint(model_selected_index)

    performance_metric2 = query_result.explain()["executionStats"]["executionTimeMillis"]

    sample = {
        'state': query_attributes,
        'action - MongoDB auto': mongodb_selected_index,
        'action - Model' : model_selected_index,
        'reward - MongoDB auto': performance_metric,
        'reward - Model': performance_metric2,
    }
    
    training_dataset.append(sample)

    print(i,"done")

with open('evaluation.json', 'w') as json_file:
    json.dump(training_dataset, json_file, indent=4)

client.close()
