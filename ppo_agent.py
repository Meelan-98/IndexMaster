import gym
from stable_baselines3 import PPO
from gym import spaces
import numpy as np
import csv
from load_wise.environment import initial_state_function,state_change, get_action
from load_wise.reward_cal import get_reward
import configparser
import time


def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

class MongoDBIndexSelectionEnv(gym.Env):
    def __init__(self, initial_state_fn, reward_fn, state_change_fn, config_file):

        self.action_space = spaces.Discrete(9) 
        self.observation_space = spaces.MultiBinary(8)

        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.workload_path = None
        self.rem_queries = 0
        self.tot_queries = 0
        
        self.initial_state_fn = initial_state_fn
        self.reward_fn = reward_fn
        self.state_change_fn = state_change_fn
        
        self.inference = False
        self.state = None
        self.reset()
        
    def reset(self):

        if (self.inference == True):
            print("Resetting to Inference")
            workload_loc = str(self.config.get("env", "test_state"))
            self.workload_path = workload_loc
        else:
            print("Resetting to Training")
            workload_loc = str(self.config.get("env", "train_state"))
            self.workload_path = workload_loc

        state_data = self.initial_state_fn(workload_loc)
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
    
    def enter_inference(self):
        self.inference = True

    def exit_inference(self):
        self.inference = False

env = MongoDBIndexSelectionEnv(initial_state_function, get_reward, state_change, "config.ini")

print("Started Learning........")
model = PPO("MlpPolicy", env, verbose=2)
model.learn(total_timesteps=10000)

print("Learning done ! Entering prediction mode")
env.enter_inference()
obs = env.reset()
done = False

results = [["Index Used","Execution Time (ms)"]]
count = 1

config = configparser.ConfigParser()
config.read("config.ini")
workload = str(config.get("env", "test_state"))
workload = (workload.split("/")[1]).split(".")[0]

print(workload)

infer_times = []

while not done:
    result = [count]

    start_time = time.time()
    action, _ = model.predict(obs)
    end_time = time.time()

    duration = (end_time - start_time)*1000000
    infer_times.append(duration)

    obs, reward, done, metadata = env.step(action)
    results.append([get_action(action),metadata["time"]])
    count = count + 1

env.exit_inference()

print(infer_times)

average = sum(infer_times) / len(infer_times)
maximum = max(infer_times)
minimum = min(infer_times)

path_to_export = "workloads/results/reinforced_" + workload + ".csv"
export_to_csv(results,path_to_export)


