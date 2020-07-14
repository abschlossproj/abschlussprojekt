# -*- coding: utf-8 -*-
'''
Problem:
in adMatrix finden sich Zeilen mit weniger als 20 Einträgen.
Es könnte aber in der Natur des Problems oder der Lösung liegen, dass nicht alle Personen 20 Kontakte haben können
'''

import numpy as np


N = 5000    # populationsize
k = 20     # figure of social interactions per day

adMatrix = np.zeros((N, N), dtype=bool)    # matrix which shows social contacts



def indexfilter_2(matrix, row):
    hv = np.where(np.sum(matrix[:,row+1:N], axis=0) < k)
    '''
    Ich glaube das kann nicht stimmen, da die Hälfte der kontakte nicht beachtet werden. 
    Reihe 0-20 kann mit dem Code ja die maximale Summe nicht erreichen, und so immer in potCon sein.
    '''
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






