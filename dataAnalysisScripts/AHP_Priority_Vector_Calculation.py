import pandas as pd
import numpy as np

class AHP_Priority_Vector_Calculation():
    def __init__(self) -> None:
        self.dimensions = None
        self.answerMatrix = None
        self.synthesizedMatrix = None
        self.priorityVector = None
        pass

    def newAnswer(self):
        for col in self.answerMatrix.columns:
            self.answerMatrix[col].values[:] = 0
            
        for i in range(len(self.answerMatrix)):
            self.answerMatrix.iat[i, i] = 1
        self.priorityVector = None
        self.synthesizedMatrix = None
        self.priorityVector = None

    def initializeAnswerMatrix(self, dimensions:list):
        self.dimensions = dimensions
        n = len(dimensions)

        self.answerMatrix = pd.DataFrame(np.zeros((n, n)), index = dimensions, columns = dimensions)
        for i in range(n):
            self.answerMatrix.iat[i, i] = 1
        return self
    
    def setResponse(self, index:list, response):
        if (len(index) != 2):
            raise ValueError("Index should be a two-dimensional value")
        
        if (isinstance(index[0], int) and isinstance(index[1], int)):
            #if (self.answerMatrix.iat[index[0], index[1]] == 0):
            self.answerMatrix.iat[index[0], index[1]] = response
            
            #if (self.answerMatrix.iat[index[1], index[0]] == 0):
            self.answerMatrix.iat[index[1], index[0]] = 1/response

        if (isinstance(index[0], str) and isinstance(index[1], str)):
            #if (self.answerMatrix.at[index[0], index[1]] == 0):
            self.answerMatrix.at[index[0], index[1]] = response
            
            #if (self.answerMatrix.at[index[1], index[0]] == 0):
            self.answerMatrix.at[index[1], index[0]] = 1/response
        return self
    
    def setResponses(self, indices, responses):
        if (len(indices) != len(responses)):
            raise ValueError("The number of indices and responses does not match")
        for i in range(len(indices)):
            self.setResponse(indices[i],responses[i])
 
    def getSynthesizedMatrix(self):
        if self.synthesizedMatrix == None:
            self.synthesizedMatrix = self.answerMatrix/np.sum(self.answerMatrix, axis = 0)
        return self.synthesizedMatrix
    
    def getPriorityVector(self):
        if self.priorityVector is None:
            synthesizedMatrix = self.getSynthesizedMatrix()
            self.priorityVector = np.sum(synthesizedMatrix, axis=1) / len(synthesizedMatrix)
        return self.priorityVector
    
    def getWeightedSumMatrix(self):
        return np.sum(self.answerMatrix * np.array(self.priorityVector).reshape((1, len(self.priorityVector))), 
                      axis=1)
    
    def verifyConsistency(self, n = None, ri = None):
        if (n and n > 10 and ri == None):
            raise ValueError("Please enter the RI value")
        if (ri == None):
            ris = (0, 0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49)
            ri = ris[n]

        lambdaMax = np.sum(self.getWeightedSumMatrix() / self.priorityVector) / n
        ci = (lambdaMax - n) / (n - 1)
        return ci/ri

def ahpTextProcess(text:str):
    splitedText = text.strip().split()
    if ("equal" in text):
        return splitedText[0], splitedText[2], 1
    
    if ("slightly" in text):
        return splitedText[0], splitedText[-1], 3
    
    if ("strongly" in text):
        return splitedText[0], splitedText[-1], 7
    
    if ("absolutely" in text):
        return splitedText[0], splitedText[-1], 9
    
    return splitedText[0], splitedText[-1], 5

""" hhh = AHP_Weight_Calculation()
indices = (("A", "E"),
           ("B", "A"), ("B", "C"), ("B", "E"), 
           ("C", "A"),("C", "E"), 
           ("D", "A"), ("D", "B"), ("D", "C"), ("D", "E"))
responses = (2,
             3, 2, 4, 
             2, 3,
             6, 2, 3, 7)
hhh.initializeAnswerMatrix(("A", "B", "C", "D", "E")).setResponses(indices, responses)
hhh.getPriorityVector()
print(hhh.verifyConsistency(5)) """