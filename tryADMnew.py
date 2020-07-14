# -*- coding: utf-8 -*-


import numpy as np


N = 1000 #5000 for testing less  # populationsize 
k = 6 #20 for testing less    # figure of social interactions per day per person
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: k=5,10,20 -> eine große Schleife?

adMatrix = np.zeros((N, N), dtype=bool)    # matrix which shows social contacts


# Berechne einen Indexfilter für mögliche Kontakte in der jeweiligen Zeile
# Nur jene Indizes sind erlaubt, deren Spaltensumme kleiner k beträgt

def indexfilter_3(row, matrix=adMatrix):
    #Da wir soweit mit einer Dreiecksmatrix arbeiten, gibt uns das ein array aller möglichen Personen in Kontakt mit der Zeile mit "False"
    potCon = np.concatenate(( np.where(matrix[:row,row] == False)[0], (np.where(matrix[row,row+1:] == False)[0] + row+1) ))
    #was ist mit der ersten und letzten Zeile? -> scheint zu funktionieren
    return potCon

    
for i in np.arange(N):    # loop for every row
    potCon = indexfilter_2(i)    # list with potentional new contacs per row
    addCon = k - adMatrix[i,].sum()      # additional contacs for k entries in a row  
    
# Durch eine ungünstige Abfolge des Matrix Aufbaus, kann die Situation entstehen, dass nicht in jeder Zeile exakt k Kontakte möglich sind.
    if addCon > 0 and len(potCon) > 0:
        newCon = min(addCon, len(potCon))  # new social contacts     ## HIER WAR FEHLER IN ANGABE K MUSS DURCH addCon ERSETZT WERDEN
        indizes = np.random.choice(potCon, newCon, replace=False)   # chooses random indices out of potential indices
        adMatrix[i, indizes] = True   # obere Dreiecksmatrix der Kontakte
        #adMatrix[indizes, i] = True   # um die Matrix symmetrisch zu machen

if (np.sum(adMatrix, axis=0) < k).any():
    print("Achtung: in adMatrix gibt Personen mit weniger als k Kontakten")
        

'''
In der adMatrix.npy hat (array([4983, 4998]),) weniger als k Einträge (mehr als k Einträge kein Problem)
Gleiches Problem bei kleineren k und N, Fehler taucht öfters auf
Statt Debugging kleiner Workaround:
'''

''' Workaround klappt noch nicht

if (np.sum(adMatrix, axis=0) != k).any():
    print("Achtung: in adMatrix gibt es Zeilensummen ungleich k. Workaround...")
########## Code von oben, klappt auch nicht########################
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


'''


#print(adMatrix)                      #for testing, also change N
#np.save('adMatrix_Mat.npy', adMatrix)   # saves adMatrix
#np.load('adMatrix.npy')             # loads adMatrix    




 















