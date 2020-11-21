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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        score = 0
        distance = float("inf")
        #loop through all the food
        for food in newFood.asList():
            #find the distance between pacman and food
            distancebetweenPacmanAndFood = manhattanDistance(newPos, food)
            #compute the minimum of the distances
            distance = min([distance, distancebetweenPacmanAndFood])
        distance2 = float("inf")
        #loop through the ghosts
        for ghost in newGhostStates:
            #find the distance between the pacman and the ghost
            distancebetweenPacmanAndGhost = manhattanDistance(newPos, ghost.getPosition())
            #find the nearest ghost to the pacman
            distance2 = min([distance2, distancebetweenPacmanAndGhost])
        #if the distance between ghost and pacman < 1
        if(distance2 <= 1): #ghost is very near to pacman
                score = score - 1000  #decrease the score as the ghost can eat the pacman and pacman might loose
        #return the score
        return successorGameState.getScore() + score + (1.0/distance)

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
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #Start from the pacman at depth 0 and maximize the value of pacman
        action = self.max_value(gameState, 0, 0)
        #return the bestAction through which we can optimize the value for pacman
        return self.bestAction

    def minimax(self,gameState,agentIndex, depth):
        #If the current gamestate is in winstates or in losestates or we have to explored all the depths
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            #If any of the above condition is satisfied return the evaluationfunction
            return self.evaluationFunction(gameState)
        #If the agentIndex is 0 it means we are exploring the Pacman
        if agentIndex == 0:
            #Since we are exploring the pacman we want to maximize the value it gets
            return self.max_value(gameState,agentIndex, depth)
        # If the agentIndex is other than 0 it means we are exploring the ghosts
        else:
            # Since we are exploring the ghosts we want to minimize the value it gets
            return self.min_value(gameState,agentIndex, depth)

    def max_value(self,gameState, agentIndex, depth):
        #Initialize temp value to -inf and Directions.STOP since we want to get the max_value
        temp = (float("-inf"),Directions.STOP)
        #list to keep track of nodesdistances and their actions
        maxlist = []
        #add the temp to maxlist
        maxlist.append(temp)
        #get all possible actions from the current state
        nextStates = gameState.getLegalActions(agentIndex)
        #loop through all the actions possible
        for nextState in nextStates:
            #compute the cost it takes to reach the successor
            maxvalue = self.minimax(gameState.generateSuccessor(agentIndex, nextState),1, depth)
            #add the computed value and corresponding action to the maxlist
            maxlist.append((maxvalue, nextState))
            #get the maximum value from the maxlist and assign the maxvalue to self.maxvalue and the corresponding action to self.bestAction
            (self.maxvalue,self.bestAction) = max(maxlist)
        #returns the max_value
        return self.maxvalue

    def min_value(self,gameState, agentIndex, depth):
        # Initialize temp value to inf and Directions.STOP since we want to get the min_value
        temp = float("inf"), Directions.STOP
        # list to keep track of nodes distances and their actions
        minlist= []
        #add the temp to minlist
        minlist.append(temp)
        # get all possible actions from the current state
        nextStates = gameState.getLegalActions(agentIndex)
        # loop through all the actions possible
        for nextState in nextStates:
            #If the value of getNumAgents() equals agentIndex+1 ie., lastghost
            if agentIndex + 1 == gameState.getNumAgents(): #exploring the lastghost
                #Get the maximum value of the successor states by passing agentIndex as 0 to send it to pacman
                minvalue = self.minimax(gameState.generateSuccessor(agentIndex, nextState), 0, depth + 1)
                #append the minvalue and the corresponding action to the minlist
                minlist.append((minvalue,nextState))
                #get the minimum value from the minlist and assign the minvalue to self.minvalue and the corresponding action to self.bestAction
                (self.minvalue, self.bestAction) =  min(minlist)
            else: #exploring the ghosts other than the last ghost
                # Get the minimum value of the successor states to send it to remaining ghosts
                minvalue = self.minimax(gameState.generateSuccessor(agentIndex, nextState), agentIndex + 1, depth)
                # append the minvalue and the corresponding action to the minlist
                minlist.append((minvalue, nextState))
                # get the minimum value from the minlist and assign the minvalue to self.minvalue and the corresponding action to self.bestAction
                (self.minvalue, self.bestAction) = min(minlist)
        #return the minvalue
        return self.minvalue

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
         # start from pacman at depth 0 and with alpha as -infinity and beta as infinity
        self.max_value(gameState, 0, 0, -float("inf"), float("inf"))
        # return the bestAction through which we can optimize the value for pacman using alphabeta pruning
        return self.bestActionforAlphabeta

    def alphabeta(self, gameState, agentIndex, depth,alpha, beta):
        # If the current gamestate is in winstates or we have to explored all the depths or if the current gamestate is in losestates
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            # If anyone of the above condition is satisfied return the evaluationfunction
            return self.evaluationFunction(gameState)
        # If the agentIndex is 0 it means we are exploring the Pacman
        if agentIndex == 0:
            # Since we are exploring the pacman we want to maximize the value it gets
            return self.max_value(gameState, agentIndex, depth,alpha, beta)
        # If the agentIndex is other than 0 it means we are exploring the ghosts
        else:
            # Since we are exploring the ghosts we want to minimize the value it gets
            return self.min_value(gameState, agentIndex, depth,alpha,beta)

    def max_value(self, gameState, agentIndex, depth, alpha, beta):
        # Initialize temp value to -inf and Directions.STOP since we want to get the max_value
        temp = (float("-inf"), Directions.STOP)
        # list to keep track of nodesdistances and their actions
        maxlist = []
        # add the temp to maxlist
        maxlist.append(temp)
        # get all possible actions from the current state
        nextStates = gameState.getLegalActions(agentIndex)
        # loop through all the actions possible
        for nextState in nextStates:
            # compute the cost it takes to reach the successor
            maxvalue = self.alphabeta(gameState.generateSuccessor(agentIndex, nextState), 1, depth,alpha,beta)
            # add the computed value and corresponding action to the maxlist
            maxlist.append((maxvalue, nextState))
            # get the maximum value from the maxlist and assign the maxvalue to self.maxvalueforAlphabeta and the corresponding action to self.bestActionforAlphabeta
            (self.maxvalueforAlphabeta, self.bestActionforAlphabeta) = max(maxlist)
            #If the value of maxvalueforAlphabeta >beta, there is no need to check child nodes, we can return the maxvalueforAlphabeta
            if(self.maxvalueforAlphabeta > beta):
                return self.maxvalueforAlphabeta
            #Set alpha value to max of maxvalueforAlphabeta and alpha Used in alphabeta pruning to reduce the amount of computation requried
            alpha = max(self.maxvalueforAlphabeta,alpha)
        # returns the max_value
        return self.maxvalueforAlphabeta

    def min_value(self, gameState, agentIndex, depth,alpha, beta):
        # Initialize temp value to inf and Directions.STOP since we want to get the min_value
        temp = float("inf"), Directions.STOP
        # #list to keep track of nodesdistances and their actions
        minlist = []
        # add the temp to minlist
        minlist.append(temp)
        # get all possible actions from the current state
        nextStates = gameState.getLegalActions(agentIndex)
        # loop through all the actions possible
        for nextState in nextStates:
            # If the value of getNumAgents() equals agentIndex+1 ie., lastghost
            if agentIndex + 1 == gameState.getNumAgents():  # exploring the lastghost
                # Get the maximum value of the successor states by passing agentIndex as 0 to send it to pacman
                minvalue = self.alphabeta(gameState.generateSuccessor(agentIndex, nextState), 0, depth + 1,alpha, beta)
                # append the minvalue and the corresponding action to the minlist
                minlist.append((minvalue, nextState))
                # get the minimum value from the minlist and assign the minvalue to self.minvalueforAlphabeta and the corresponding action to self.bestActionforAlphabeta
                (self.minvalueforAlphabeta, self.bestActionforAlphabeta) = min(minlist)
                # If the value of minvalueforAlphabeta < alpha, there is no need to check child nodes, we can return the minvalueforAlphabeta
                if (self.minvalueforAlphabeta < alpha):
                    return self.minvalueforAlphabeta
                # Set beta value to min of minvalueforAlphabeta and beta . Used in alphabeta pruning to reduce the amount of computation requried
                beta = min(beta, self.minvalueforAlphabeta)
            else:  # exploring the ghosts other than the remaining ghosts
                # Get the minimum value of the successor states to send it to remaining ghosts
                minvalue = self.alphabeta(gameState.generateSuccessor(agentIndex, nextState), agentIndex + 1, depth,alpha , beta)
                # append the minvalue and the corresponding action to the minlist
                minlist.append((minvalue, nextState))
                # get the minimum value from the minlist and assign the minvalue to self.minvalue and the corresponding action to self.bestAction
                (self.minvalueforAlphabeta, self.bestAction1) = min(minlist)
                # If the value of minvalueforAlphabeta < alpha, there is no need to check child nodes, we can return the minvalueforAlphabeta
                if (self.minvalueforAlphabeta < alpha):
                    return self.minvalueforAlphabeta
                # Set alpha value to max of minvalueforAlphabeta and beta Used in alphabeta pruning to reduce the amount of computation requried
                beta = min(beta, self.minvalueforAlphabeta)

        # return the minvalueforAlphabeta
        return self.minvalueforAlphabeta

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
        # return the bestAction through which we can optimize the value for pacman
        self.max_value(gameState,0,0)
        #return the best action possible for pacman
        return self.bestActionforExpectimax

    def expectimax(self, gameState, agentIndex, depth):
        # If the current gamestate is in winstates or we have to explored all the depths or if the current gamestate is in losestates
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            # If anyone of the above condition is satisfied return the evaluationfunction
            return self.evaluationFunction(gameState)
        # If the agentIndex is 0 it means we are exploring the Pacman
        if agentIndex == 0:
            # Since we are exploring the pacman we want to maximize the value it gets
            return self.max_value(gameState, agentIndex, depth)
        # If the agentIndex is other than 0 it means we are exploring the ghosts
        else:
            # Since we are exploring the ghosts we want to get expected value it gets
            return self.expecti_value(gameState, agentIndex, depth)

    def max_value(self, gameState, agentIndex, depth):
        # Initialize temp value to -inf and Directions.STOP since we want to get the max_value
        temp = (float("-inf"), Directions.STOP)
        # list to keep track of nodesdistances and their actions
        maxlist = []
        # add the temp to maxlist
        maxlist.append(temp)
        # get all possible actions from the current state
        nextStates = gameState.getLegalActions(agentIndex)
        # loop through all the actions possible
        for nextState in nextStates:
            # compute the cost it takes to reach the successor
            maxvalue = self.expectimax(gameState.generateSuccessor(agentIndex, nextState), 1, depth)
            # add the computed value and corresponding action to the maxlist
            maxlist.append((maxvalue, nextState))
            # get the maximum value from the maxlist and assign the maxvalue to self.maxvalueforExpectimax and the corresponding action to self.bestActionforExpectimax
            (self.maxvalueforExpectimax, self.bestActionforExpectimax) = max(maxlist)
        # returns the max_value
        return self.maxvalueforExpectimax

    def expecti_value(self, gameState, agentIndex, depth):
        #initialize averagescore to be zero
        averageScore = 0
        probability = 1.0 / len(gameState.getLegalActions(agentIndex))
        # get all possible actions from the current state
        nextStates = gameState.getLegalActions(agentIndex)
        # loop through all the actions possible
        for nextState in nextStates:
            # If the value of getNumAgents() equals agentIndex+1 ie., lastghost
            if agentIndex + 1 == gameState.getNumAgents():  # exploring the lastghost
                # Get the  value of the successor states by passing agentIndex as 0 to send it to pacman
                expectivalue =  self.expectimax(gameState.generateSuccessor(agentIndex, nextState), 0, depth + 1)
                averageScore =  averageScore + expectivalue

            else:  # exploring the ghosts other than the remaining ghosts
                # Get the minimum value of the successor states to send it to remaining ghosts
                expectivalue = averageScore + self.expectimax(gameState.generateSuccessor(agentIndex, nextState), agentIndex + 1, depth)
                averageScore = averageScore + expectivalue

        # return the minvalue
        return averageScore * probability


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Initialize score value to zero
      If the currentPosition of pacman has food increase the score
      Loop through all the food and find the minimum distance between the pacman and food. Take the reciprocal of the minimum dsitance between the pacman and the food.
      If the current food position we iterated through the loop is capsule position increase the score
      Loop through all the ghosts and find the minimum distance between the pacman and the ghost. If the distance<=2 check if the ghost is scared or not
      If the ghost is scared then increase the score .
      else decrease the score so that pacman moves away from that position.
      if the current pacman position is same as ghost position return infinity.
      else return the score + min(1/distance)
    """
    "*** YOUR CODE HERE ***"
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    currentGhostStates = currentGameState.getGhostStates()
    score = 0
    distance = float("inf")
    #if the current postion of pacman has food increase the score
    if currentFood[currentPos[0]][currentPos[1]]:
        score = score+10
    # loop through all the food
    for food in currentFood.asList():
        # find the distance between pacman and food
        distancebetweenPacmanAndFood = manhattanDistance(currentPos, food)
        # compute the minimum of the distances
        distance = min([distance, distancebetweenPacmanAndFood])
        #if the food in the capsules
        if food in currentGameState.getCapsules():
            #increment the score
            score = score + 150
    distance2 = float("inf")
    # number of foods left
    numberOfFoodsLeft = len(currentFood.asList())
    # loop through the ghosts
    for ghost in currentGhostStates:
        # find the distance between the pacman and the ghost
        distancebetweenPacmanAndGhost = manhattanDistance(currentPos, ghost.getPosition())
        # find the nearest ghost to the pacman
        distance2 = min([distance2, distancebetweenPacmanAndGhost])
        # if the distance between ghost and pacman < 1
        if (distance2 <= 1):  # ghost about to eat pacman
            if not ghost.scaredTimer:  # If the ghost isn't scared then decrease the score so that pacman runs away
                score = score - 1000
            else: #if the ghost is scared, then increase the score
                score = score + 2000
    #if the current position of pacman is same as ghost position
    if(currentPos == ghost.getPosition):
        #return -inf
        return float("-inf")
    return currentGameState.getScore() + score + (1.0 / distance) -2* numberOfFoodsLeft

# Abbreviation
better = betterEvaluationFunction
