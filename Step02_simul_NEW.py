'''
-*- coding: utf-8 -*-
This script should be run after Step01, the creation of the ad.matrix
In this file\'s directory needs to be adMatrix_k*.npy'
It then calculates all suggested scenarios with the given number of contacts, and freely choosable number of patient 0s and probability of infection
Expected runtime: 11min - matthias@matthias'
'''
import numpy as np
import pandas as pd
import datetime
import os
import itertools #loading animation
import threading #loading animation
import sys #loading animation
import time #loading animation

##### FOR TESTING, SET t
#t = int(input('Set t'))

# Global variables
N = 5000                        # populationsize
m = 5                           # ill people on day 1
p = 0.1                         # infection rate
mr = 2/3                        # mortality rate for S patients
x = 5                           # quarantine after x days
pCD = [80/100, 15/100, 5/100]   # probability vector to set course of disease
t = 50                          # simulation period (days)
tmin=10; tmax=16                # Duration of sickness
output_directory = "documentation_tables"
if not os.path.exists(output_directory) or not output_directory in os.listdir():
    os.mkdir(output_directory)  
done = False #loading animation

#loading animation
def loadingicon():
    for symb in itertools.cycle(['\\','|', '/', '-']):
        if done:
            break
        sys.stdout.write('\rsimulating scenario ' + symb)
        sys.stdout.flush() #to see the new spinning symbol at once, not after the loop's finished
        time.sleep(0.1)

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
    
def scenario(k,m,p):
    adMatrix = np.load('adMatrix_k'+str(k)+'.npy')      # loads adMatrix 
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
    data.loc[index, "dur"] = [np.random.randint(tmin, tmax) for i in index]     # sets predicted illness duration of ill people on day 1 
    data.loc[index, "CD"] = [diseasecourse() for i in index]                # sets disease course of ill people on day 1

    documentation = pd.DataFrame({          # documention of stati, people in isolation, course of disease for each day 
                                  "days": np.arange(t+1),
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
      
    filename_permutation = ('documentation_simul_k%s_m%s_p%s.csv' %(k,m,int(100*p)))
    filename_permutation = filename_permutation.replace('m1_','m01_').replace('m5_','m05_').replace('k5_','k05_')
    savestring = output_directory+'/'+filename_permutation # Compatibility with backslash?
    documentation.to_csv(savestring)
    sys.stdout.write(f'\rSimulation for the scenario completed and saved at: {savestring} \n') #\r to let the loading icon vanish from that line

print('Calculate all possible 27 scenarios by putting [any], or do you wish to run a specific scenario? ') 
print('For the latter, please put in: \n -the continued contacts per person -                              k = (5, 10, 20)\
                                      \n -the number of persons that start out infected -                  m = (1, 5, 10)\
                                      \n -the probability of transmission per contact and day in percent - p = (10, 25, 50):')

try:
    inp = input('k, m, p = ')
    k,m,p = tuple(int(x) for x in inp.split(","))
    p = p/100
    print(f'You chose k={k}, m={m} and p={p}')
    if not (k in [5,10,20]):
        print('k needs to be a value that has a pre-calculated adMatrix_k*.npy, that is in {5;10;20}')
        raise ValueError()
    else:
        #loading animation        
        done = False 
        thread = threading.Thread(target=loadingicon)
        thread.start() #concurrent running
        
        scenario(k,m,p)
        done = True
except:
    print('*'*60)
    print('Now all scenarios are being looped')
    print('*'*60)
    print('Start at:',datetime.datetime.now())
    
    # Create all permutations manually:
    P = []
    for k in [5,10,20]:
        for m in [1,5,10]:
            for p in [0.10,0.25,0.50]:
                P.append((k,m,p))
      
    for k,m,p in P:
        #loading animation
        done = False 
        thread = threading.Thread(target=loadingicon)
        thread.start()
        
        scenario(k,m,p)
        done = True
    
    print('Fin.  at:', datetime.datetime.now())
    print('Simulation for all', len(P), 'scenarios completed!\nSaved in '+output_directory)       
        
        
    
