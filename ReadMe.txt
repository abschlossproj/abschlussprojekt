This repository contains the Uebung 4 of 040971 UK Computational Statistics - University Vienna under Prof. Hudec and Dr. Sauerzopf
It is a joint work of:
Robin Kaggl
Manuel Schuller
Matthias Lang

There are three scripts to be run respectively in R or python:

Step01* creates a 5000x5000 matrix, with an empty diagonal.
There are randomly distributed 1's in it, so that each row counts k of them.
This matrix gets than saved to the directory the script is run in.

Step02* uses this matrix, some m and p, meaning the number of patient zeros and the probability of infection per contact per day,
and the following variables:
t = 105                         # simulation period (days) -> with 105 for every k,m,p all changes for everyscenario documented
N = 5000                        # populationsize from Step01
mr = 0.05                       # mortality rate
x = 5                           # quarantine after x days
pCD = [80/100, 15/100, 5/100]   # probability vector to set course of disease to either L, M or S
tmin=10; tmax=16                # the duration of sickness is uniformely distributed between these two values
The script then puts out tables documenting the fictious course of a virus in the population.

Step03* uses and modifies those tables giving as output enlightening graphics.
