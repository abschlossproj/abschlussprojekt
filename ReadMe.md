This repository contains the 
# Uebung 4 of 040971 UK Computational Statistics 
***
University Vienna under Prof. Hudec and Dr. Sauerzopf

It is a joint work of:
+ Robin Kaggl
+ Manuel Schuller
+ Matthias Lang
***
There are three scripts to be run respectively in R or python:

### Step01* 
Creates a 5000x5000 matrix, with an empty diagonal.
There are randomly distributed 1's in it, so that each row counts k of them.
Python: There are matrices saved in .npy format for k=[5,10,20]. It may be that for some of the last rows there are one or two '1' too few, as with the implemented algorithm there's no solution for these cases.
This matrix gets than saved to the directory the script is run in.

### Step02* 
Uses this matrix, some m and p, meaning the number of patient zeros and the probability of infection per contact per day,
and the following variables:
```
t = 120                         # simulation period (days) -> with 105 for every k,m,p all changes for everyscenario documented
N = 5000                        # populationsize from Step01
mr = 0.05                       # mortality rate
x = 5                           # quarantine after x days
pCD = [80/100, 15/100, 5/100]   # probability vector to set course of disease to either L, M or S
tmin=10; tmax=16                # the duration of sickness is uniformely distributed between these two values
```
The script then puts out tables documenting the fictious course of a virus in the population.
Python: If not specified otherwise by the user, the script will put out 27 tables for 3x3x3 combinations of k, m and p. Each table than has an entry for each day showing the number of healthy, infected, recovered and dead persons, as well as how bad they got hid by the virus, whether they are in quarantine and how long they are affected by the illness.

### Step03* 
Uses and modifies those tables giving as output enlightening graphics.
Python: Here are also some more values imputed from the given tables, e.g. the newly infected, the change in infected overall and the dead per day.
