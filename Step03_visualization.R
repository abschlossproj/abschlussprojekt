# ab Z. 70 noch in python
'
This script loads the .csv files from documentation_tables/, combines them into a single dataframe.
Some graphics are then generated to compare the scenarios and different interesting developments.
To that end, some more rows are generated out of the existing ones.
As scenarios the difference between k and p seems most interesting, so m is fixed mostly at 5.
One scenario is randomly chosen to illustrate further
The graphics are saved to graphics/
'

library(ggplot)
library(readr)
library(dplyr)
library(stringr)

WorkingDirectory <- readline(prompt="Enter the working directory or press [Enter] if your on matthias's machine: ")
if (str_length(WorkingDirectory) <5) {WorkingDirectory <- "/home/matthias/Documents/Wien/Statistik/2020_SoSe/CompStat_SS20/alt_und_meins/meins/UE4/abschlussprojekt"}
paste('Working directory: ', WorkingDirectory)

#setwd(WorkingDirectory)
graphics = file.path(WorkingDirectory,"Rgraphics/")

# prepare a number for log_10, so that we don't get 'ugly' values under 1
log10 <- function(x){
  if (x>10)      {x
  }else if (x>0) {11
  }else          {10 }}


print('-------------------------------------------------------')
print('graphics are being generated... Do not press any key...')
print('-------------------------------------------------------')


files = list.files(file.path(WorkingDirectory,'documentation_tables')) #lists all csv generated in simul script


# combine all the tables into one dataframe 'docs'
docs= data.frame()
for (x in files) {
  df = read_delim(file.path(WorkingDirectory,'documentation_tables' , x), delim=',') 
#slice the parameters of the scenario from the filename
  df = df %>% mutate(
                    'k' = as.integer(str_sub(x, 22,23)),
                    'm' = as.integer(str_sub(x, 26,27)),
                    'p' = as.integer(str_sub(x, 30,31)),
                    )
  docs = bind_rows(docs, df)  
}

t = 105 #max(docs['days'])


########################
# 1 Data manipulation   #
#######################

# Some nice simulations are chosen:
docm05 = docs[docs['m']==5,]
#################################################################
file = files[25] #arbitrarely chosen scenario with a nice development
################################################################
doc = read_delim(file.path(WorkingDirectory,'documentation_tables', file), delim=',')



docm05_cp = docm05
docm05_cp <- mutate(docm05_cp, 'k' = toString('k'), 'p'= toString('p'))
doc_interest = docm05_cp[docm05_cp['days']<10]

###################################################################################
#####################################################################################
########################################### till here in R #########################
#####################################################################################
####################################################################################

# tägliche Neuinfektionen, vs Veränderung Infizierter vs Tote
D_chng = []; D_nw = []; R_nw = []; T_nw = []
for i in np.arange(len(doc)-1)+1:
  D_chng.append(doc.loc[i,"D"]-doc.loc[i-1,"D"])
D_nw.append(doc.loc[i-1,"H"]-doc.loc[i,"H"])
R_nw.append(doc.loc[i,"R"]-doc.loc[i-1,"R"])
T_nw.append(doc.loc[i,"T"]-doc.loc[i-1,"T"])

doc_change = pd.DataFrame({'H': doc.loc[1:t,'H'],
  'D': doc.loc[1:t,"D"],
  'G': np.add(doc.loc[1:t,"H"],doc.loc[1:t,"R"]), #Genesene+Healthy
  'D_change': D_chng, 
  'D_new' :D_nw,
  'R_new':R_nw,
  'days':doc.loc[1:t,'days'], 
  'T':doc.loc[1:t,"T"],
  'T_new':np.multiply(-1, T_nw),
  'T_new_pos':T_nw,
  'T_new_log': (np.log10(list(map(log10, T_nw)))) }) 

#cumsums -> makes overlapping possible, doc_c['T'] (not doc_c.T) actually is always 5000
doc_c = doc.copy()
doc_c['D'] = doc_c['D']+doc_c['H']
doc_c['R'] = doc_c['R']+doc_c['D']
doc_c['T'] = doc_c['T']+doc_c['R']

# logaithmierte D und T
doc_logT = doc['T'].apply(lambda x: math.log(log10(x), 10)) #sehr langsam :/
doc_logD = doc['D'].apply(lambda x: math.log(log10(x), 10)) # -> np.log(x) (geht auch mit df/ser?!)
doc_logIso = doc.Iso.apply(lambda x: math.log(log10(x),10))
doc_logDT = pd.DataFrame((doc['days'], doc_logT, doc_logD, doc_logIso)).T


#################
# 2 Plotting    #
################


# units for saving
w=15; h=10; u='cm'; dpi=300

# Mimicking the ZIB Plots on Instagramm
ggsave(filename = graphics + 'ZIB-like.png', width=w, height=w, units=u, dpi=dpi, plot=
         ggplot(doc_change, aes(x= "days", y='D_new')) \
       + geom_col(fill='white', width=.8) + geom_smooth(color='yellow', size=1.5)\
       + labs(title='XYZ Virus in Scenario ABC:\n Tägliche Neuinfektionen', y='')\
       + theme_classic()\
       + theme( rect=element_rect(color='#0072B2', size=0, fill='#0072B2'),\
                axis_text = element_text(colour = 'white'), axis_title = element_text(colour = 'white'), \
                axis_line = element_line(color='white'), plot_title = element_text(colour = 'white'))\
       + xlim(20,55) + ylim(0,180)
)#value in R as c(), axis.title


g = ggplot(docm05, aes(x='days'))

# facet über p, k, m fix 5
ggsave(filename = graphics + 'pkm_facet.png', width=w, height=h, units=u, dpi=dpi, plot=
         g + geom_line(aes(y='T'))  + labs(title='Herding immunity works, \nHygiene and Distancing is better', y='virus fatalities')\
       + facet_grid(('k','p'), labeller='label_both') #in R not a tuple but ~
)
# interesting: for (20,50) there's less deads in total than vor (10,25)


# line-graphs, die die totalen Infizierten über verschiedenen p,k vergleichen
ggsave(filename = graphics + 'line_pk.png', width=w, height=1.5*h, units=u, dpi=dpi, plot=
         g + geom_line(aes(y='D', color='k', fill='k')) + facet_wrap(('p','k'), labeller='label_both')\
       + labs(y='infected persons', title='Only the strictest measures flatten the curve') + scale_color_gradient(guide=False) + theme_void()
)

g_int = ggplot(doc_interest, aes(x='days',y='D'))

ggsave(filename = graphics + 'line_pk-log.png', width=w, height=h, units=u, dpi=dpi, plot=
         g_int + geom_line(aes(colour='k',linetype="p")) + scale_y_log10()\
       + labs(y='Infected persons', title='Cases for some scenarios from \'day zero\'') + theme_linedraw()
)



# Zeit vs Anzahl -> transparent überlappendes Säulendiagramm
g_col = ggplot(doc, aes(x= "days")) \
+ geom_line(aes(y='H'),color='#203910',position='stack',alpha=0.4) \
+ geom_line(aes(y="D"),color='purple',position='stack',alpha=0.4) \
+ geom_line(aes(y="R"),color='#4101a2',position='stack',alpha=0.4) \
+ geom_line(aes(y="T"),color='#b21281',position='stack',alpha=0.4) 

ggsave(filename = graphics + 'time_line-col-log.png', width=w, height=h, units=u, dpi=dpi, plot=
         g_col + scale_y_log10() + theme_bw() 
)

# "gestacktes" Säulendiagramm, sodass gut die Verhältnisse sichtbar sind
ggsave(filename = graphics + 'time_line-colstacked.png', width=w, height=h, units=u, dpi=dpi, plot=
         ggplot(doc_c, aes(x= "days")) \
       + geom_col(aes(y="T"),fill='red',position='stack') \
       + geom_col(aes(y="R"),fill='green',position='stack') \
       + geom_col(aes(y="D"),fill='yellow',position='stack') \
       + geom_col(aes(y='H'),fill='blue',position='stack') \
       + labs(y='', title='Ratio of populace that is infected, recovered or dead') + theme_bw() + xlim(0,80)\
       + annotate(geom='text', x=39, y=3000,label='Infected')\
       + annotate(geom='text', x=55, y=4000,label='Recovered')\
       + annotate(geom='text', x=14, y=1900,label='Healthy')\
       + annotate(geom='text', x=75, y=4850,label='Dead')
)
ggsave(filename = graphics + 'time_line_linesimple.png', width=w, height=h, units=u, dpi=dpi, plot=            
         ggplot(doc_logDT, aes(x='days'))\
       + geom_line(aes(y="D"),color='#0072B2') \
       + geom_line(aes(y="Iso"),color='#56B4E9') \
       + geom_line(aes(y="T"),color='#D55E00') \
       + labs(title='Isolating helps keeping fatalities low', y='cases and deaths, log10')
)

ggsave(filename = graphics + 'changes.png', width=w, height=h, units=u, dpi=dpi, plot=
         ggplot(doc_change, aes(x='days'))  \
       + geom_col(aes(y="D_new"), position='dodge',fill= 'orange', width=0.8) \
       + geom_col(aes(y='R_new'), position='dodge',fill='blue', width=0.8,alpha=.6) \
       + geom_col(aes(y='T_new_pos'),fill='red', width=1)\
       + labs(title='Daily new infected, recovered and deceased', x='', y='daily new cases') \
       + xlim(0,80)
) 


print('----------------------------------------')
#print('Start at:', starttime)
#print('Fin.  at:', datetime.datetime.now())
print(paste('Graphics are saved in folder', graphics))
print("Done")

