'''
Es gibt "plotnine" für python, das hat fast die gleiche Grammatik wie ggplot2 für R.

pip install plotnine

https://plotnine.readthedocs.io/en/stable/index.html
'''

#to-do: documentation Matrix aus simul_2.py abspeichern und hier laden

from plotnine import ggplot, aes, geom_line, geom_col
import pandas as pd

file = '/home/matthias/Documents/Wien/Statistik/2020_SoSe/CompStat_SS20/alt_und_meins/meins/UE4/abschlussprojekt/documentation_simul.csv'

doc = pd.read_csv(file , index_col=0)

ggplot(doc, aes(x='days'))   + geom_line(aes(y='H')) \
                             + geom_line(aes(y="D")) \
                             + geom_line(aes(y="T")) \
                             + geom_line(aes(y="R")) 

ggplot(doc, aes(x= "days")) \
            + geom_col(aes(y='H',fill=0),position='stack',alpha=0.5) \
            + geom_col(aes(y="D",fill=1),position='stack',alpha=0.5) \
            + geom_col(aes(y="R",fill=2),position='stack',alpha=0.5) \
            + geom_col(aes(y="T",fill=3),position='stack',alpha=0.5)

ggplot(doc, aes(x='days')) + geom_bar(aes(fill='days'))
