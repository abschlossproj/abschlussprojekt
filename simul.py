# -*- coding: utf-8 -*-

import numpy as np

N = 5000    # populationsize
m = 10      # # ill people on day 1 m=1,5,10
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: m=1,5,10 -> Umsetzung mit Schleife?
p = 0.5     # infection rate p=0.10, .25 ODER .50
mp = 0.05   # mortality rate
# status = ["H",0,"R","T"] #with an integer as the duration the subject is infected
#Parameter der Krankheitsdauer hier als function? #gleichverteilt 10-15d

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
Am Tag 1 und an jeden folgenden Tag: 
• Führen Sie für jeden Kontakt einer jeden Person eine Zufallsexperiment aus, um eine etwaige Ansteckung zu bestimmen. Nur aktuell infizierte Personen können ansteckend sein. Nur gesunde Personen, die noch nicht infiziert waren können angesteckt werden. 
• Bei mehreren Kontakten mit Infizierten steigt die Wahrscheinlichkeit einer Ansteckung 
• Dokumentieren Sie den zeitlichen Verlauf der Gesunden, Infizierten, Genesenen und Verstorbenen.
'''


