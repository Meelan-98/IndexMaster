import gym
from stable_baselines3 import PPO
from gym import spaces
import numpy as np
from load_wise.vectorizer import export_load_vector,state_change
from load_wise.reward_cal import get_reward

class MongoDBIndexSelectionEnv(gym.Env):
    def __init__(self, initial_state_fn, reward_fn, state_change_fn):
        self.action_space = spaces.MultiBinary(5)  # Binary array of size 5
        self.observation_space = spaces.MultiBinary(55)  # Binary array of size 55
        
        self.initial_state_fn = initial_state_fn
        self.reward_fn = reward_fn
        self.state_change_fn = state_change_fn
        
        self.state = None
        self.reset()
        
    def reset(self):
        self.state = self.initial_state_fn('tData.json')
        return np.array(self.state)
    
    def step(self, action):

        chosen_indexes = np.where(action == 1)[0]  # Get the selected indexes
        
        binary_action = [int(bit) for bit in chosen_indexes]
        ones_count = sum(binary_action)
        
        if ones_count != 3:
            reward = -1
        else:
            reward = self.reward_fn(chosen_indexes)  # Calculate the reward
        self.state = self.state_change_fn(self.state,chosen_indexes)  # Change the state
        done = True  # Set to True if the episode is over
        
        return np.array(self.state), reward, done, {}


env = MongoDBIndexSelectionEnv(export_load_vector, get_reward, state_change)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
obs = env.reset()

done = False
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _ = env.step(action)
    print(action,reward)
