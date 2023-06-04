import random
import numpy as np
import json

# Define the Deep Q-Network (DQN) class
class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size))
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
    
    def select_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            return np.argmax(self.q_table[state])
    
    def update_q_table(self, state, action, reward, next_state):
        q_value = self.q_table[state, action]
        max_q_value = np.max(self.q_table[next_state])
        new_q_value = q_value + self.learning_rate * (reward + self.discount_factor * max_q_value - q_value)
        self.q_table[state, action] = new_q_value
    
    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Load the training dataset from a JSON file
def load_training_dataset(filename):
    with open(filename, 'r') as json_file:
        training_dataset = json.load(json_file)
    return training_dataset

# Train the DQN model on the training dataset
def train_dqn_model(training_dataset, state_size, action_size, num_episodes):
    dqn = DQN(state_size, action_size)
    
    for episode in range(num_episodes):
        total_reward = 0
        for k in range(len(training_dataset)):
            sample = training_dataset[k]
            state = sample['state']
            action = sample['action']
            reward = sample['reward']
            next_state = training_dataset[k+1]['state']  # Update with your own logic for getting the next state
            
            dqn.update_q_table(state, action, reward, next_state)
            total_reward += reward
        
        dqn.decay_epsilon()
        
        # Print the total reward for the episode
        print("Episode: {}, Total Reward: {}".format(episode + 1, total_reward))
    
    return dqn

# Test the trained DQN model on a new query
def test_dqn_model(dqn, state):
    action = dqn.select_action(state)
    return action

# Example usage
training_dataset = load_training_dataset('training_dataset.json')
state_size = len(training_dataset[0]['state'])
action_size = 3  # Assuming three indexes: name_index, job_title_index, and address_index
num_episodes = 100

dqn_model = train_dqn_model(training_dataset, state_size, action_size, num_episodes)

# # Test the trained model on a new query state
# new_query_state = [1, 2, 3, 4, 5]  # Update with your own logic for the new query state
# optimal_index = test_dqn_model(dqn_model, new_query_state)
# print("Optimal Index: {}".format(optimal_index))
