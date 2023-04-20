'''
template: Richard Weiss, April 2023
grid world simulation 
you can do this in O-O, functional, or imperative style
I used O-O here

for O-O, there would be a GridCell class, which is also the state of the agent.
What are the instance methods?
you want to choose an action, get a reward and determine the next state
in the first version, the policy is random, ie the action is chosen randomly from the 4
steps:
initialize the grid
initialize the position of the agent
loop a number of steps
choose an action and compute the result


useful Python: match case, randrange, 
match repuires Python 3.10
'''
import numpy as np
import random as rnd

N = 5   #grid size



class GridCell():
    def __init__(self, r, c):
        actions = ['n', 'e', 'w', 's']
        # what else do you need?
        row = r
        col = c


    def get_reward(action):
        if row == 0 and action == 's':
            reward = 2
        else:
            reward = 0
        return reward

    
    def get_next_cell(action):
        r = row
        c = col
        # action is 'n', 'e', 's', 'w'
        '''
        match action:
           case 'n':
              r -= 1
           case _:
              print(action, 'invalid action')
        '''

        return r,c
    

    def step():
        act_index = rnd.randrange(0, 4)
        action = actions[act_index]
        rwd = get_reward(action)


if __name__ == '__main__':
    rnd.seed(42)
    grid = []

    for i in range(N):
        grid.append([])
        for j in range(N):
            grid[i].append(GridCell(i,j))
            print(grid[i][j], end=' ')
