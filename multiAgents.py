from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
 


    def getAction(self, gameState):
       
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
      
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

       
        scr=successorGameState.getScore()
        food_d=newFood.asList()

        for i in food_d:
		        prey_distance = util.manhattanDistance(i,newPos)
		        if (prey_distance)!=0:
        		        scr=scr+(1.0/prey_distance)
		 
        for ghost in newGhostStates:
		        hallowen_pos=ghost.getPosition()
		        hallowen_Dist = util.manhattanDistance(hallowen_pos,newPos)
		        if (abs(newPos[0]-hallowen_pos[0])+abs(newPos[1]-hallowen_pos[1]))>1:	
			             scr=scr+(1.0/hallowen_Dist)
        return scr

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
   

    def getAction(self, gameState):
     
        agents_count = gameState.getNumAgents()
        distance = self.depth * agents_count
        
        self.getAction1(gameState,distance,agents_count)
        return self.action1
        util.raiseNotDefined()
    
    def getAction1(self,gameState,distance,agents_count):
        maximumfunction = list()
        minimumfunction = list()
        if gameState.isWin() or gameState.isLose():
		        return self.evaluationFunction(gameState)
                
        if distance > 0:
		        if distance%agents_count ==0:
			            agent_no = 0
				
		        else: 
			           agent_no = agents_count-(distance%agents_count)
		
		        actions = gameState.getLegalActions(agent_no)
		        for action in actions:
			            successorGameState = gameState.generateSuccessor(agent_no,action)
			 
			            if agent_no == 0: 
				                maximumfunction.append((self.getAction1(successorGameState,distance-1,agents_count), action))			
				                maximum = max(maximumfunction) 
				                self.maximum_value = maximum[0]
				                self.action1=maximum[1]	
				
			            else:	
				                minimumfunction.append((self.getAction1(successorGameState,distance-1,agents_count), action))			
				                minimum = min(minimumfunction)
				                self.minimum_value = minimum[0]
			
		        if agent_no == 0:
			            return self.maximum_value
		        else:
			            return self.minimum_value
                        
        else:
		        return self.evaluationFunction(gameState) 

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
   

    def getAction(self, gameState):
      
        
        def AB(gameState,agent,depth,a,b):
            result = []

            if not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState),0

            if depth == self.depth:
                return self.evaluationFunction(gameState),0

            if agent == gameState.getNumAgents() - 1:
                depth += 1


            if agent == gameState.getNumAgents() - 1:
                next_A = self.index

            else:
                next_A = agent + 1

            for action in gameState.getLegalActions(agent):
                if not result: 
                    next_Value = AB(gameState.generateSuccessor(agent,action),next_A,depth,a,b)

                    result.append(next_Value[0])
                    result.append(action)

                    if agent == self.index:
                        a = max(result[0],a)
                    else:
                        b = min(result[0],b)
                else:

                    if result[0] > b and agent == self.index:
                        return result

                    if result[0] < a and agent != self.index:
                        return result

                    previous_Value = result[0] 
                    next_Value = AB(gameState.generateSuccessor(agent,action),next_A,depth,a,b)

                    if agent == self.index:
                        if next_Value[0] > previous_Value:
                            result[0] = next_Value[0]
                            result[1] = action
                            a = max(result[0],a)

                    else:
                        if next_Value[0] < previous_Value:
                            result[0] = next_Value[0]
                            result[1] = action
                            b = min(result[0],b)
            return result

        return AB(gameState,self.index,0,-float("inf"),float("inf"))[1]

        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
  

    def getAction(self, gameState):
      
        agents_co = gameState.getNumAgents()
        d1 = self.depth * agents_co
        self.getAction1(gameState,d1,agents_co)
        return self.action1
        util.raiseNotDefined()

    def getAction1(self,gameState,d1,agents_co):
	    maximum_function = list()
	    minimum_function = list()
	    if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
			
	    if d1 > 0:
                if d1%agents_co ==0:
                 agentno = 0
                else:agentno = agents_co-(d1%agents_co)
                actions = gameState.getLegalActions(agentno)
                for action in actions:
                 successorGameState = gameState.generateSuccessor(agentno,action)
                 
                 if agentno == 0:
                  maximum_function.append((self.getAction1(successorGameState,d1-1,agents_co), action))
                  maximum = max(maximum_function)
                  self.maximum_value = maximum[0]
                  self.action1=maximum[1]
                 else:
                  minimum_function.append((self.getAction1(successorGameState,d1-1,agents_co), action))
                  A = 0.0
                  for i in minimum_function:
                   A += minimum_function[minimum_function.index(i)][0]
                  A /= len(minimum_function) 
                  self.Avg_val = A
                if agentno == 0:
                        return self.maximum_value
                else:
                 return self.Avg_val
	
	    else:
             return self.evaluationFunction(gameState) 
             util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
 
    foodDst = 0
    for food in newFood.asList():
        dist = manhattanDistance(food, newPos)
        #print ('dist', dist)
        foodDst += dist
    
    Pacman_score = 0
    if len(newFood.asList()) == 0:
        Pacman_score = 1000000
    
    hallowen_Score = 0
    if newScaredTimes[0] > 0:
             hallowen_Score += 100.0
    for state in newGhostStates:
        dist = manhattanDistance(newPos, state.getPosition())
        if state.scaredTimer == 0 and dist < 3:
            hallowen_Score -= 1.0 / (3.0 - dist);
        elif state.scaredTimer < dist:
            hallowen_Score += 1.0 / (dist)
    
    Pacman_score += 1.0 / (1 + len(newFood.asList())) + 1.0 / (1 + foodDst) + hallowen_Score + currentGameState.getScore()
    
    return Pacman_score;
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
