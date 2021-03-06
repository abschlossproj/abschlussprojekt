This repository contains the python scripts and outputs of
# Uebung 4 of 040971 UK Computational Statistics 

You may find the version **ported to R [here](https://github.com/abschlossproj/Abschluss-in-R)**
***
24.08.2020

University Vienna under Prof. Hudec and Dr. Sauerzopf

It is a joint work of:
+ Robin Kaggl
+ Manuel Schuller
+ Matthias Lang
***
Run `start.py` to run the whole simulation and generate all outputs, or each step on its own.

### Step 1
Creates a 5000x5000 matrix, with an empty diagonal.
There are randomly distributed 1's in it, so that each row counts k of them.
There are matrices for k=[5,10,20]. It may be that for some of the last rows there are one or two '1' too few, as with the implemented algorithm there's no solution for these cases.
This matrix gets than saved to the directory the script is run in, either in.npy or .rds format

### Step 2
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

**The additional tasks are done here, but not fully implemented:**
That means that in Step 2 the model includes the severity of the infection as well as quarantine and isolation measures. Only a fraction of those at risk with a severe infection die. That is not fully represented/visualized in Step 3.

The additional tasks are partly implemented in `Step02_simul.py`, and full in `Step02_simul_NEW.py`. The latter may not work fully with Step 3.

### Step 3 
Uses and modifies those tables giving, as output enlightening graphics.
THere are also some more values imputed from the given tables, e.g. the newly infected, the change in infected overall and the dead per day.

One example graphic is given below, the other outputs are already saved in `graphics` for ease of use.

![example output](graphics/ZIB-like.png)

The plots are inspired by the Grammar of Graphics [^1], using the packages plotnine and ggplot2 so both outputs for the respective programming languages look alike.

[^1]: Wickham, Hadley. “A Layered Grammar of Graphics.” Journal of Computational and Graphical Statistics 19, no. 1 (January 2010): 3–28. https://doi.org/10.1198/jcgs.2009.07098.


