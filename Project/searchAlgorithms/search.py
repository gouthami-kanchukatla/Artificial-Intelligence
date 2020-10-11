# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    root_node = problem.getStartState() #get the intial state
    fringe_nodes = util.Stack()  #fringe nodes is an openset follows LIFO structure, which has nodes to be explored 
    node_path  = [] 
    fringe_nodes.push((root_node,node_path))
    closed_set = set()  #close_set consists of already explored nodes
  
    while True: #Iterate until you find the goal node
        (check_node,node_path) = fringe_nodes.pop()
        if problem.isGoalState(check_node): #If the goal node is found,  search is successful, hence break.
            break
        elif check_node not in closed_set:   # if the state is not already visited, explore and add it to the visited states
            closed_set.add(check_node) 
            successor_nodes = problem.getSuccessors(check_node)  #retrieve the  successor states
            for (node,next_path,_) in successor_nodes:

                fringe_nodes.push((node,node_path+[next_path])) # add  the  successor states to explore further

    #print("res",node_path)
    return node_path

    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    root_node = problem.getStartState() #get the intial state
    fringe_nodes = util.Queue()  #fringe nodes is an openset follows FIFO structure, which has nodes to be explored 
    node_path  = [] 
    fringe_nodes.push((root_node,node_path))
    closed_set = set()  #close_set consists of already explored nodes
  
    while True: #Iterate until you find the goal node
        (check_node,node_path) = fringe_nodes.pop()
        if problem.isGoalState(check_node): #If the goal node is found,  search is successful, hence break.
            break
        elif check_node not in closed_set:   # if the state is not already visited, explore and add it to the visited states
            closed_set.add(check_node) 
            successor_nodes = problem.getSuccessors(check_node)  #retrieve the  successor states
            for (node,next_path,_) in successor_nodes:

                fringe_nodes.push((node,node_path+[next_path])) # add  the  successor states to explore further

    #print("res",node_path)
    return node_path

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    root_node = problem.getStartState() #get the intial state
    fringe_nodes = util.PriorityQueue() #fringe nodes are stored in the priority queue  with respect to the cost, lowest lost has highest priority
    node_path  = [] 
    node_cost = 0
    fringe_nodes.push((root_node,node_path,node_cost),node_cost)
    closed_set = set()  #close_set consists of already explored nodes
  
    while True: #Iterate until you find the goal node
        (check_node,node_path,node_cost) = fringe_nodes.pop()
        if problem.isGoalState(check_node): #If the goal node is found,  search is successful, hence break.
            break
        elif check_node not in closed_set:   # if the state is not already visited, explore and add it to the visited states
            closed_set.add(check_node) 
            successor_nodes = problem.getSuccessors(check_node)  #retrieve the  successor states
            for (node,next_path,cost) in successor_nodes:

                fringe_nodes.push((node,node_path+[next_path],node_cost+cost),node_cost+cost) # add  the  successor states to explore further

    #print("res",node_path)
    return node_path
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    root_node = problem.getStartState() #get the intial state
    fringe_nodes = util.PriorityQueue() #fringe nodes are stored in the priority queue  with respect to the node_cost+ heuristic_cost, lowest lost has highest priority
    node_path  = [] 
    node_cost = 0
    heu_cost = heuristic(root_node,problem)
    fringe_nodes.push((root_node,node_path,node_cost),node_cost+heu_cost)
    closed_set = set()  #close_set consists of already explored nodes
  
    while True: #Iterate until you find the goal node
        (check_node,node_path,node_cost) = fringe_nodes.pop()
        if problem.isGoalState(check_node): #If the goal node is found,  search is successful, hence break.
            break
        elif check_node not in closed_set:   # if the state is not already visited, explore and add it to the visited states
            closed_set.add(check_node) 
            successor_nodes = problem.getSuccessors(check_node)  #retrieve the  successor states
            for (node,next_path,cost) in successor_nodes:
                heu_cost =  heuristic(node, problem)
                fringe_nodes.push((node,node_path+[next_path],node_cost+cost),node_cost+cost+heu_cost) # add  the  successor states to explore further

    #print("res",node_path)
    return node_path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
