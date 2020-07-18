'''
Es gibt "plotnine" für python, das hat fast die gleiche Grammatik wie ggplot2 für R.

pip install plotnine

https://plotnine.readthedocs.io/en/stable/index.html

To-do: Legende, Titel, Farben, Beschriftung, Export

vllt. log Darstellung nur Kranker und Toter
Darstellung neuer Infektionen und Toter insgesamt
'''

#to-do: documentation Matrix aus simul_2.py abspeichern und hier laden

from plotnine import ggplot, aes, geom_line, geom_col
import pandas as pd
import math

file = '/home/matthias/Documents/Wien/Statistik/2020_SoSe/CompStat_SS20/alt_und_meins/meins/UE4/abschlussprojekt/documentation_simul.csv'

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
doc_change = pd.DataFrame({'D_change': D_chng, 
                           'D_new' :D_nw, 
                           'days':doc.loc[1:25,'days'], 
                           'T':doc.loc[1:25,"T"],
                           'sgR_new': (R_nw > T_nw)}) #zeigt an, ob die Verringerung Kranker eher wegen Todes oder Genesungen kommt
ggplot(doc_change, aes(x='days'))  \
    + geom_col(aes(y="T"),color='red') \
    + geom_col(aes(y="D_change", col='sgR_new')) \
    + geom_line(aes(y="D_new"))
    #+ geom_line(aes(y="D_change"))
     
    
    