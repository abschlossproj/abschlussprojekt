# -*- coding: utf-8 -*-


import numpy as np


N = 10 #5000 for testing   # populationsize 
k = 20     # figure of social interactions per day per person
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: k=5,10,20 -> eine große Schleife?

adMatrix = np.zeros((N, N), dtype=bool)    # matrix which shows social contacts


# Berechne einen Indexfilter für mögliche Kontakte in der jeweiligen Zeile
# Nur jene Indizes sind erlaubt, deren Spaltensumme kleiner k beträgt
def indexfilter_2(matrix, row):
    # Gibt ein array mit den Personen aus, die weniger als k Kontakte hatten:
    hv = np.where(np.sum(matrix[:,row+1:N], axis=0) < k)

    potCon = hv[0] + (row + 1) #array aller möglichen Personen, die infiziert werden könnten
    return potCon

    
for i in np.arange(N):    # loop for every row
    potCon = indexfilter_2(adMatrix, i)    # list with potentional new contacs per row
    addCon = k - adMatrix[i,].sum()      # additional contacs for k entries in a row  
    
# Durch eine ungünstige Abfolge des Matrix Aufbaus, kann die Situation entstehen, dass nicht in jeder Zeile exakt k Kontakte möglich sind.
    if addCon > 0 and len(potCon) > 0:
        newCon = min(addCon, len(potCon))  # new social contacts     ## HIER WAR FEHLER IN ANGABE K MUSS DURCH addCon ERSETZT WERDEN
        indizes = np.random.choice(potCon, newCon, replace=False)   # chooses random indices out of potential indices
        adMatrix[i, indizes] = True   
        # adMatrix[indizes, i] = True   # transpose the matrix -> was bringt das? Auf alle Fälle überflüssig adMatrix zweimal zu def.
        
print(adMatrix)                      #for testing, also change N
#np.save('adMatrix_tmp.npy', adMatrix)   # saves adMatrix
#np.load('adMatrix.npy')             # loads adMatrix

        
            




 















