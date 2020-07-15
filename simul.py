# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

N = 5000    # populationsize
m = 10      # # ill people on day 1 m=1,5,10
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: m=1,5,10 -> Umsetzung mit Schleife?
p = 0.5     # infection rate p=0.10, .25 ODER .50
mp = 0.05   # mortality rate
T = 100     # arbitrary endpoint of simulation
a=10;b=15   #Parameter der Krankheitsdauer gleichverteilt 10-15d
# status = ["H",0,"R","T"] #with an integer as the duration the subject is infected

adMatrix = np.load('adMatrix.npy')      # loads adMatrix

'''
Wählen Sie zufällig die am Tag 1 initial infizierten Personen aus
'''
adMatrix = np.load('adMatrix.npy')             # loads adMatrix 
#Speichert eine "Liste" aller Personen, mit status
#anderer Datentyp besser?
l = [] #np.arange(len(adMatrix))
N = len(adMatrix)-1 #vgl N aus altem Skript-1, population size, but as index

#bool <-> Der Zustand der Personen wird in den Diagonalelementen gespeichert
P0 = np.random.choice(N, m, replace=False)

#Liste der Personen, alle "H", nur m Personen "0"
for i in range(N):
    if i in P0:
        l += ["0"]
    else:
        l += ["H"]

'''
Vorgehen:
0. Checke, wie lange eine Person krank ist -> Status zu R oder T je nach m   -> aktualisiere l
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
1. status 2. theoretische Krankheitsdauer 3. aktuelle Krankheitsdauer (1. und 3. könnten zusammengefasst werden)
'''
# Jeder Person wird eine theoretische Krankheitsdauer zugewiesen
r = np.random.uniform(low=a,high=b,size=N+1) #Krankheitsdauer später runden
pd.DataFrame(data=[l,r], index=("status","theordur")).transpose()  
    
# Zufallsexperiment einer etwaigen Ansteckung

# Zufallsexperiment, ob am Ende der Ansteckung T oder R


















