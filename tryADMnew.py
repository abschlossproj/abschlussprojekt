# -*- coding: utf-8 -*-
'''
In der adMatrix.npy hat (array([4983, 4998]),) weniger als k Einträge (mehr als k Einträge kein Problem)
Gleiches Problem bei kleineren k und N, Fehler taucht öfters auf
Neue Funktion indexfilter_3 hat das Problem scheinbar behoben

if (np.sum(adMatrix, axis=0) < k).any():
    print("Achtung: in adMatrix gibt Personen mit weniger als k Kontakten")
spuckt keinen Fehler aus, aber 
adMatrix.sum()-(5000*20) > 0
also müssten es wieder zu wenige Kontakte sein???

Ich denke dass der erste Code vllt doch richtig war, bemerkenswerter Weise waren die Fehler immer in den letzten Zeilen:
Es könnte sein, dass das "Rätsel" wie die Kontakte zu verteilen sind, am Ende nicht auflösbar ist und deshalb einige Felder leer bleiben
'''

#Code wegen ewigen Loops noch nie ausgeführt

import numpy as np


N = 5000   # populationsize 
k = 20     # figure of social interactions per day per person
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: k=5,10,20 -> eine große Schleife?

adMatrix = np.zeros((N, N), dtype=bool)    # matrix which shows social contacts


# Berechne einen Indexfilter für mögliche Kontakte in der jeweiligen Zeile
# Nur jene Indizes sind erlaubt, deren Spaltensumme kleiner k beträgt

def indexfilter_3(row, matrix=adMatrix):
    #Da wir soweit mit einer Dreiecksmatrix arbeiten, gibt uns das ein array aller möglichen Personen in Kontakt mit der Zeile mit "False"
    potCon_f = np.concatenate(( np.where(matrix[:row,row] == False)[0], (np.where(matrix[row,row+1:] == False)[0] + row+1) ))
    #was ist mit der ersten und letzten Zeile? -> scheint zu funktionieren
    potCon = []
    for x in potCon_f:   #Das kann  man sicher schöner machen, ich steh auf dem Schlauch, dieser Loop dauert 15min aufwärts
        if  (matrix[:x,x].sum() + matrix[x,x+1:].sum()) < k:
            potCon.append(x)
    return potCon

    
for i in np.arange(N):    # loop for every row
    potCon = indexfilter_3(i)    # list with potentional new contacs per row
    addCon = k - adMatrix[i,].sum()      # additional contacs for k entries in a row  
    
# Durch eine ungünstige Abfolge des Matrix Aufbaus, kann die Situation entstehen, dass nicht in jeder Zeile exakt k Kontakte möglich sind.
    if addCon > 0 and len(potCon) > 0:
        newCon = min(addCon, len(potCon))  # new social contacts     ## HIER WAR FEHLER IN ANGABE K MUSS DURCH addCon ERSETZT WERDEN
        indizes = np.random.choice(potCon, newCon, replace=False)   # chooses random indices out of potential indices
        adMatrix[i, indizes] = True   # obere Dreiecksmatrix der Kontakte
        adMatrix[indizes, i] = True   # um die Matrix symmetrisch zu machen
if (np.sum(adMatrix, axis=0) < k).any():
    print("Achtung: in adMatrix gibt Personen mit weniger als k Kontakten")
        

np.save('adMatrix_Mat2.npy', adMatrix)   # saves adMatrix
#np.load('adMatrix.npy')             # loads adMatrix    





