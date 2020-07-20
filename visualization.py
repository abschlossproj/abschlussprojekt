'''
Es gibt "plotnine" für python, das hat fast die gleiche Grammatik wie ggplot2 für R.

pip install plotnine

https://plotnine.readthedocs.io/en/stable/index.html

To-do: Legende, Titel, Theme, Farben, Beschriftung
To-do: Abspeichern als eine daten (layout), Export mit dynamischen Namen je nach Szenario
To-do: als Loop Input und Output Files -> same für simul_2.py, um die verschiedenen Szenarien durchlaufen zu lassen
To-do: letzte Graphik noch skizzieren
To-do: maybe shorten the datatables, when theres a boring "tail"
'''

#to-do: documentation Matrix aus simul_2.py abspeichern und hier laden

from plotnine import ggplot, aes, geom_line, geom_col, facet_grid
import pandas as pd
import numpy as np
import math
import os


########### P copied from simul Script :/ -> is it even used?
k_l=[5,10,20]         # number of contacts, only relevant for saved adMatrix from that script
m_l = [1,5,10]        # ill people on day 1
p_l = [.1,.25,.5]     # infection rate
P = []
for k in k_l:
    for m in m_l:
        for p in p_l:
            P.append((k,m,p))

files = os.listdir('documentation_tables')
docs = pd.DataFrame()
#i=1
for i, y in enumerate(files):
    df = pd.read_csv(('documentation_tables' + '/' + files[i]), index_col=0) # Compatibility issues?
    #slice the parameters of the scenario from the filename
    df['k'] = int(y[21:23])
    df['m'] = int(y[25:27])
    df['p'] = int(y[29:31])
    if len(docs)==0:
        docs=df
    else:
        docs=pd.concat([docs, df], ignore_index = True)
    #i+=1
    #if i>1:
    #    break

        
        
# facet über p, k, m,mr fix
 '''todo'''

# line-graphs, die die totalen Infizierten über verschiedenen p,k vergleichen
docm05 = docs[docs.m==5]
g = ggplot(docm05, aes(x='days'))
g + geom_line(aes(y='T')) + facet_grid(('k','p')) #in R not a tuple but ~


#docs[(docs.k==20)&(docs.m==10)&(docs.p==25)]

############################
'''

Below was before simul got looped

'''
###########################

file = files[4] #random, choose later on a 'nice' one

doc = pd.read_csv(file , index_col=0)

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



#docmelted = pd.melt(doc, id_vars=['days'], value_vars=['H','D','R','T'])
#docmelted
#ggplot(docmelted) + geom_bar(aes(fill=docmelted[docmelted["variable"]=="H"]))

# "gestacktes" Säulendiagramm, sodass gut die Verhältnisse sichtbar sind
#cumsums
doc_c = doc.copy()
doc_c['D'] = doc_c['D']+doc_c['H']
doc_c['R'] = doc_c['R']+doc_c['D']
doc_c['T'] = doc_c['T']+doc_c['R']
ggplot(doc_c, aes(x= "days")) \
    + geom_col(aes(y="T",fill=3),position='stack') \
    + geom_col(aes(y="R",fill=2),position='stack') \
    + geom_col(aes(y="D",fill=1),position='stack') \
    + geom_col(aes(y='H',fill=0),position='stack') 
            
# logaithmierte D und T
def log10(x):
    if x>0:
        return x
    else:
        return 1
doc_logT = doc['T'].apply(lambda x: math.log(log10(x),10)) #sehr langsam :/
doc_logD = doc['D'].apply(lambda x: math.log(log10(x),10)) # -> np.log(x) (geht auch mit df/ser?!)
doc_logDT = pd.DataFrame((doc['days'], doc_logT, doc_logD)).T
ggplot(doc_logDT, aes(x='days'))   + geom_line(aes(y="D")) \
                             + geom_line(aes(y="T"))


# tägliche Neuinfektionen, vs Veränderung Infizierter vs Tote
D_chng = []; D_nw = []; R_nw = []; T_nw = []
for i in np.arange(len(doc)-1)+1:
    D_chng.append(doc.loc[i,"D"]-doc.loc[i-1,"D"])
    D_nw.append(doc.loc[i-1,"H"]-doc.loc[i,"H"])
    R_nw.append(doc.loc[i,"R"]-doc.loc[i-1,"R"])
    T_nw.append(doc.loc[i,"T"]-doc.loc[i-1,"T"])
doc_change = pd.DataFrame({'D': doc.loc[1:25,"D"],
                           'G': np.add(doc.loc[1:25,"H"],doc.loc[1:25,"R"]), #Genesene+Healthy
                           'D_change': D_chng, 
                           'D_new' :D_nw, 
                           'R_new':R_nw,
                           'days':doc.loc[1:25,'days'], 
                           'T':doc.loc[1:25,"T"],
                           'T_new':np.multiply(-1, T_nw),
                           'sgR_new': (R_nw > T_nw),
                           'sgD_change': np.sign(D_chng), #zeigt an, ob die Verringerung Kranker eher wegen Todes oder Genesungen kommt
                           'cumT':np.add(R_nw,T_nw)}) 
ggplot(doc_change, aes(x='days'))  \
    + geom_col(aes(y="cumT"),fill='red',width=.6) \
    + geom_col(aes(y="D_new",alpha=.5)) \
    + geom_col(aes(y="R_new",width=.6,fill='sgD_change')) \
    + geom_line(aes(y='G'))
    #+ geom_line(aes(y="D_change"))
    #+ geom_col(aes(y="D_change", col='sgR_new')) #<-könnte später interessant werden, wenn in Simulationen die Ansteckungsraten langsamer sind, also sich D ändert, weil Leute sterben (-), genesen (-) und sich anstecken (+) 
doc_change.sgR_new


'''
Welche Veränderungen sind wichtig?
Wie viele Leute sterben?
Wie viele Leute stecken sich täglich an?
Wie viele Leute genesen?

Das vielleicht gegen ein Barplot der gestacked die Toten, Gesunden und Resistenten anzeigt

'''
    
'''
Notizen vom 20.07:
Grafiken:
rote Column negativ: Tote/Tag, grüne positiv: Genesungen pro Tag, gelbe Transparent dahinter: Neuinfektionen, Linie: entweder D oder cumD
'''
