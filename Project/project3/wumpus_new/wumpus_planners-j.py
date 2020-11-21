# wumpus_planners.py
# ------------------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

from wumpus_environment import *
from wumpus_kb import *
import search

#-------------------------------------------------------------------------------
# Distance fn
#-------------------------------------------------------------------------------

def manhattan_distance_with_heading(current, target):
    """
    Return the Manhattan distance + any turn moves needed
        to put target ahead of current heading
    current: (x,y,h) tuple, so: [0]=x, [1]=y, [2]=h=heading)
    heading: 0:^:north 1:<:west 2:v:south 3:>:east
    """
    md = abs(current[0] - target[0]) + abs(current[1] - target[1])
    if current[2] == 0:   # heading north
        # Since the agent is facing north, "side" here means
        # whether the target is in a row above or below (or
        # the same) as the agent.
        # (Same idea is used if agent is heading south)
        side = (current[1] - target[1])
        if side > 0:
            md += 2           # target is behind: need to turns to turn around
        elif side <= 0 and current[0] != target[0]:
            md += 1           # target is ahead but not directly: just need to turn once
        # note: if target straight ahead (curr.x == tar.x), no turning required
    elif current[2] == 1: # heading west
        # Now the agent is heading west, so "side" means
        # whether the target is in a column to the left or right
        # (or the same) as the agent.
        # (Same idea is used if agent is heading east)
        side = (current[0] - target[0])
        if side < 0:
            md += 2           # target is behind
        elif side >= 0 and current[1] != target[1]:
            md += 1           # target is ahead but not directly
    elif current[2] == 2: # heading south
        side = (current[1] - target[1])
        if side < 0:
            md += 2           # target is behind
        elif side >= 0 and current[0] != target[0]:
            md += 1           # target is ahead but not directly
    elif current[2] == 3: # heading east
        side = (current[0] - target[0])
        if side > 0:
            md += 2           # target is behind
        elif side <= 0 and current[1] != target[1]:
            md += 1           # target is ahead but not directly
    return md


#-------------------------------------------------------------------------------
# Plan Route
#-------------------------------------------------------------------------------

def plan_route(current, heading, goals, allowed):
    """
    Given:
       current location: tuple (x,y)
       heading: integer representing direction
       gaals: list of one or more tuple goal-states
       allowed: list of locations that can be moved to
    ... return a list of actions (no time stamps!) that when executed
    will take the agent from the current location to one of (the closest)
    goal locations
    You will need to:
    (1) Construct a PlanRouteProblem that extends search.Problem
    (2) Pass the PlanRouteProblem as the argument to astar_search
        (search.astar_search(Problem)) to find the action sequence.
        Astar returns a node.  You can call node.solution() to exract
        the list of actions.
    NOTE: represent a state as a triple: (x, y, heading)
          where heading will be an integer, as follows:
          0='north', 1='west', 2='south', 3='east'
    """

    # Ensure heading is a in integer form
    if isinstance(heading,str):
        heading = Explorer.heading_str_to_num[heading]

    if goals and allowed:
        prp = PlanRouteProblem((current[0], current[1], heading), goals, allowed)
        # NOTE: PlanRouteProblem will include a method h() that computes
        #       the heuristic, so no need to provide here to astar_search()
        node = search.astar_search(prp)
        if node:
            return node.solution()
    
    # no route can be found, return empty list
    return []

#-------------------------------------------------------------------------------

class PlanRouteProblem(search.Problem):
    def __init__(self, initial, goals, allowed):
        """ Problem defining planning of route to closest goal
        Goal is generally a location (x,y) tuple, but state will be (x,y,heading) tuple
        initial = initial location, (x,y) tuple
        goals   = list of goal (x,y) tuples
        allowed = list of state (x,y) tuples that agent could move to """
        self.initial = initial # initial state
        self.goals = goals     # list of goals that can be achieved
        self.allowed = allowed # the states we can move into

    def h(self,node):
        """
        Heuristic that will be used by search.astar_search()
        """
        goal_distances=[]
        goal_distances = [manhattan_distance_with_heading(node.state,goal) for goal in self.goals]  #calculating the distances of each goal node from the start node
        mini=min(goal_distances) #finding the nearest goal node
        return(mini)


    def actions(self, state):
        """
        Return list of allowed actions that can be made in state
        """
        L1 = ['Forward','TurnLeft','TurnRight']
        L2 = ['TurnLeft','TurnRight']
        if state[2] == 0 and (state[0],state[1]+1) in self.allowed:       #IF FACING NORTH
            return(L1)
        if state[2] == 1 and (state[0]-1,state[1]) in self.allowed:        #IF FACING WEST
            return(L1)
        if state[2] == 2 and (state[0],state[1]-1) in self.allowed:        #IF FACING SOUTH
            return(L1)
        if state[2] == 3 and (state[0]+1,state[1]) in self.allowed:         #IF FACING EAST
            return(L1)
        return(L2)  #IF THE NEXT FORWARD TILE IS BLOCKED


    def result(self, state, action):
        """
        Return the new state after applying action to state
        0 = North
        1 = West
        2 = South
        3 = East
        """
        if action == 'TurnLeft':
            if state[2] == 0:  #if NORTH
                return(state[0],state[1],1)  #RESULT FACING WEST
            if state[2] == 1:  #IF WEST
                return(state[0],state[1],2) #RESULT FACING SOUTH
            if state[2] == 2: #IF SOUTH
                return (state[0],state[1],3) #RESULT FACING EAST
            if state[2] == 3: #IF EAST
                return(state[0],state[1],0)  #RESULT FACING NORTH

        if action == 'TurnRight':
            if state[2] == 0:  #if NORTH
                return(state[0],state[1],3)  #RESULT FACING EAST
            if state[2] == 1:  #IF WEST
                return(state[0],state[1],0)   #RESULT FACING NORTH
            if state[2] == 2:   #IF SOUTH
                return(state[0],state[1],1)   #RESULT FACING WEST
            if state[2] == 3:   #IF EAST
                return(state[0],state[1],2)   #RESULT FACING SOUTH

        

        if action == 'Forward':
            if state[2] == 0:   #IF NORTH
                return(state[0],state[1] + 1,state[2])  #MOVE FORWARD IN Y DIRECTION(X,Y=Y+1)
            if state[2] == 1: #IF WEST
                return(state[0]-1,state[1],state[2])   #MOVE BACKWARD IN X DIRECTION (X=X-1,Y)
            if state[2] == 2: #IF SOUTH
                return(state[0],state[1]-1,state[2])   #MOVE BACKWARD IN Y DIRECTION (X,Y=Y-1)
            if state[2] == 3:  #IF EAST
                return(state[0]+1,state[1],state[2])   #MOVE FORWARD IN X DIRECTION(X=X+1,Y)



    def goal_test(self, state):
        """
        Return True if state is a goal state
        """
        if(state[0:2] in self.goals):  #checking if current x,y is a goal state or not
            p=True
        else:
            p=False
        return(p)


#-------------------------------------------------------------------------------

def test_PRP(initial):
    """
    The 'expected initial states and solution pairs' below are provided
    as a sanity check, showing what the PlanRouteProblem soluton is
    expected to produce.  Provide the 'initial state' tuple as the
    argument to test_PRP, and the associate solution list of actions is
    expected as the result.
    The test assumes the goals are [(2,3),(3,2)], that the heuristic fn
    defined in PlanRouteProblem uses the manhattan_distance_with_heading()
    fn above, and the allowed locations are:
        [(0,0),(0,1),(0,2),(0,3),
        (1,0),(1,1),(1,2),(1,3),
        (2,0),            (2,3),
        (3,0),(3,1),(3,2),(3,3)]
    
    Expected intial state and solution pairs:
    (0,0,0) : ['Forward', 'Forward', 'Forward', 'TurnRight', 'Forward', 'Forward']
    (0,0,1) : ['TurnRight', 'Forward', 'Forward', 'Forward', 'TurnRight', 'Forward', 'Forward']
    (0,0,2) : ['TurnLeft', 'Forward', 'Forward', 'Forward', 'TurnLeft', 'Forward', 'Forward']
    (0,0,3) : ['Forward', 'Forward', 'Forward', 'TurnLeft', 'Forward', 'Forward']
    """
    return plan_route((initial[0],initial[1]), initial[2],
                      # Goals:
                      [(2,3),(3,2)],
                      # Allowed locations:
                      [(0,0),(0,1),(0,2),(0,3),
                       (1,0),(1,1),(1,2),(1,3),
                       (2,0),            (2,3),
                       (3,0),(3,1),(3,2),(3,3)])


# -------------------------------------------------------------------------------
# Plan Shot
# -------------------------------------------------------------------------------

def plan_shot(current, heading, goals, allowed):
    """ Plan route to nearest location with heading directed toward one of the
    possible wumpus locations (in goals), then append shoot action.
    NOTE: This assumes you can shoot through walls!!  That's ok for now. """
    if goals and allowed:
        psp = PlanShotProblem((current[0], current[1], heading), goals, allowed)
        node = search.astar_search(psp)
        if node:
            plan = node.solution()
            plan.append(action_shoot_str(None))
            # HACK:
            # since the wumpus_alive axiom asserts that a wumpus is no longer alive
            # when on the previous round we perceived a scream, we
            # need to enforce waiting so that itme elapses and knowledge of
            # "dead wumpus" can then be inferred...
            plan.append(action_wait_str(None))
            return plan

    # no route can be found, return empty list
    return []


# -------------------------------------------------------------------------------

class PlanShotProblem(search.Problem):
    def __init__(self, initial, goals, allowed):
        """ Problem defining planning to move to location to be ready to
              shoot at nearest wumpus location
        NOTE: Just like PlanRouteProblem, except goal is to plan path to
              nearest location with heading in direction of a possible
              wumpus location;
              Shoot and Wait actions is appended to this search solution
        Goal is generally a location (x,y) tuple, but state will be (x,y,heading) tuple
        initial = initial location, (x,y) tuple
        goals   = list of goal (x,y) tuples
        allowed = list of state (x,y) tuples that agent could move to """
        self.initial = initial  # initial state
        self.goals = goals  # list of goals that can be achieved
        self.allowed = allowed  # the states we can move into

    def h(self, node):
        """
        Heuristic that will be used by search.astar_search()
        """
        possibleWumpusLocations = self.goals
        explorerLocations = self.allowed
        shotSpots = []

        for WumpusLoc in possibleWumpusLocations:
            for ExplorerLoc in explorerLocations:
                if (WumpusLoc[0] == ExplorerLoc[0]) or (WumpusLoc[1] == ExplorerLoc[1]):
                    shotSpots.append(ExplorerLoc)

        distanceToShotSpots = [manhattan_distance_with_heading(node.state, goal) for goal in shotSpots]
        return min(distanceToShotSpots)


        
    

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        if action == 'TurnLeft':
            if state[2] == 0:  #if NORTH
                return(state[0],state[1],1)  #RESULT FACING WEST
            if state[2] == 1:  #IF WEST
                return(state[0],state[1],2) #RESULT FACING SOUTH
            if state[2] == 2: #IF SOUTH
                return (state[0],state[1],3) #RESULT FACING EAST
            if state[2] == 3: #IF EAST
                return(state[0],state[1],0)  #RESULT FACING NORTH

        if action == 'TurnRight':
            #print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
            if state[2] == 0:  #if NORTH
                return(state[0],state[1],3)  #RESULT FACING EAST
            if state[2] == 1:  #IF WEST
                return(state[0],state[1],0)   #RESULT FACING NORTH
            if state[2] == 2:   #IF SOUTH
                return(state[0],state[1],1)   #RESULT FACING WEST
            if state[2] == 3:   #IF EAST
                return(state[0],state[1],2)   #RESULT FACING SOUTH

        

        if action == 'Forward':
            if state[2] == 0:   #IF NORTH
                return(state[0],state[1] + 1,state[2])  #MOVE FORWARD IN Y DIRECTION(X,Y=Y+1)
            if state[2] == 1: #IF WEST
                return(state[0]-1,state[1],state[2])   #MOVE BACKWARD IN X DIRECTION (X=X-1,Y)
            if state[2] == 2: #IF SOUTH
                return(state[0],state[1]-1,state[2])   #MOVE BACKWARD IN Y DIRECTION (X,Y=Y-1)
            if state[2] == 3:  #IF EAST
                return(state[0]+1,state[1],state[2])   #MOVE FORWARD IN X DIRECTION(X=X+1,Y)

        #if action == 'Shoot':
        #    return(state[0],state[1],state[2])   #RETURN CURRENT LOCATION



    
    def actions(self, state):
        """
        Return list of allowed actions that can be made in state
        """
        L1 = ['Forward','TurnLeft','TurnRight']
        L2 = ['TurnLeft','TurnRight']
        if state[2] == 0 and (state[0],state[1]+1) in self.allowed:       #IF FACING NORTH
            return(L1)
        if state[2] == 1 and (state[0]-1,state[1]) in self.allowed:        #IF FACING WEST
            return(L1)
        if state[2] == 2 and (state[0],state[1]-1) in self.allowed:        #IF FACING SOUTH
            return(L1)
        if state[2] == 3 and (state[0]+1,state[1]) in self.allowed:         #IF FACING EAST
            return(L1)
        return(L2)  #IF THE NEXT FORWARD TILE IS BLOCKED


    def goal_test(self, state):
        """
        Return True if state is a goal state
        """
        possibleWumpusLocations = self.goals
        print("Inside goal test @ plan shot")
        if state in self.goals:     #RETURN FALSE IF YOUR CURRENT STATE MATCHES WITH ONE OF THE GOAL STATE
            return False

        for location in possibleWumpusLocations:  #CHECH ALL THE GOAL NODES ONE AT A TIME
            
            if location[1] == state[1]: #IF BOTH Y CORDINATES MATCHES THEN 
                if ((location[0] < state[0]) and state[2] == 1): #IF X CORDINATE OF GOAL NODE IS LESS THAN CURRENT STATE AND THE DIRECTION IS WEST
                    return True #RETURN TRUE
                if ((location[0] > state[0]) and state[2] == 3): #IF X CORDINATE OF GOAL NODE IS GREATER THAN CURRENT STATE AND THE DIRECTION IS EAST
                    return True       #RETURN TRUE

            if location[0] == state[0]:   #IF BOTH X CORDINATES MATCHES THEN 
                if ((location[1] > state[1]) and state[2] == 0): #IF Y CORDINATE OF GOAL NODE IS GREATER THAN CURRENT STATE AND THE DIRECTION IS NORTH
                    return True   #RETURN TRUE
                if ((location[1] < state[1]) and state[2] == 2):  #IF Y CORDINATE OF GOAL NODE IS LESS THAN CURRENT STATE AND THE DIRECTION IS SOUTH
                    return True  #RETURN TRUE

# -------------------------------------------------------------------------------

def test_PSP(initial=(0, 0, 3)):
    """
    The 'expected initial states and solution pairs' below are provided
    as a sanity check, showing what the PlanShotProblem soluton is
    expected to produce.  Provide the 'initial state' tuple as the
    argumetn to test_PRP, and the associate solution list of actions is
    expected as the result.
    The test assumes the goals are [(2,3),(3,2)], that the heuristic fn
    defined in PlanShotProblem uses the manhattan_distance_with_heading()
    fn above, and the allowed locations are:
        [(0,0),(0,1),(0,2),(0,3),
        (1,0),(1,1),(1,2),(1,3),
        (2,0),            (2,3),
        (3,0),(3,1),(3,2),(3,3)]
    Expected intial state and solution pairs:
    (0,0,0) : ['Forward', 'Forward', 'TurnRight', 'Shoot', 'Wait']
    (0,0,1) : ['TurnRight', 'Forward', 'Forward', 'TurnRight', 'Shoot', 'Wait']
    (0,0,2) : ['TurnLeft', 'Forward', 'Forward', 'Forward', 'TurnLeft', 'Shoot', 'Wait']
    (0,0,3) : ['Forward', 'Forward', 'Forward', 'TurnLeft', 'Shoot', 'Wait']
    """
    return plan_shot((initial[0], initial[1]), initial[2],
                     # Goals:
                     [(2, 3), (3, 2)],
                     # Allowed locations:
                     [(0, 0), (0, 1), (0, 2), (0, 3),
                      (1, 0), (1, 1), (1, 2), (1, 3),
                      (2, 0), (2, 3),
                      (3, 0), (3, 1), (3, 2), (3, 3)])

# -------------------------------------------------------------------------------