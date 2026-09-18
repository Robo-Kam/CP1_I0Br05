import numpy as np
from heapq import heapify, heappush, heappop
from collections import defaultdict

def getNeighbors(grid_dim: int, position: tuple):
    """
    checks the four neighboring cells of a given cell in the map and returns a list of the coordinates of the neighboring cells that are not obstructed
    Inputs:
        u (tuple) = coordinate of a cell in the map
    Outputs:
        neighbors (list of tuples) = distance of u to cand, list of coordinates of the neighboring cells that are not obstructed
    """
    neighbors = []
    
    for delta in ((0,1), (0,-1), (1,0), (-1,0)): # up, down, right, left
        cand = (position[0] + delta[0], position[1] + delta[1]) # row and column of the candidate neighbor
        # check if the candidate cell is within the bounds of the map, is not obstructed, and has not already been added to the list of neighbors
        # it's not obstructed if the value of the cell in the map is less than 0.3 (i.e., it is a movable cell)
        if cand[0] >= 0 and cand[0] < grid_dim and cand[1] >= 0 and cand[1] < grid_dim:
            cost = np.sqrt(delta[0]**2 + delta[1]**2) # distance from the position to the position + delta
            neighbors.append((cost, cand))

    return neighbors


def A_star(grid_dim: int, start: tuple, goal: tuple):

    queue = [(0,start)] # list of cells to be explored, initialized with the starting cell
    heapify(queue) # stores queue in a heap to associate memory allocation -- makes it faster and more streamlined

    # maintain a data structure to store the cost from the start node and init all entries with inf if there isn't already a value
    distances = defaultdict(lambda: float('inf')) # initialize with starting distance of inf, because we don't know what the shortest cost path is
    distances[start] = 0 # distance from start position is 0, duh

    visited = set() # track visited cells to avoid cycles.  Listed as a set to avoid multiple entries of the same position.
    parent = {} # dictionary to store the parent of each cell, which will be used to reconstruct the path from the goal to the start

    while queue:
        (currentdist, position) = heappop(queue) # add the current distance from the start and the position being checked

        if position in visited: # if we have already been to the position continue on to the next iteration of while loop.  Don't need to check again.
            continue
        visited.add(position) # add position to visited set to avoid re-checking positions
        if position == goal: # if the position being checked is the goal, then we have the shortest path.  break while loop
            break
        for (cost, u) in getNeighbors(grid_dim, position): # iterate over neighbors of the position: top, right, left, bottom
            # for example (0, start) = (0, (0,0)). neighbors = [((1, (0,1)), (1,(1,0))]
            newcost = distances[position] + cost # distances[start] = 0 + 1 = 1
            if newcost < distances[u]: # to start, if 1 < distances[(0,1)] (which is init with inf), add the new cost to the dict as well as the positions
                distances[u] = newcost # add new distance from the start to the dictionary
                parent[u] = position # update parents dictionary with new position for building path after loop
                euclidean_distance = np.sqrt((goal[0]-u[0])**2+(goal[1]-u[1])**2) # distance of the position to the goal
                heappush(queue, (newcost + euclidean_distance, u)) # update the dictionary for the current position with the total distance from the start to the goal
                # plt.plot(u[1], u[0], 'g*') # green star for each cell that is discovered and added to the queue
                # plt.show()
                # plt.pause(0.000001)

    # generate a list of the path from the goal to the start by following the parent dictionary
    key = goal # key is where we are trying to get to
    path = [] # list to store the path from the goal to the start.  Working backwards.

    while key in parent.keys(): # parent.keys was filled with positions from the while loop above, so it contains all the cells that were visited and their parents
        key = parent[key] # starts with goal, then goes to its parents
        if key in path: # if key is in the path, then stop
            break
        path.insert(0, key)# insert the parent of the current key at the beginning of the path list, so that the path is built in reverse order from the goal to the start

    path.append(goal)

    # for p in path:
    #     plt.plot(p[1], p[0], 'r.')
    # plt.ioff()
    # plt.show()
    #print(path)
    return path


