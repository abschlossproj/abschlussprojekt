# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:15:21 2020
@author: Manuel Schuller
"""

import numpy as np
import random as random


N = 500    # populationsize
k = 5     # figure of social interactions/day

adMatrix = np.zeros((N, N), dtype=bool)    # matrix which mirrors social contacts




def filterindex(matrix, row):    # filters column-indizes for potential new social contacts
    potnewCon = []        
    for j in list(range(i+1, N)): 
        if sum(matrix[:, j]) < k:
            potnewCon.append(j) 
    return potnewCon


def newentries(matrix, row):    # calculates additional social contacts for k entries in a row
    addCon = k - sum(matrix[row,])
    return addCon


def sample(row, potnewCon, newCon):     # draws #newCon objects out of potnewCon without replacement
    indizes = random.sample(potnewCon, newCon)    
    return indizes  
    

def transpose(matrix):      # transposes upper triangle matrix to lower triangle matrix
    i_lower = np.tril_indices(N, -1)
    matrix[i_lower] = matrix.T[i_lower]
    return matrix


for i in list(range(N)):    # every row
    potnewCon = filterindex(adMatrix, i)    # list with potentional new contacs per row
    addCon = newentries(adMatrix, i)        # additional contacs for k entries in a row  

    if addCon > 0 and len(potnewCon) > 0:
        newCon = min(k, len(potnewCon))  # new social contacts
        indizes = sample(i, potnewCon, newCon)
        adMatrix[i, indizes] = True
            
adMatrix = transpose(adMatrix)



    



































