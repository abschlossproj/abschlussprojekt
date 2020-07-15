# -*- coding: utf-8 -*-
'''
In der adMatrix.npy hat (array([4983, 4998]),) weniger als k Einträge (mehr als k Einträge kein Problem)
Gleiches Problem bei kleineren k und N, Fehler taucht öfters auf

spuckt keinen Fehler aus, aber 
adMatrix.sum()-(5000*20) > 0
also müssten es wieder zu wenige Kontakte sein???

Es könnte sein, dass das "Rätsel" wie die Kontakte zu verteilen sind, am Ende nicht auflösbar ist und deshalb einige Felder leer bleiben
'''


import numpy as np

N = 5000   # populationsize 
k = 20     # figure of social interactions per day per person
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: k=5,10,20 -> eine große Schleife?

adMatrix = np.zeros((N, N), dtype=bool)    # matrix which shows social contacts


# Berechne einen Indexfilter für mögliche Kontakte in der jeweiligen Zeile
# Nur jene Indizes sind erlaubt, deren Spaltensumme kleiner k beträgt

def indexfilter_2(row, matrix=adMatrix):
    hv = np.where(np.sum(matrix[:,row+1:], axis=0) < k)
    potCon = hv[0] + (row + 1)
    return potCon

    
for i in np.arange(N):    # loop for every row
    potCon = indexfilter_2(i)    # list with potentional new contacs per row
    addCon = k - adMatrix[i,].sum()      # additional contacs for k entries in a row  

    if addCon > 0 and len(potCon) > 0:
        newCon = min(addCon, len(potCon))  # new social contacts     ## HIER WAR FEHLER IN ANGABE K MUSS DURCH addCon ERSETZT WERDEN
        indizes = np.random.choice(potCon, newCon, replace=False)   # chooses random indices out of potential indices
        adMatrix[i, indizes] = True   # obere Dreiecksmatrix der Kontakte
        adMatrix[indizes, i] = True   # um die Matrix symmetrisch zu machen

if (np.sum(adMatrix, axis=0) < k).any():
    print("Achtung: in adMatrix gibt Personen mit weniger als k Kontakten: ", np.where(np.sum(adMatrix, axis=1) != k) )
# Durch eine ungünstige Abfolge des Matrix Aufbaus, kann die Situation entstehen, dass nicht in jeder Zeile exakt k Kontakte möglich sind.

#Test, ob spurlos
print("Die Spur der Adjazenzmatrix ist: ", adMatrix.trace())

np.save('adMatrix_4.npy', adMatrix)   # saves adMatrix
#np.load('adMatrix.npy')             # loads adMatrix    

'''
Ist adMatrix für alle Tage konstant, oder ändern sich die Kontakte pro Tag?
In der Angabe steht nur "für jede Person konstant"
-> vllt als Funktion
'''



