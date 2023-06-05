import torch
import torch.nn as nn
import torch.optim as optim
import json

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=64):
        super(DQN, self).__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Embedding layer for the state/query
        self.embedding_layer = nn.EmbeddingBag(state_dim, hidden_dim, sparse=True)
        self.fc = nn.Linear(hidden_dim, action_dim)

    def forward(self, state):
        embedded_state = self.embedding_layer(state)
        output = self.fc(embedded_state)
        return output


class Agent:
    def __init__(self, state_dim, action_dim, learning_rate, discount_factor):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.model = DQN(state_dim, action_dim)
        self.optimizer = optim.Adagrad(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()
        self.action_to_index = {"name_1":"0","address_text":"1","job_title_1_company_1":"2"}  # Dictionary to map action string to index
        self.index_to_action = {"0":"name_1","1":"address_text","2":"job_title_1_company_1"}  # Dictionary to map index to action string

    def preprocess_state(self, state):
        state_tensor = torch.LongTensor([hash(str(value)) % self.state_dim for value in state])
        #state_tensor = torch.LongTensor([hash(str(value)) % self.state_dim for value in state])

        return state_tensor.unsqueeze(0)

    def update_q_table(self, state, action, reward, next_state):
        state_tensor = self.preprocess_state(state)
        next_state_tensor = self.preprocess_state(next_state)

        q_values = self.model(state_tensor)
        action_index = self.action_to_index[action]  # Convert action string to index
        q_value = q_values[0][action_index]

        next_q_values = self.model(next_state_tensor)
        max_q_value, _ = torch.max(next_q_values, dim=1)

        target_q_value = reward + self.discount_factor * max_q_value

        loss = self.criterion(q_value.unsqueeze(0), target_q_value)  # Ensure the same shape

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def select_action(self, state,action):
        state_tensor = self.preprocess_state(state)
        q_values = self.model(state_tensor)
        _, action_index = torch.max(q_values, dim=1)
        #print(action_index.item())
        #print(self.index_to_action)
        action = self.index_to_action[str(action_index.item())]  # Convert index to action string
        return action


# Load rewards from JSON file
def load_rewards_from_file(filename):
    with open(filename, 'r') as file:
        rewards = json.load(file)
    return rewards

def load_queries_from_file(filename):
    with open(filename, 'r') as file:
        queries = json.load(file)
    return queries

# Example usage
state_dim = 4  # Dimension of the state/query
action_dim = 3  # Number of possible actions
learning_rate = 0.001
discount_factor = 0.9

# Initialize the agent
agent = Agent(state_dim, action_dim, learning_rate, discount_factor)

# Load rewards from file
rewards = load_rewards_from_file('training_dataset.json')
queries_set = load_queries_from_file('queries.json')
for i, reward in enumerate(rewards):
    action = reward['action']
    if action not in agent.action_to_index:
        index = len(agent.action_to_index)
        agent.action_to_index[action] = index
        agent.index_to_action[index] = action

torch.manual_seed(42)

    # Load the trained model
model = DQN(state_dim, action_dim)
model.load_state_dict(torch.load('trained_model.pth'))

    # Set model in evaluation mode
model.eval()

    # Create the agent for prediction
agent.model = model


# Train the agent using the rewards
for i in range(len(rewards)):

    state = rewards[i]['state']
    action = rewards[i]['action']
    reward_value = rewards[i]['reward']
    try :
        index_state = queries_set.index(state)
        next_state = queries_set[index_state+1]
    except IndexError:
        pass
    torch.save(agent.model.state_dict(), 'trained_model.pth')
# Get user input for query/state


# Select the best action based on the query/state

# j = input("Enter Query number : ")
# query = queries_set[int(j)]
# next_state = queries_set[int(j)+1]
# action = input("Enter the action you prefer: ")
# query_list = [str(value) for value in query.values()]
# query_list = [hash(value) % state_dim for value in query_list]
# best_action = agent.select_action(query_list)
# if action == best_action :
#     print("Yes, That is the best action for the Query")
# else:
#     print("No, The best action for the query is", best_action)
