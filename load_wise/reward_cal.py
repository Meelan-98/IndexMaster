import random
import math

def get_reward(index_choices):
    print("came here")
    timespent = random.randint(5, 10)
    return(math.log(timespent, math.e))
