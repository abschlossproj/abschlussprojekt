# -*- coding: utf-8 -*-

import numpy as np

N = 5000    # populationsize
m = 10      # # ill people on day 1
# unterschiedliche Szenarien sollen gerechnet werden. Vorschlag: m=1,5,10 -> Umsetzung mit Schleife?
p = 0.5     # infection rate
mp = 0.05   # mortality rate
#Parameter der Krankheitsdauer hier als function?

adMatrix = np.load('adMatrix.npy')      # loads adMatrix

