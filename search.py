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

from re import L
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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    visited = set()
    path = []
    node = problem.getStartState()
    fringe.push((node, path))
    if problem.isGoalState(node):
        return []
    

    while True:
        if fringe.isEmpty():
            return []
        
        node, path = fringe.pop()
        visited.add(node)

        if problem.isGoalState(node):
            return path

        children = problem.getSuccessors(node)

        for child in children:
            if child[0] not in visited:
                child_path = list(path)
                child_path.append(child[1])
                fringe.push((child[0], child_path))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from searchAgents import CornersProblem                     # For implementing #5: CornersProblem
    if type(problem) is CornersProblem:
        cornersReached = problem.getCornersReached()
    visited = set()
    fringe = util.Queue()
    node = problem.getStartState()
    path = []
    fringe.push((node, path))

    while not fringe.isEmpty():
        node, path = fringe.pop()

        if node in visited:
            continue

        visited.add(node)

        if problem.isGoalState(node):
            return path

        if type(problem) is CornersProblem:                     # #5: CornersProblem
            if cornersReached != problem.getCornersReached():   # number of cornersReached has changed in the problem = found a corner
                visited.clear()                                 # Clear all visited nodes
                cornersReached = problem.getCornersReached()    # Match number of corners reached with the problem
                visited.add(node)                               # Add current corner to visited set
                fringe = util.Queue()                           # Reset queue
                fringe.push((node, path))                       # Reinsert current corner to the fringe that was just cleared

        children = problem.getSuccessors(node)
        for child, move, cost in children:
            if child not in visited:
                fringe.push((child, path + [move]))
    return list()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()               # ucs uses a PriorityQueue
    visited = set()                             # Create a set for visited nodes
    path = []                                   # Used to return the list of moves
    node = problem.getStartState()              # Get the Start node
    totalcost = problem.getCostOfActions(path)  # Cost of paths
    fringe.push((node, path), totalcost)        # Push start node to fringe
    
    if problem.isGoalState(node):               # If Start is the Goal node, then return empty path
        return []
    
    # Select cheapest paths
    while True:
        if fringe.isEmpty():
            return []
        
        node, path = fringe.pop()               # Returns 2 items
        visited.add(node)                       # Add node to visited set

        if problem.isGoalState(node):           # If popped node is the Goal
            return path

        children = problem.getSuccessors(node)  # Get children of node
        
        for child in children:
            if child[0] not in visited:         # Make sure child has not been visited
                child_path = list(path)         # Store all previous paths before reaching the child path
                child_path.append(child[1])     # Append the directions of the child path
                totalcost = problem.getCostOfActions(child_path) # Get total cost of child
                fringe.push((child[0], child_path), totalcost)
                # debugging

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = set()
    fringe = util.PriorityQueue()
    node = problem.getStartState()
    path = []
    fringe.push((node, path), 0)

    while not fringe.isEmpty():
        node, path = fringe.pop()

        if node in visited:
            continue

        visited.add(node)

        if problem.isGoalState(node):
            return path

        children = problem.getSuccessors(node)
        for child, move, stepCost in children:
            if child not in visited:
                nHeuristic = stepCost + problem.getCostOfActions(path) + heuristic(child, problem = problem)
                fringe.push(
                    (child, path + [move]), nHeuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
