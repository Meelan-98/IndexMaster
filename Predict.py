import torch
from dqn import DQN, Agent
import json 

if __name__ == "__main__":
    state_dim = 4  # Dimension of the state/query
    action_dim = 3  # Number of possible actions

    # Load the saved model architecture
    model = DQN(state_dim, action_dim)

    # Load the model's state dictionary
    model.load_state_dict(torch.load('trained_model.pth'))

    state_dim = 4  # Dimension of the state/query
    action_dim = 3  # Number of possible actions
    learning_rate = 0.001
    discount_factor = 0.9

    # Initialize the agent
    agent = Agent(state_dim, action_dim, learning_rate, discount_factor)
    j = input("Enter Query number : ")
    with open('queries.json', 'r') as file:
        queries_set = json.load(file)
    query = queries_set[int(j)]
    next_state = queries_set[int(j)+1]
    action = input("Enter the action you prefer: ")
    query_list = [str(value) for value in query.values()]
    query_list = [hash(value) % state_dim for value in query_list]

    best_action = agent.select_action(query_list,action)
    if action == best_action :
        print("Yes, That is the best action for the Query")
    else:
        print("No, The best action for the query is", best_action)
