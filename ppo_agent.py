import gym
from stable_baselines3 import PPO
from gym import spaces
import numpy as np
import csv
from load_wise.environment import initial_state_function,state_change
from load_wise.reward_cal import get_reward


def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

class MongoDBIndexSelectionEnv(gym.Env):
    def __init__(self, initial_state_fn, reward_fn, state_change_fn, w_path):

        self.action_space = spaces.Discrete(3) 
        self.observation_space = spaces.MultiBinary(10)

        self.workload_path = w_path
        self.rem_queries = 0
        self.tot_queries = 0
        
        self.initial_state_fn = initial_state_fn
        self.reward_fn = reward_fn
        self.state_change_fn = state_change_fn
        
        self.state = None
        self.reset()
        
    def reset(self):
        
        state_data = self.initial_state_fn(self.workload_path)
        self.state = state_data[0]
        self.rem_queries = state_data[1]
        self.tot_queries = state_data[1]

        return np.array(self.state)
    
    def step(self, action):

        rewards = self.reward_fn(self.workload_path,self.tot_queries,self.rem_queries,action)

        reward = rewards[1]

        self.rem_queries = self.rem_queries - 1

        done = False

        if self.rem_queries == 0:
            done = True
        else:
            self.state = self.state_change_fn(self.workload_path,self.tot_queries,self.rem_queries)  # Change the state
        
        return np.array(self.state), reward, done, {"time" : rewards[0]}

workload = "train_workload_0"
workload_path = "workloads/" + workload + ".json"

env = MongoDBIndexSelectionEnv(initial_state_function, get_reward, state_change, workload_path)

model = PPO("MlpPolicy", env, verbose=2)
model.learn(total_timesteps=1000)

obs = env.reset()
done = False

results = []
count = 1

while not done:
    result = [count]
    action, _ = model.predict(obs)
    obs, reward, done, metadata = env.step(action)
    results.append([count,metadata["time"],action])
    count = count + 1

path_to_export = "workloads/results/reinforced_" + workload + ".csv"
export_to_csv(results,path_to_export)


