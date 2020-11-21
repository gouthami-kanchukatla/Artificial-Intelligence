# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        pacman_pos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        closeness_score = 0
        food_distance  = float("inf")
        ghost_distance  = float("inf")

        for ghost_pos in successorGameState.getGhostPositions():

            #calculate the manhattandistance between the pacman and the ghost
            pacman_ghost_distance = manhattanDistance(pacman_pos, ghost_pos)

            #compute the nearest ghost to the pacman
            ghost_distance = min([ghost_distance, pacman_ghost_distance])

        #The  ghost is assumed to be very close under this condition
        if(ghost_distance <= 1):

        		# The pacman has high probability to loose as it very close and 
        		#can be eaten by the ghost, therefore reduce the score. 
                closeness_score = closeness_score - 1000  
        
        food_list = newFood.asList()

        for food_pos in food_list:

            #calculate the manhattandistance between the pacman and the food pallete
            pacman_food_distance = manhattanDistance(pacman_pos, food_pos)

            #compute the nearest food pallete to the pacman
            food_distance = min([food_distance, pacman_food_distance])
       
        return successorGameState.getScore() + closeness_score + (1.0/food_distance)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an aent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        "*** YOUR CODE HERE ***"
        best_action = self.maxValue(gameState, 0, 0)
        #return the bestAction through which we can optimize the value for pacman
        return self.best_action

    def minimax(self,gameState,agentIndex, depth):

       # Evaluate if explored all depths or if gamestate = winstate or losestate
        if  depth == self.depth or  gameState.isLose() or gameState.isWin() :
            return self.evaluationFunction(gameState)
        
        #As given in the description, pacman is agent 0, therefore maximize it
        elif agentIndex == 0:
            return self.maxValue(gameState,agentIndex, depth)
        # if the agent is not equal to zero then  it is a ghost, therefore minimize it.
        else:
            return self.minValue(gameState,agentIndex, depth)

    def minValue(self,gameState, agentIndex, depth):
        # min_node_list has a list of the nodes distances with respective actions
        min_node_list= []
        # setting the min score to the largest num possible, state as Directions.STOP 
        initial_values = (float("inf"), Directions.STOP) 
        min_node_list.append(initial_values)

        # retrieving all possible legal actions from the current state
        next_states = gameState.getLegalActions(agentIndex)
        for state in next_states:
            num_agents = gameState.getNumAgents()

            #Checking  for the last ghost through this condition
            if agentIndex + 1 == num_agents: 
	            #calculate the cost it takes to reach the successor
                min_score= self.minimax(gameState.generateSuccessor(agentIndex, state), 0, depth + 1)
                
            else: 
            	#exploringg all the other ghosts other than last ghost
                min_score = self.minimax(gameState.generateSuccessor(agentIndex, state), agentIndex + 1, depth)
            min_node_list.append((min_score, state))

            # find the minimum value of the successor states to send it to remaining ghosts.
            (self.min_score, self.best_action) = min(min_node_list)
        return self.min_score
        util.raiseNotDefined()

    def maxValue(self,gameState, agentIndex, depth):
        # max_node_list has a list of the nodes distances with respective actions
        max_node_list = []
        # setting the min score to the largest num possible, state as Directions.STOP 
        initial_values = (float("-inf"),Directions.STOP)

        max_node_list.append(initial_values)
        # retrieving all possible legal actions from the current state
        next_states = gameState.getLegalActions(agentIndex)
        for state in next_states:
            #calculate the cost it takes to reach the successor
            max_score = self.minimax(gameState.generateSuccessor(agentIndex, state),1, depth)
            max_node_list.append((max_score, state))
            (self.max_score,self.best_action) = max(max_node_list)

        return self.max_score

    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

         # intialiize  depth, alpha &  beta with default values.
        alpha_beta_best_Action = self.maxValue(gameState, 0, 0, float("-inf"), float("inf"))
        #To optimize the value for pacman, return the best possible action
        return self.alpha_beta_best_Action

    def alphaBeta(self, gameState, agentIndex, depth,alpha, beta):
        # Evaluate if explored all depths or if gamestate = winstate or losestate
        if  depth == self.depth or  gameState.isLose() or gameState.isWin() :
            return self.evaluationFunction(gameState)
        
        #As given in the description, pacman is agent 0, therefore maximize it
        elif agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth,alpha, beta)
        # if the agent is not equal to zero then  it is a ghost, therefore minimize it.
        else:
            return self.minValue(gameState, agentIndex, depth,alpha,beta)

    def minValue(self, gameState, agentIndex, depth,alpha, beta):
        # min_node_list has a list of the nodes distances with respective actions
        min_node_list= []

        # setting the min score to the largest num possible, state as Directions.STOP 
        initial_values = (float("inf"), Directions.STOP) 
        min_node_list.append(initial_values)

        # retrieving all possible legal actions from the current state
        next_states = gameState.getLegalActions(agentIndex)
        for state in next_states:
            num_agents = gameState.getNumAgents()
            # condition for the lastghost
            # exploring the ghosts and find the minimum value of the successor states to pass it to remaining ghosts
            if agentIndex + 1 == num_agents:  # exploring the lastghost
                # find the pacman agent min value of the successor states

                min_score = self.alphaBeta(gameState.generateSuccessor(agentIndex, state), 0, depth + 1,alpha, beta)
                min_node_list.append((min_score, state))
                (self.alpha_beta_min_value, self.alpha_beta_best_Action) = min(min_node_list)
            else:  # exploring the  remaning ghosts except the last ghost
                min_score = self.alphaBeta(gameState.generateSuccessor(agentIndex, state), agentIndex + 1, depth,alpha , beta)
                min_node_list.append((min_score, state))

                (self.alpha_beta_min_value, self.alpha_beta_best_Action_2) = min(min_node_list)


            # If alpha_beta_min_value < alpha, we can return the alpha_beta_min_value without any need to check the childnodes
            #  Following the alpha-beta pruning to reduce the amount of computation needed, set beta value to min of alpha_beta_min_value and beta .
            if (self.alpha_beta_min_value < alpha): return self.alpha_beta_min_value
            beta = min(beta, self.alpha_beta_min_value)

        return self.alpha_beta_min_value

  

    def maxValue(self, gameState, agentIndex, depth, alpha, beta):
        #list to keep track of nodesdistances and their actions
        max_node_list = []
        initial_values = (float("-inf"),Directions.STOP)

        max_node_list.append(initial_values)

        # retrieving all possible legal actions from the current state
        next_states = gameState.getLegalActions(agentIndex)
        for state in next_states:
            # calculate the cost it takes to reach the successor
            max_score = self.alphaBeta(gameState.generateSuccessor(agentIndex, state), 1, depth,alpha,beta)
            max_node_list.append((max_score, state))
            (self.alpha_beta_max_value, self.alpha_beta_best_Action) = max(max_node_list)

            # If alpha_beta_max_value > alpha, we can return the alpha_beta_max_value without any need to check the childnodes
            if(self.alpha_beta_max_value > beta):
                return self.alpha_beta_max_value

            #  Following the alpha-beta pruning to reduce the amount of computation needed, set beta value to min of alpha_beta_min_value and beta .
            alpha = max(self.alpha_beta_max_value,alpha)
        return self.alpha_beta_max_value

    


        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectiMax(gameState, agentIndex, depth):

			num_agents = gameState.getNumAgents()
			if agentIndex == num_agents: #checking if the agent is a last ghost

				#If explored all the  depths, return
				if depth == self.depth: 
					gameState=self.evaluationFunction(gameState)
					return(gameState)
				else:      
					#continue if the max depth has not yet been reached
					return expectiMax(gameState, 0, depth + 1)

			else:  
				#if not in min layer
				next_states = gameState.getLegalActions(agentIndex)

				if(not len(next_states) ):
					gameState = self.evaluationFunction(gameState)
					return(gameState)
					#finding all the mini max values
				mini_max = (expectiMax(gameState.generateSuccessor(agentIndex, i), agentIndex + 1, depth) for i in next_states)  
				#if the agent is pacman then calculate the max value of minimax 
				if agentIndex == 0:  return max(mini_max)
				else:   # if not agent,  find the expectimax value by storing all the possible moves in a set, taking sum, finding ratio
					mini_max_set =  set(mini_max)
					mini_max_sum =  sum(mini_max_set)     
					length=len(mini_max_set)    
					ratio = (mini_max_sum/length)  
					return(ratio)

        action_highest_min_max = max(gameState.getLegalActions(0), key=lambda x: expectiMax(gameState.generateSuccessor(0, x), 1, 1))
        # return the action with highest minimax value
        return(action_highest_min_max)





def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    current_food_states = currentGameState.getFood()
    current_pacman_pos = currentGameState.getPacmanPosition()
    score = 0
    closest_food_distance = float("inf")

    #if the pacman has found food  in its current position then increment the score

    if current_food_states[current_pacman_pos[0]][current_pacman_pos[1]] != 0: score = score+10

    for food in current_food_states.asList():

    	#if food is in  capsules form, further increase the score
        if food in currentGameState.getCapsules():
            score = score + 150

        # calculate  the manhattanDistance between pacman and food
        pacman_food_distance = manhattanDistance(current_pacman_pos, food)
        # compute the minimum of the distances
        closest_food_distance = min([closest_food_distance, pacman_food_distance])
        

    left_food_palletes = len(current_food_states.asList())
    current_ghost_states = currentGameState.getGhostStates()
    closest_ghost_distance = float("inf")

    for ghost in current_ghost_states:
        # calculate  the manhattanDistance between pacman and ghost
        pacman_ghost_distance = manhattanDistance(current_pacman_pos, ghost.getPosition())
        # find the closest ghost to the pacman
        closest_ghost_distance = min([closest_ghost_distance, pacman_ghost_distance])
        # if the closest distance   is <= 1, ghost will eat pacman
        if (closest_ghost_distance <= 1):

        	# If the ghost isn't scared then decrement the score to make the pacman run away from  the ghost
            if not ghost.scaredTimer:  
                score = score - 1000
            else: 
            #if the ghost is scared, then increase the score
                score = score + 2000

    if(current_pacman_pos == ghost.getPosition):
        return float("-inf")

    return currentGameState.getScore() + score + (1.0 / closest_food_distance) -2* left_food_palletes
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

