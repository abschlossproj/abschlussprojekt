# -*- coding: utf-8 -*-


import numpy as np


N = 10 #5000 for testing less  # populationsize 
k = 3 #20 for testing less    # figure of social interactions per day per person
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
        adMatrix[i, indizes] = True   # obere Dreiecksmatrix der Kontakte
if (np.sum(adMatrix, axis=0) < k).any():
    print("Achtung: in adMatrix gibt Personen mit weniger als k Kontakten")
        adMatrix[indizes, i] = True   # um die Matrix symmetrisch zu machen
        

'''
In der adMatrix.npy hat (array([4983, 4998]),) weniger als k Einträge (mehr als k Einträge kein Problem)
Gleiches Problem bei kleineren k und N
Statt Debugging kleiner Workaround:
'''


if (np.sum(adMatrix, axis=0) != k).any():
    print("Achtung: in adMatrix gibt es Zeilensummen ungleich k. Workaround...")
####################################################################
    potCon = indexfilter_2(adMatrix, i)    # list with potentional new contacs per row
    addCon = k - adMatrix[i,].sum()      # additional contacs for k entries in a row  

    
# Durch eine ungünstige Abfolge des Matrix Aufbaus, kann die Situation entstehen, dass nicht in jeder Zeile exakt k Kontakte möglich sind.
    if addCon > 0 and len(potCon) > 0:
        newCon = min(addCon, len(potCon))  # new social contacts     ## HIER WAR FEHLER IN ANGABE K MUSS DURCH addCon ERSETZT WERDEN
        indizes = np.random.choice(potCon, newCon, replace=False)   # chooses random indices out of potential indices
        adMatrix[i, indizes] = True   # obere Dreiecksmatrix der Kontakte
        adMatrix[indizes, i] = True   # um die Matrix symmetrisch zu machen
#################################################################     

    if (np.sum(adMatrix, axis=0) != k).any():
        print("Achtung: in adMatrix gibt es Zeilensummen ungleich k")
    else:
        print("Workaround erfolgreich, adMatrix vollständig")
else:
    print("In adMatrix sind alle Zeilensummen gleich k")


#Workaround klappt auch nicht


#print(adMatrix)                      #for testing, also change N
#np.save('adMatrix_Mat.npy', adMatrix)   # saves adMatrix
#np.load('adMatrix.npy')             # loads adMatrix    




 















