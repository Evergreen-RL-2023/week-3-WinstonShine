'''
template: Richard Weiss, April 2023
g.grid world simulation 
you can do this in O-O, functional, or imperative style
I used O-O here

for O-O, there would be a GridCell class, which is also the state of the agent.
What are the instance methods?
you want to choose an action, get a reward and determine the next state
in the first version, the policy is random, ie the action is chosen randomly from the 4
steps:
initialize the g.grid
initialize the position of the agent
loop a number of steps
choose an action and compute the result


useful Python: match case, randrange, 
match repuires Python 3.10
'''
# Winston Shine
# Reinforcement Learning
# Lab 3
# 4/20/2023

import random as rnd

N = 5   #g.grid size
class Grid():
    #g.grid = []
    #length: int
    #width: int

    def __init__(self, size):
        self.grid = self.__generate_grid(size)
        self.length = size #square matrix, width is same

    def print_vals(self,size):
        for row in range(size):
            rowStr = ""
            for col in range(size):
                rowStr += "[ "+ "{0:.2f}".format(self.grid[row][col].val) + " ]"
            print(rowStr)

    def __generate_grid(self,size):
        grid = []
        #special g.grid cells a and b
        #A = (0,2)
        #B = (0,4)
        for i in range(size):
            grid.append([])
            for j in range(size):   
                match (i,j):
                    case (0,1):
                        grid[i].append(GridCell(i,j,1))
                    case (0,3):
                        grid[i].append(GridCell(i,j,2))
                    case _:
                        grid[i].append(GridCell(i,j,0))
        return grid

    def next_states(self,r,c):
        vals = []
        #north
        if r !=  0:
            vals.append(self.grid[r-1][c].val)
        else:
            vals.append(self.grid[r][c].val) # cell is next to edgesouth
        if r != 4:
            vals.append(self.grid[r+1][c].val)
        else:
            vals.append(self.grid[r][c].val) # cell is next to edge
        #east
        if c != 4:
            vals.append(self.grid[r][c+1].val)
        else:
            vals.append(self.grid[r][c].val) # cell is next to edge
        #west
        if c != 0:
            vals.append(self.grid[r][c-1].val)
        else:
            vals.append(self.grid[r][c].val) # cell is next to edge
        return vals

class Agent():
    def __init__(self,size):
        self.row = rnd.randrange(0,size-1)
        self.col = rnd.randrange(0,size-1)
        self.total_rewards = 0
        self.actions = ['n', 'e', 'w', 's']

    def get_location(self):
        return (self.row, self.col)

    def step(self, g):
        #choose action
        #act_index = rnd.randrange(0, 4)
        action = rnd.choice(self.actions)
        
        #generate reward
        current_cell = g.grid[self.row][self.col]
        reward, self.row, self.col = current_cell.get_next_cell(action)
        
        # state calculation
        current_cell.update_state(reward, g)
        self.total_rewards += reward # / count? do I need to track number of steps

class GridCell():
    def __init__(self, r, c, type):
        #state-value? initialized with rnd gauss?
        self.row = r
        self.col = c
        self.cell_type = type # 0 - normal, 1 - A, 2 - B
        self.val = 0
    
    # given the reward after an action is taken, and the values of all possible following states
    # this function calculates the new value of a cell
    def update_state(self, reward, g):
        if self.cell_type == 1:
            self.val = g.grid[4][1].val * .9 + reward # only one possible next state 
            return
        elif self.cell_type == 2:
            self.val = g.grid[2][3].val * .9 + reward # only one possible next state
            return
                
        #average all possible next states
        possible_next_states = g.next_states(self.row, self.col)
        avg = 0
        for val in possible_next_states:
            avg += (val * .9) #what if cell is against an edge? then count of states is not 4
        
        avg = avg / len(possible_next_states)
        #return avg value of neighbors + reward gained then apply discount
        self.val = avg + reward 
         
    #returns: reward, row, col
    #this functions determines a reward for a step, as well as finding the coordinates for the next cell
    def get_next_cell(self, action):
        reward = 0
        new_row = self.row
        new_col = self.col

        #Special cells
        #A = (0,1) - reward 10
        #B = (0,3) - reward 5
        if self.row == 0:
            match self.col:
                case 1: # case A
                    reward = 10
                    new_row = 4
                    new_col = 1
                    return reward, new_row, new_col

                case 3: # case B
                    reward = 5
                    new_row = 2
                    new_col = 3
                    return reward, new_row, new_col

        #if next location is out of bounds, location remains the same - reward -1
        match action:
            case "n":
                if self.row == 0:
                    reward = -1
                    #location remains unchanged
                else:
                    reward = 0
                    new_row = self.row - 1
            case "e":
                if self.col == 4:
                    reward = -1
                    #location remains unchanged
                else:
                    reward = 0
                    new_col = self.col + 1
                
            case "s":
                if self.row == 4:
                    reward = -1
                    #location remains unchanged
                else:
                    reward = 0
                    new_row = self.row + 1
            case "w":
                if self.col == 0:
                    reward = -1
                    #location remains unchanged
                else:
                    reward = 0
                    new_col = self.col - 1
        
        return reward, new_row, new_col

if __name__ == '__main__':
    n_steps = 10000

    #g.grid generation
    grid = Grid(N)
    grid.print_vals(N)
    
    #agent generation
    agent = Agent(grid.length)
    print(str(agent.total_rewards))
    for i in range(n_steps):
        agent.step(grid)

    #results
    print("Results after " + str(n_steps))
    grid.print_vals(N)
    print("Total Rewards = " + str(agent.total_rewards))
