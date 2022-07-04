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
import sys
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        print(bestScore)
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
        MAX =-99999
        powerup = -MAX
        toCap = 10
        
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsules = currentGameState.getCapsules()
        score = successorGameState.getScore()
        
        evalDict = {
      
            
            
        }
        foods = newFood.asList()

        if(len(capsules)> 0):
            for cap in capsules:
                distCap = util.manhattanDistance(newPos,cap)
                if(distCap == 0):
                    score = powerup
                else:
                    score -= distCap*40
        ghostDists = []
        foodDists =[]
        for ghost in newGhostStates:
            pos = ghost.getPosition()
            ghostDist = util.manhattanDistance(newPos, pos)
            ghostDists.append(ghostDist)
            if ghost.scaredTimer > 0:
                score -= ghostDist
                        
        for food in foods:
            pos = food
            foodDist = util.manhattanDistance(newPos, pos)
            foodDists.append(foodDist)
        
        """
        if(len(foods) > 0):
            successorGameState.getScore -= min(foodDists)
            """


       
            
            

            
        
        if 0 in  ghostDists:
            ghostDists = MAX
        else:
            ghostDist = min(ghostDists)
        foodDist = min(foodDists)
        score += ghostDist/len(foods)
        score -= foodDist

   
  
              
            
            
            
        """
        TODO IMPLEMENT WITH SCARED TIMES TOMORROW. OTHERWISE, DONE!   
        """ 
        return score

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maximizer(gameState, depth):
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), "Stop"
            legalActions = gameState.getLegalActions()
            value = float('-inf')
            bestMove = "Stop"
            for action in legalActions:
                val = max(value, minimizer(gameState.generateSuccessor(0, action), 1, depth))
                if val > value:
                    value = val
                    bestMove = action
            return value, bestMove

        def minimizer(gameState, a, depth):
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            value = float('inf')
            legalActions = gameState.getLegalActions(a)
            agents = gameState.getNumAgents()
            if a == agents - 1:
                for action in legalActions:
                    val = min(value, maximizer(gameState.generateSuccessor(a, action), depth + 1)[0])
                    if val < value:
                        value = val
            else:
                for action in legalActions:
                    val = min(value, minimizer(gameState.generateSuccessor(a, action), a + 1, depth))
                    if val < value:
                        value = val
            return value

        minimax = maximizer(gameState, 0)[1]
        return minimax

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # legalMoves = gameState.getLegalActions()
        # print(legalMoves)

        # initial call
        bestMove = ''
        alpha = -abs(sys.maxsize)
        beta = sys.maxsize
        for action in gameState.getLegalActions(self.index):
            maxEval = -abs(sys.maxsize)
            bestValue = self.minimax(gameState.generateSuccessor(self.index, action), self.depth-1, alpha, beta, self.index)
            if bestValue > maxEval:
                maxEval = bestValue
                bestMove = action
            alpha = max(alpha, bestValue)
        return bestMove
    
    """
    a recursive minimax function with pruning capabilities
    Returns the best score that can be achieved.

    TODO its unfinished yet
    """
    def minimax(self, futureState, depth, alpha, beta, agent):
        if agent == self.index and depth > 0:
            print(futureState)
            print('position: ' + str(futureState.getPacmanPosition()))
            print('depth: ' + str(depth))
            print('alpha: ' + str(alpha))
            print('beta: ' + str(beta))
            print('agent: ' + str(agent))

        # if the depth is 0 or game is over
        if depth == 0 or futureState.isLose() or futureState.isWin():
            return self.evaluationFunction(futureState)

        # if the agent being evaluated is the last agent, decrement the depth
        if agent == (futureState.getNumAgents() - 1):
            depth = depth - 1
        
        if agent == 0:  # agent 0 is Pacman, which uses the maximizer
            maxEval = -abs(sys.maxsize)
            for action in futureState.getLegalActions(agent):
                print('action 0: ' + action)
                print('\n')
                eval = self.minimax(futureState.generateSuccessor(agent, action), depth, alpha, beta, ((agent+1) % futureState.getNumAgents()))
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:           # agent > 0 are Ghosts, uses the minimizer
            minEval = sys.maxsize
            for action in futureState.getLegalActions(agent):
                # print('action %d: %s' % (agent, action))
                # print('\n')
                eval = self.minimax(futureState.generateSuccessor(agent, action), depth, alpha, beta, ((agent+1) % futureState.getNumAgents()))
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
