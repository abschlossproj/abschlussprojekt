# -*- coding: utf-8 -*-


import numpy as np


N = 5000    # populationsize
k = 20     # figure of social interactions per day

adMatrix = np.zeros((N, N), dtype=bool)    # matrix which shows social contacts



def indexfilter_2(matrix, row):
    hv = np.where(np.sum(matrix[:,row+1:N], axis=0) < k)
    potCon = hv[0] + (row + 1)
    return potCon
    

for i in np.arange(N):    # loop for every row
    potCon = indexfilter_2(adMatrix, i)    # list with potentional new contacs per row
    addCon = k - adMatrix[i,].sum()      # additional contacs for k entries in a row  
    
    if addCon > 0 and len(potCon) > 0:
        newCon = min(addCon, len(potCon))  # new social contacts     ## HIER WAR FEHLER IN ANGABE K MUSS DURCH addCon ERSETZT WERDEN
        indizes = np.random.choice(potCon, newCon, replace=False)   # chooses random indices out of potential indices
        adMatrix[i, indizes] = True   
        adMatrix[indizes, i] = True   # transpose the matrix
        

np.save('adMatrix_2.npy', adMatrix)   # saves adMatrix
#np.load('adMatrix.npy')             # loads adMatrix

        
'''
Code braucht bei mir, Matthias: 
2:10

'''






