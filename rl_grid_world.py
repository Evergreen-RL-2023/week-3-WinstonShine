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
# Winston Shine
# Reinforcement Learning
# Lab 3
# 4/20/2023

import random as rnd

N = 5   #grid size
class Grid():
    #grid = []
    #length: int
    #width: int

    def __init__(self, size):
        self.grid = self.__generate_grid(size)
        self.length = size #square matrix, width is same

    def print_cell_type(self,size):
        for row in range(size):
            rowStr = ""
            for col in range(size):
                rowStr += "[ "+ str(self.grid[row][col].cell_type) + " ]"
            print(rowStr)

    def __generate_grid(self,size):
        grid = []
        #special grid cells a and b
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
#        act_index = rnd.randrange(0, 4)
        action = rnd.choice(self.actions)
        
        #generate reward
        current_cell = g.grid[self.row][self.col]
        reward, self.row, self.col = current_cell.get_next_cell(action)
        self.total_rewards += reward # / count? do I need to track number of steps

class GridCell():
    def __init__(self, r, c, type):
        #state-value? initialized with rnd gauss?
        self.row = r
        self.col = c
        self.cell_type = type # 0 - normal, 1 - A, 2 -B
    
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
                    new_row = self.row + 1
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
                    new_col = self.col + 1
        
        return reward, new_row, new_col

if __name__ == '__main__':
    
    #grid generation
    grid = Grid(N)
    grid.print_cell_type(N)

    #agent generation
    agent = Agent(grid.length)
    print(str(agent.get_location()) + " " + str(agent.total_rewards))
    agent.step(grid)
    print(str(agent.get_location()) + " " + str(agent.total_rewards))

    #test cases for special cells A and B
    #A = (0,1) - reward 10
    #B = (0,3) - reward 5
    print("\nTest cases for special cells A and B")
    agentA = Agent(grid.length)
    agentB = Agent(grid.length)
    agentA.row = 0
    agentA.col = 1
    agentB.row = 0
    agentB.col = 3
    agentA.step(grid)
    agentB.step(grid)
    print(str(agentA.get_location()) + " " + str(agentA.total_rewards))
    print(str(agentB.get_location()) + " " + str(agentB.total_rewards))

    #Test cases for edge of grid
    print("\nTest cases for grid edges")
    edge_agent = Agent(grid.length)
    
    i = 0
    # north edge
    while i < 5:
        edge_agent.row = 0
        edge_agent.col = i
        edge_agent.actions = ['n']
        edge_agent.step(grid)
        print(str(edge_agent.get_location()) + " " + str(edge_agent.total_rewards))
        i += 1
    i = 0
    # east edge
    while i < 5:
        edge_agent.row = i
        edge_agent.col = 4
        edge_agent.actions = ['e']
        edge_agent.step(grid)
        print(str(edge_agent.get_location()) + " " + str(edge_agent.total_rewards))
        i += 1
    i = 0
    # south edge
    while i < 5:
        edge_agent.row = 4
        edge_agent.col = i
        edge_agent.actions = ['s']
        edge_agent.step(grid)
        print(str(edge_agent.get_location()) + " " + str(edge_agent.total_rewards))
        i += 1
    i = 0
    # west edge
    while i < 5:
        edge_agent.row = i
        edge_agent.col = 0
        edge_agent.actions = ['w']
        edge_agent.step(grid)
        print(str(edge_agent.get_location()) + " " + str(edge_agent.total_rewards))
        i += 1
