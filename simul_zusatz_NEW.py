# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

N = 5000                        # populationsize
m = 5                           # ill people on day 1
p = 0.1                         # infection rate
mr = 2/3                        # mortality rate for S patients
x = 5                           # quarantine after x days
pCD = [80/100, 15/100, 5/100]   # probability vector to set course of disease
t = 50                          # simulation period (days)

adMatrix = np.load('adMatrix_5.npy')      



def diseasecourse():        # sets course of disease    # L=leicht, M=Mittel, S=Schwer 
    hv = np.nonzero(np.random.multinomial(1, pCD))[0]
    if hv == 0:
        return "L"
    elif hv == 1:
        return "M"
    elif hv == 2:
        return "S"
    
def doordie():              # determines wether S patients survive or die
    if np.random.binomial(1, mr) == True:
        return "T"
    else:
        return "R"
    
    
    

data = pd.DataFrame({       
                     "ID" : np.arange(N),   
                     "stati" : np.chararray(N),             # healthstatus, H=Health D=Disease T=Death R=Resistant
                     "day" : np.zeros(N),                   # days since infection
                     "dur" : np.zeros(N),                   # predicted illness duration
                     "iso" : np.zeros(N, dtype=bool),       # isolation
                     "CD"  : np.chararray(N)                # course of disease     # L=leicht, M=Mittel, S=Schwer 
                   })      
data["stati"] = 'H'     # sets health status on H

# choose m ill people on day 1 randomly
index = np.random.choice(N, m)
data.loc[index, "stati"] = 'D'
data.loc[index, "dur"] = [np.random.randint(10, 16) for i in index]     # sets predicted illness duration of ill people on day 1 
data.loc[index, "CD"] = [diseasecourse() for i in index]                # sets disease course of ill people on day 1


documentation = pd.DataFrame({          # documention of stati, people in isolation, course of disease for each day 
                              "H" : np.zeros(t+1),
                              "D" : np.zeros(t+1),
                              "R" : np.zeros(t+1),
                              "T" : np.zeros(t+1),
                              "Iso" : np.zeros(t+1),
                              "L" : np.zeros(t+1),
                              "M" : np.zeros(t+1),
                              "S" : np.zeros(t+1)
                            }) 
    
# documentation of "day zero"
documentation.loc[0, "H"] = N-m
documentation.loc[0, "D"] = m
documentation.loc[0, "L"] = len(data[data["CD"] == "L"])
documentation.loc[0, "M"] = len(data[data["CD"] == "M"])
documentation.loc[0, "S"] = len(data[data["CD"] == "S"])






for day in np.arange(t):    # loop for every day
    
    data.loc[data["stati"] == 'D', "day"] += 1      # duration of illness plus 1 day since infection
    data.loc[data["day"] == x, "iso"] = True        # isolates people after x days of illness
    
    crit = data[(data["day"] == data["dur"]) & (data["stati"] == 'D') & (data["CD"] == "S")]["ID"]      # S patients where illness is over            
    res  = data[(data["day"] == data["dur"]) & (data["stati"] == 'D') & (data["CD"] != "S")]["ID"]      # L and M patients where illness is over
   
    data.loc[crit, "stati"] = [doordie() for i in crit]     # status update S patients        
    data.loc[res, "stati"] = "R"                            # status update L, M patients
    data.loc[np.concatenate((crit, res)), "iso"] = False    # end of quarantine
    data.loc[np.concatenate((crit, res)), "CD"] = ""
    
    spreader = data[(data["stati"] == 'D') & (data["iso"] == False)]["ID"]          # ill people outside of quarantine on day t
    newInf = []         # indices of new infections on day t
    
    for i in spreader:
        contacts = np.nonzero(adMatrix[i])[0]       # social contacs of ill people 
        for j in contacts:                          
            if np.random.binomial(1, p) == True and data["stati"][j] == 'H':    # random decision wether infection or not
                newInf.append(j)  
                
    data.loc[newInf, "stati"] = 'D'     # status update new infections
    data.loc[newInf, "dur"] = [np.random.randint(10, 16) for i in newInf]   # sets predicted illness duration of new infections
    data.loc[newInf, "CD"] = [diseasecourse() for i in newInf]              # sets course of illness of new infections
    
    # update the documentation
    documentation.loc[day+1, "H"] = len(data[data["stati"] == 'H'])
    documentation.loc[day+1, "D"] = len(data[data["stati"] == "D"])
    documentation.loc[day+1, "R"] = len(data[data["stati"] == "R"])
    documentation.loc[day+1, "T"] = len(data[data["stati"] == "T"])
    documentation.loc[day+1, "Iso"] = np.sum(data["iso"])
    documentation.loc[day+1, "L"] = len(data[data["CD"] == 'L'])
    documentation.loc[day+1, "M"] = len(data[data["CD"] == 'M'])
    documentation.loc[day+1, "S"] = len(data[data["CD"] == 'S'])