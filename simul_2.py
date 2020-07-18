# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

N = 5000    # populationsize
m = 10      # # ill people on day 1
p = 0.1     # infection rate
mr = 0.05   # mortality rate

adMatrix = np.load('adMatrix.npy')      # loads adMatrix

data = pd.DataFrame({       
                     "ID" : np.arange(N),   
                     "stati" : np.chararray(N),     # healthstatus of each person   # H=Health, D=Disease, T=Death, R=Resistant
                     "day" : np.zeros(N),           # days since infection
                     "dur" : np.zeros(N)            # predicted illness duration
                   })      
data["stati"] = 'H'     # sets health status on H

# choose #m ill people on day 1 randomly
index = np.random.choice(N, m)
data.loc[index, "stati"] = 'D'
for i in index:                     # sets predicted illness duration of ill people on day 1 
    data.loc[i, "dur"] = np.random.randint(10, 16)



t = 20      # days of simulation

documentation = pd.DataFrame({          # documention of stati for each day 
                              "H" : np.zeros(t+1),
                              "D" : np.zeros(t+1),
                              "R" : np.zeros(t+1),
                              "T" : np.zeros(t+1)     
                            }) 
documentation.loc[0, "H"] = N-m
documentation.loc[0, "D"] = m

for day in np.arange(t):    # loop for every day
    
    data.loc[data["stati"] == 'D', "day"] += 1      # duration of illnes plus 1 day since infection
    
    crit = data[(data["day"] == data["dur"]) & (data["stati"] == 'D')]["ID"]    # indices where illness is over / days since infection = predicted illness duration
    for i in crit:          # resistant/dead + status update
        if np.random.binomial(1, mr) == False:
            data.loc[i, "stati"] = 'R'
        else:
            data.loc[i, "stati"] = 'T'
    
    ill = data[data["stati"] == 'D']["ID"]          # list of ill people on day t
    newInf = []         # indices of new infections on day t
    
    for i in ill:
        contacts = np.nonzero(adMatrix[i])[0]       # social contacs of ill people 
        for j in contacts:                          
            if np.random.binomial(1, p) == True and data["stati"][j] == 'H':    # random decision wether infection or not
                newInf.append(j)  
                
    data.loc[newInf, "stati"] = 'D'     # status update new infections
    for i in newInf:
        data.loc[i, "dur"] = np.random.randint(10,16)   # sets predicted illness duration of new infections
    
    # update the documentation
    documentation.loc[day+1, "H"] = len(data[data["stati"] == 'H'])
    documentation.loc[day+1, "D"] = len(data[data["stati"] == "D"])
    documentation.loc[day+1, "R"] = len(data[data["stati"] == "R"])
    documentation.loc[day+1, "T"] = len(data[data["stati"] == "T"])
    
    
    
    
    
    
    
    
    
    
