'''
This script loads the .csv's from documentation_tables/, combines them into a single dataframe.
Some graphics are then generated to compare the scenarios and different interesting developments.
To that end, some more rows are generated out of the existing ones.
As scenarios the difference between k and p seems most interesting, so m is fixed mostly at 5.
To make only a single nice graphic, one scenario is chosen at random (the first or fourth one)
The graphics are saved to graphics/


To-do: Legende, Titel, Theme, Farben, Beschriftung
To-do: Abspeichern
to-do: mehrere m's mit layout abspeichern
to-do: dfs now also with more rows iso and levels S,M,L

geom_line häufig problematisch, wenn es statt vieler lines nur eine ausspuckt, die alles verscuht zu kombinieren -> geom_line(aes(group = Subject ))

of interest: differnce between iso and without iso?
capacity when too much severe cases

docs[docs.days==105] -> there are still D!!!! 105 not long enough!!!!! -> make it dynamically, espec. if there's an upcoming diff between with quarantine and w/o???

give some countries 'names' and characters, e.g. commonwealth, with a secluded AUS, a herd-immunity GBR and mixture of IRA. Then compare, and aggravate the cases.

https://www.nzz.ch/panorama/coronavirus-neuste-fallzahlen-in-der-schweiz-und-weltweit-ld.1542774?reduced=true
oder siehe screenshot zib - instagramm
'''

from plotnine import ggplot, aes, geom_line, geom_col, facet_grid,  scale_y_log10, geom_point, facet_wrap, geom_step, geom_boxplot, facet_wrap, geom_crossbar, coord_cartesian, coord_flip, geom_bar, ggsave, geom_tile, geom_smooth, geom_segment, geom_text, geom_hline, theme_bw, ylim, labs, scale_color_gradient, theme_set
import pandas as pd
import numpy as np
import math
import os
import datetime
#import glob
import matplotlib.pyplot as plt

output_directory = "graphics"
if not os.path.exists(output_directory) or not output_directory in os.listdir():
    os.mkdir(output_directory) 

# prepare a number for log_10, so that we don't get 'ugly' values under 1
def log10(x):
    if x>10:
        return x
    elif x>0:
        return 11
    else: #if x=0
        return 10 # 1 would be better, looks not good tho, and the base would look like zero
    
print('Expected runtime: XXmin')
starttime = datetime.datetime.now()
print('Start at:', starttime)
print('-'*80)
print('graphics are being generated... Do not press any key...')
print('-'*80)
'''
########### P copied from simul Script :/ -> is it even used?
k_l=[5,10,20]         # number of contacts, only relevant for saved adMatrix from that script
m_l = [1,5,10]        # ill people on day 1
p_l = [.1,.25,.5]     # infection rate
P = []
for k in k_l:
    for m in m_l:
        for p in p_l:
            P.append((k,m,p))
############
'''
files = os.listdir('documentation_tables') #lists all csv generated in simul script
docs = pd.DataFrame()

# combine all the tables into one dataframe 'docs'
#i=1
for x, y in enumerate(files):
    df = pd.read_csv(('documentation_tables' + '/' + files[x]), index_col=0) # Compatibility issues?
    #slice the parameters of the scenario from the filename
    df['k'] = int(y[21:23])
    df['m'] = int(y[25:27])
    df['p'] = int(y[29:31])
    if len(docs)==0:
        docs=df
    else:
        docs=pd.concat([docs, df], ignore_index = True) #to get an index with length 27*38
    #i+=1
    #if i>1:
    #    break

t = max(docs.days)

########################
# 1 Data manipulation   #
#######################



# Some nice simulations are chosen:
docm05 = docs[docs.m==5]
file = files[4] #random, choose later on a 'nice' one: k5, m1, p10
doc = pd.read_csv('documentation_tables/' + file , index_col=0)

#for it to work in a single graph, one probably needs k and p as factors not doubles
docm05_cp = docm05.copy()
docm05_cp['k'] = docm05.k.astype(str)
docm05_cp['p'] = docm05.p.astype(str)
doc_interest = docm05_cp[docm05_cp['days']<10]


# tägliche Neuinfektionen, vs Veränderung Infizierter vs Tote
D_chng = []; D_nw = []; R_nw = []; T_nw = []
for i in np.arange(len(doc)-1)+1:
    D_chng.append(doc.loc[i,"D"]-doc.loc[i-1,"D"])
    D_nw.append(doc.loc[i-1,"H"]-doc.loc[i,"H"])
    R_nw.append(doc.loc[i,"R"]-doc.loc[i-1,"R"])
    T_nw.append(doc.loc[i,"T"]-doc.loc[i-1,"T"])
    
doc_change = pd.DataFrame({'H': doc.loc[1:38,'H'], #normally 25 -> bug
                           'D': doc.loc[1:38,"D"],
                           'G': np.add(doc.loc[1:38,"H"],doc.loc[1:38,"R"]), #Genesene+Healthy
                           'D_change': D_chng, 
                           'D_new' :D_nw,
                           'D_new_c': np.add(np.add(R_nw,T_nw),D_nw),
                           'D_new_neg': np.negative(D_nw),
                           'R_new':R_nw,
                           'R_new_c':np.add(R_nw,T_nw),
                           'R_new_neg': np.negative(R_nw),
                           'days':doc.loc[1:38,'days'], 
                           'T':doc.loc[1:38,"T"],
                           'T_new':np.multiply(-1, T_nw),
                           'T_new_pos':T_nw,
                           'T_new_log': (np.log10(list(map(log10, T_nw)))),
                           'cumT':np.add(R_nw,T_nw)}) 

#cumsums
doc_c = doc.copy()
doc_c['D'] = doc_c['D']+doc_c['H']
doc_c['R'] = doc_c['R']+doc_c['D']
doc_c['T'] = doc_c['T']+doc_c['R']

# logaithmierte D und T
doc_logT = doc['T'].apply(lambda x: math.log(log10(x),10)) #sehr langsam :/
doc_logD = doc['D'].apply(lambda x: math.log(log10(x),10)) # -> np.log(x) (geht auch mit df/ser?!)
doc_logDT = pd.DataFrame((doc['days'], doc_logT, doc_logD)).T


#################
# 2 Plotting    #
################

# facet über p, k, m fix 5
g = ggplot(docm05, aes(x='days'))
g + geom_line(aes(y='T'))  + facet_grid(('k','p')) #in R not a tuple but ~
# interesting: for (20,50) there's less deads in total than vor (10,25)


# line-graphs, die die totalen Infizierten über verschiedenen p,k vergleichen
g + geom_point(aes(y=docm05.D, fill='p', size='k'))
g + geom_line(aes(y='D', color='k', fill='k')) + facet_wrap(('p','k'))

g_int = ggplot(doc_interest, aes(x='days',y='D')) 
g_int + geom_line(aes(colour='k')) + scale_y_log10() + facet_wrap('p')

g_int + geom_line(aes(colour='k',linetype="p")) + scale_y_log10()
#g_int + geom_point(aes(colour='k',shape="p")) 

'''
# ggplot(docm05, aes('days','D', colour='p')) + geom_line() + facet_wrap(('k')) #maybe works in R?
### workaround
docm05wide = docm05[['days', 'D', 'p','k']]
# I am too dumb to pivot:
df = docm05.iloc[:,[0,2,5,7]]
docm05k05 = df[df.k == 5][['days','D','p']]
docm05k10 = df[df.k == 10][['days','D','p']]
docm05k20 = df[df.k == 20][['days','D','p']]

.pivot( columns='D',values=['k','p'])
docm05wide = docm05.pivot(columns='p')
'''


# Zeit vs Anzahl HDTR
ggplot(doc, aes(x='days'))   + geom_line(aes(y='H')) \
                             + geom_line(aes(y="D")) \
                             + geom_line(aes(y="T")) \
                             + geom_line(aes(y="R")) 

# Zeit vs Anzahl -> transparent überlappendes Säulendiagramm
ggplot(doc, aes(x= "days")) \
            + geom_col(aes(y='H',fill=0),position='stack',alpha=0.5) \
            + geom_col(aes(y="D",fill=1),position='stack',alpha=0.5) \
            + geom_col(aes(y="R",fill=2),position='stack',alpha=0.5) \
            + geom_col(aes(y="T",fill=3),position='stack',alpha=0.5)

# "gestacktes" Säulendiagramm, sodass gut die Verhältnisse sichtbar sind
ggplot(doc_c, aes(x= "days")) \
    + geom_col(aes(y="T",fill=3),position='stack') \
    + geom_col(aes(y="R",fill=2),position='stack') \
    + geom_col(aes(y="D",fill=1),position='stack') \
    + geom_col(aes(y='H',fill=0),position='stack') 
            
ggplot(doc_logDT, aes(x='days'))   + geom_line(aes(y="D")) \
                             + geom_line(aes(y="T"))

ggplot(doc_change, aes(x='days'))  \
    + geom_col(aes(y="cumT"),fill='red',width=.6) \
    + geom_col(aes(y="D_new",alpha=.5)) \
    + geom_col(aes(y="R_new",width=.6)) \
    + geom_line(aes(y='G'))
    #+ geom_line(aes(y="D_change"))
    #+ geom_col(aes(y="D_change", col='sgR_new')) #<-könnte später interessant werden, wenn in Simulationen die Ansteckungsraten langsamer sind, also sich D ändert, weil Leute sterben (-), genesen (-) und sich anstecken (+) 

    #+ geom_line(aes(y="G",fill='3')) \
    #+ geom_line(aes(y="H")) \
ggplot(doc_change, aes(x='days'))  \
    + geom_col(aes(y="D_new_c", fill= 1), width=0.4) \
    + geom_col(aes(y='R_new_c', fill=2), width=0.4) \
    + scale_y_log10() \
    + geom_col(aes(y='T_new_log'),fill='red', width=0.4)

ggplot(doc_change, aes(x='days'))  \
    + geom_col(aes(y="D_new_c", fill= 1), width=0.4) \
    + geom_col(aes(y='R_new_c', fill=2), width=0.4) \
    + geom_point(aes(y='G'),fill='w') \
    + geom_col(aes(y='T_new_pos'),fill='red', width=0.4)

print('-'*80)
    print('Start at:', starttime)
    print('Fin.  at:', datetime.datetime.now())
    print('Graphics are saved at in folder %s' %output_directory)
    print("Done")
