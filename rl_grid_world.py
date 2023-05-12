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
# Lab 3 & 4
# 5/11/2023

import random as rnd

N = 5   # grid size
class Grid():
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
        rewards = []
        #north
        if r !=  0:
            vals.append(self.grid[r-1][c].val)
            rewards.append(0)
        else:
            vals.append(self.grid[r][c].val) # cell is next to edge
            rewards.append(-1)
        #south
        if r != 4:
            vals.append(self.grid[r+1][c].val)
            rewards.append(0)
        else:
            vals.append(self.grid[r][c].val) # cell is next to edge
            rewards.append(-1)
        #east
        if c != 4:
            vals.append(self.grid[r][c+1].val)
            rewards.append(0)
        else:
            vals.append(self.grid[r][c].val) # cell is next to edge
            rewards.append(-1)
        #west
        if c != 0:
            vals.append(self.grid[r][c-1].val)
            rewards.append(0)
        else:
            vals.append(self.grid[r][c].val) # cell is next to edge
            rewards.append(-1)
        return rewards, vals

class Agent():
    def __init__(self,size):
        self.row = rnd.randrange(0,size-1)
        self.col = rnd.randrange(0,size-1)
        self.total_rewards = 0
        self.actions = ['n', 'e', 'w', 's']

    def step(self, g):
        # choose action
        # act_index = rnd.randrange(0, 4)
        action = rnd.choice(self.actions)
        
        # find next cell
        current_cell = g.grid[self.row][self.col]
        self.row, self.col = current_cell.get_next_cell(action)
        
        # state value calculation
        current_cell.update_state(g)

class GridCell():
    def __init__(self, r, c, type):
        #state-value? initialized with rnd gauss?
        self.row = r
        self.col = c
        self.cell_type = type # 0 - normal, 1 - A, 2 - B
        self.val = 0
    
    # calculate return
    def value_function(self,reward,val):
        return val * .9 + reward
    
    # this function calculates the new value of a cell using the average return from all possible next states
    # uses .9 discount
    def update_state(self, g):
        if self.cell_type == 1:
            self.val = self.value_function(10,g.grid[4][1].val)

        elif self.cell_type == 2:
            self.val = self.value_function(5,g.grid[2][3].val)


        else:
            #average all possible next states
            adj_rewards, adj_vals = g.next_states(self.row, self.col)
            avg = 0
            i = 0
            while i < len(adj_vals):
                avg += self.value_function(adj_rewards[i], adj_vals[i])
                i+=1

            avg = avg / len(adj_vals)
            #return avg value of neighbors + reward gained then apply discount
            self.val = avg
         
    #returns: row, col
    #doing an unnecessary assignment here - fix later
    def get_next_cell(self, action):
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
                    return new_row, new_col

                case 3: # case B
                    reward = 5
                    new_row = 2
                    new_col = 3
                    return new_row, new_col

        #if next location is out of bounds, location remains the same
        match action:
            case "n":
                if self.row != 0:
                    new_row = self.row - 1
            case "e":
                if self.col != 4:
                    new_col = self.col + 1
            case "s":
                if self.row != 4:
                    new_row = self.row + 1
            case "w":
                if self.col != 0:
                    new_col = self.col - 1
        
        return new_row, new_col

if __name__ == '__main__':
    n_steps = 5000

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
    
    print(grid.grid[0][0].val)
    print(grid.grid[0][1].val)