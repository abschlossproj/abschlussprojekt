# -*- coding: utf-8 -*-


import numpy as np


N = 5000    # populationsize
k = 20     # figure of social interactions per day per person
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: k=5,10,20 -> eine große Schleife?

adMatrix = np.zeros((N, N), dtype=bool)    # matrix which shows social contacts


# Berechne einen Indexfilter für mögliche Kontakte in der jeweiligen Zeile
# Nur jene Indizes sind erlaubt, deren Spaltensumme kleiner k beträgt
def indexfilter_2(matrix, row):
    # Gibt ein array mit den Personen aus, die weniger als k Kontakte hatten
    hv = np.where(np.sum(matrix[:,row+1:N], axis=0) < k)

    #Berechnen der erfolderlichen neuen Kontakte, um auf k zu kommen
    #potCon = hv[0] + (row + 1) #verstehe ich nicht, das spuckt doch ein array aus!?
    potCon = k - np.sum(matrix[:,row+1:N], axis=0) # evlt 0, könnte auch für Konstruktion von hv verwendet werden
    return potCon

    

for i in np.arange(N):    # loop for every row
    potCon = indexfilter_2(adMatrix, i)    # list with potentional new contacs per row
    addCon = k - adMatrix[i,].sum()      # additional contacs for k entries in a row  
    
    if addCon > 0 and len(potCon) > 0:
        newCon = min(addCon, len(potCon))  # new social contacts     ## HIER WAR FEHLER IN ANGABE K MUSS DURCH addCon ERSETZT WERDEN
        indizes = np.random.choice(potCon, newCon, replace=False)   # chooses random indices out of potential indices
        adMatrix[i, indizes] = True   
        adMatrix[indizes, i] = True   # transpose the matrix
        

np.save('adMatrix.npy', adMatrix)   # saves adMatrix
#np.load('adMatrix.npy')             # loads adMatrix

        
            




 















