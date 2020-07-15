# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

N = 5000    # populationsize
m = 10      # # ill people on day 1 m=1,5,10
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: m=1,5,10 -> Umsetzung mit Schleife?
p = 0.5     # infection rate p=0.10, .25 ODER .50
mp = 0.2 #for testing higher, normally .05 # mortality rate
T = 100     # arbitrary endpoint of simulation
a=10;b=15   #Parameter der Krankheitsdauer gleichverteilt 10-15d
# status = {"healtyh":"H","infected":"I","recovered":"R","dead":"T"} 

adMatrix = np.load('adMatrix.npy')      # loads adMatrix

'''
Wählen Sie zufällig die am Tag 1 initial infizierten Personen aus
'''
#Speichert eine "Liste" aller Personen, mit status
#anderer Datentyp besser?
l = [] #np.arange(len(adMatrix))
N = len(adMatrix) #vgl N aus altem Skript, population size

#bool <-> Der Zustand der Personen wird in den Diagonalelementen gespeichert
P0 = np.random.choice(N, m, replace=False)

#Liste der Personen, alle "H", nur m Personen "I"
for i in range(N):
    if i in P0:
        l += ["I"]
    else:
        l += ["H"]

'''
Vorgehen:
0. Checke, wie lange eine Person krank ist -> Status zu R oder T je nach mp, dur aktualisieren   -> aktualisiere l
1. Steckt eine Person einen seiner "H"-Kontakte mit Wahrscheinlichkeit p an? -> aktualisiere l
   Wie könnte man das lösen, ohne N*(N-1) Zufallsexperimente durchzuführen?
2. speichere l zum Tag i
3. loop -> Wann hört der Loop auf? Willkürlich

Eventuelle Probleme:
Es wird davon ausgegangen, dass zuerst alle genesen/versterben, dann sich angesteckt wird und von vorne
Die Krankeitsdauer wird also auch gerundet
'''

'''
Problem:
Krankheitsverlauf gleichverteilt -> muss also deterministisch bei Ansteckung determiniert werden, statt als Zufallsexperiment
-> eigentlich kann l schon initialisiert werden, und jeder Person eine theoretische Krankheitsdauer zugerechnet werden
-> 3 Spalten:
1. status 2. theoretische Krankheitsdauer 3. aktuelle Krankheitsdauer
'''
# Jeder Person wird eine theoretische Krankheitsdauer zugewiesen
r = np.random.uniform(low=a,high=b,size=N) #Krankheitsdauer später runden
d = np.zeros((N))
pers = pd.DataFrame(data=[l,r,d], index=("status","theordur","dur")).transpose()  
# Jede Zeile in pers und adMatrix entspricht der gleichen Person

########## loop should begin here ################

#0# Status ändern?

# Krankheitsende

#Zum Testen seien einige Personen schon lange krank:#
test = (1,3,5,6,34,1234,356,321,421,4998,4023)      #
pers.loc[test,["dur"]] = 15                         #
pers.loc[test[0],["dur"]] = 1                       #
pers.loc[test,["status"]] = "I"                     #
#####################################################
ind = (pers["theordur"] < pers["dur"]) & (pers["status"] ==  "I")
select = np.arange(N)[ind]    # in R I would use df[which()]
dec = np.random.choice(select, int(len(select)*mp), replace=False)
pers.loc[dec,["status"]] = "T"
# pers.loc[ind & pers["status"]!="T",["status"]] = "R" Why does this not work?
rec = set(select).difference(set(dec))
pers.loc[rec,["status"]] = "R"

#Krankheit dauert noch an
sic = pers["status"] == "I"
pers.loc[sic,["dur"]] += 1


#1# Zufallsexperiment einer etwaigen Ansteckung
'''
für jede Zeile der adjutanten Matrix jeden I schauen, wie viele der Kontake H sind
-> Ein Anteil p dieser Kontakte wird infiziert, diese werden in l festgehalten
Durch diese Methode wird sichergestellt, dass "der Erwartungswert für die druch diese Person neu infizierten 2,5 Personen [sei]".
'''


# Zufallsexperiment, ob am Ende der Ansteckung T oder R


















