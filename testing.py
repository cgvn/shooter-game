from random import random, randint
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class shooter:
    def __init__(self,name,probability,target_list):
        self.name = name
        self.probability = probability
        self.status = 'alive'
        self.target = -1
        self.target_list = target_list.copy()
    
    def find_self(self):
        self.index = [ti for ti,tj in enumerate(self.target_list) if tj==self.name][0]    
    
    def remove_self(self):
        self.target_list.pop(self.index)
    
    def choose_target(self):
        pass
        
    def shoot_target(self):
        self.hit = random()<self.probability

class shootUp(shooter):
    def choose_target(self):
        self.target_list.sort()
        self.find_self()
        target_indx = self.index + 1
        if target_indx==len(self.target_list):
            target_indx = self.index - 1
        self.target = self.target_list[target_indx]
        
class shootUpRound(shooter):
    def choose_target(self):
        self.target_list.sort()
        self.find_self()
        target_indx = self.index + 1
        if target_indx==len(self.target_list):
            target_indx = 0
        self.target = self.target_list[target_indx]        
        
class shootDown(shooter):
    def choose_target(self):
        self.target_list.sort()
        self.find_self()
        target_indx = self.index - 1
        if target_indx==-1:
            target_indx = len(self.target_list) - 1
        self.target = self.target_list[target_indx]    
        
class shootRandom(shooter):
    def choose_target(self):
        self.find_self()
        self.remove_self()
        target_indx = randint(0,len(self.target_list)-1)
        self.target = self.target_list[target_indx]

def find_index(target_list,name):
    return [ti for ti,tj in enumerate(target_list) if tj==name][0]

def initialize_game(num_shooters,shooter_type='up'):
    target_list = [i for i in range(1,num_shooters+1,1)]
    shooters = []
    for i,j in enumerate(target_list):
        shooters.append(shooter_types[shooter_type](j,j/num_shooters,target_list))
    return shooters

def play_round(shooters,verbose=False):
    shooter_list = [si.name for si in shooters]
    for s in shooters:
        if s.status=='dead':
            continue
        target_list = [si.name for si in shooters if si.status=='alive']
        s.target_list = target_list.copy()
        s.choose_target()
        s.shoot_target()
        if s.hit:
            target_index = find_index(shooter_list,s.target)
            shooters[target_index].status='dead'        
        if verbose:
            print("target list: {}".format(target_list))
            print("{} aimed {}. Kill is {}".format(s.name,s.target,s.hit))
    return [si.name for si in shooters if si.status=='alive']        

def play_game(shooters,verbose=False):
    round_no = 1
    target_list = [si.name for si in shooters if si.status=='alive'] 
    while len(target_list)>1:
        target_list = play_round(shooters=shooters,verbose=verbose)  
        if verbose:
            print("End of round {}.  Survivors {}".format(round_no,target_list))
        round_no = round_no + 1
    return target_list[0]

shooter_types = {'up':shootUp,'down':shootDown,'random':shootRandom,'upRound':shootUpRound}

# collect statistics
winner_list = []
num_shooters = 25
shooter_type = 'up'
num_games = 100
for _ in tqdm(range(num_games)):
    # initialize
    shooters = initialize_game(num_shooters=num_shooters,shooter_type=shooter_type)
    # play game
    winner = play_game(shooters=shooters, verbose=False)
    winner_list.append(winner)

plt.hist(winner_list,bins=2*num_shooters+1)
plt.xlabel('Shooter ID')
plt.ylabel('Number of wins')
plt.show()    
