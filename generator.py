import random # define the random module  
from random import randrange
import string    

def get_a_name() -> str:
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
    return ran  