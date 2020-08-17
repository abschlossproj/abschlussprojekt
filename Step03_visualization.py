
#this file should be on master branch, with Step01,02 and Readme and besprechung on MatBranch2
'''
This script loads the .csv's from documentation_tables/, combines them into a single dataframe.
Some graphics are then generated to compare the scenarios and different interesting developments.
To that end, some more columns are generated out of the existing ones.
Between scenarios the difference between k and p seems most interesting, so m is fixed mostly at 5.
To make only a single nice graphic, one scenario is chosen at random (the first or fourth one)
The graphics are saved to graphics/
'''

def Step03_visualization():
    
    from plotnine import ggplot, aes, geom_line, geom_col, facet_grid,  scale_y_log10, geom_point, facet_wrap, geom_step, geom_boxplot, facet_wrap, geom_crossbar, coord_cartesian, coord_flip, geom_bar, ggsave, geom_tile, geom_smooth, geom_segment, geom_text, geom_hline, theme_bw, ylim, labs, scale_color_gradient, theme_set, theme, scale_color_discrete, theme_void, theme_linedraw, theme_classic, xlim, themes, element_rect, scale_colour_manual, element_text, element_line, geom_text, annotate

    import pandas as pd
    import numpy as np
    import math
    import os

    import datetime
    #import glob
    import matplotlib.pyplot as plt

    graphics = "graphics/"
    if not (os.path.exists(graphics) or graphics in os.listdir()):
        os.mkdir(graphics) 

    # prepare a number for log_10, so that we don't get 'ugly' values under 1
    def log10(x):
        if x>10:
            return x
        elif x>0:
            return 11
        else: #if x=0
            return 10 # 1 would be better, looks not good tho, and the base would look like zero

    #print('Expected runtime: XXmin')
    starttime = datetime.datetime.now()
    print('Start at:', starttime)
    print('-'*80)
    print('graphics are being generated... Do not press any key...')
    print('-'*80)


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
    #docs[docs.days==t] #-> there are still D!!!! 105 not long enough!!!!! -> make it dynamically, espec. if there's an upcoming diff between with quarantine and w/o???
    #also change colors etc?


    ########################
    # 1 Data manipulation   #
    #######################

    # Some nice simulations are chosen:
    docm05 = docs[docs.m==5]
    #################################################################
    file = files[25] #arbitrarely chosen scenario with a nice development
    ################################################################
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

    doc_change = pd.DataFrame({'H': doc.loc[1:t,'H'],
                               'D': doc.loc[1:t,"D"],
                               'G': np.add(doc.loc[1:t,"H"],doc.loc[1:t,"R"]), #Genesene+Healthy
                               'D_change': D_chng, 
                               'D_new' :D_nw,
                               'D_new_c': np.add(np.add(R_nw,T_nw),D_nw),
                               'D_new_neg': np.negative(D_nw),
                               'R_new':R_nw,
                               'R_new_c':np.add(R_nw,T_nw),
                               'R_new_neg': np.negative(R_nw),
                               'days':doc.loc[1:t,'days'], 
                               'T':doc.loc[1:t,"T"],
                               'T_new':np.multiply(-1, T_nw),
                               'T_new_pos':T_nw,
                               'T_new_log': (np.log10(list(map(log10, T_nw)))),
                               'cumT':np.add(R_nw,T_nw)}) 

    #cumsums -> makes overlapping possible, doc_c['T'] (not doc_c.T) actually is always 5000
    doc_c = doc.copy()
    doc_c['D'] = doc_c['D']+doc_c['H']
    doc_c['R'] = doc_c['R']+doc_c['D']
    doc_c['T'] = doc_c['T']+doc_c['R']

    # logaithmierte D und T
    doc_logT = doc['T'].apply(lambda x: math.log(log10(x),10)) #sehr langsam :/
    doc_logD = doc['D'].apply(lambda x: math.log(log10(x),10)) # -> np.log(x) (geht auch mit df/ser?!)
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
    '''
    ggsave(filename = graphics + 'point_pk.png', width=w, height=h, units=u, plot=
            g + geom_point(aes(y=docm05.D, fill='p', size='k'))
          )
    '''
    ggsave(filename = graphics + 'line_pk.png', width=w, height=1.5*h, units=u, dpi=dpi, plot=
            g + geom_line(aes(y='D', color='k', fill='k')) + facet_wrap(('p','k'), labeller='label_both')\
              + labs(y='infected persons', title='Only the strictest measures flatten the curve') + scale_color_gradient(guide=False) + theme_void()
          )

    g_int = ggplot(doc_interest, aes(x='days',y='D'))
    '''
    ggsave(filename = graphics + 'line_pk-logfacet.png', width=w, height=h, units=u, dpi=dpi, plot=
            g_int + geom_line(aes(colour='k')) + scale_y_log10() + facet_wrap('p')
          )
    '''
    ggsave(filename = graphics + 'line_pk-log.png', width=w, height=h, units=u, dpi=dpi, plot=
            g_int + geom_line(aes(colour='k',linetype="p")) + scale_y_log10()\
                  + labs(y='Infected persons', title='Cases for some scenarios from \'day zero\'') + theme_linedraw()
          )

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
    '''
    ggsave(filename = graphics + 'time_line.png', width=w, height=h, units=u, dpi=dpi, plot=
            ggplot(doc, aes(x='days'))\
                + geom_line(aes(y='H')) \
                + geom_line(aes(y="D")) \
                + geom_line(aes(y="T")) \
                + geom_line(aes(y="R")) 
          )
    '''

    # Zeit vs Anzahl -> transparent überlappendes Säulendiagramm
    g_col = ggplot(doc, aes(x= "days")) \
                + geom_line(aes(y='H'),color='#203910',position='stack',alpha=0.4) \
                + geom_line(aes(y="D"),color='purple',position='stack',alpha=0.4) \
                + geom_line(aes(y="R"),color='#4101a2',position='stack',alpha=0.4) \
                + geom_line(aes(y="T"),color='#b21281',position='stack',alpha=0.4) 
    '''
    ggsave(filename = graphics + 'time_line-col.png', width=w, height=h, units=u, dpi=dpi, plot=
            g_col + theme_bw() #+ scale_color_gradient(guide=False)
          )
    '''
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
    '''
    ggsave(filename = graphics + 'time_line_colchange', width=w, height=h, units=u, dpi=dpi, plot=
            ggplot(doc_change, aes(x='days'))  \
                + geom_col(aes(y="cumT"),fill='red',width=.6) \
                + geom_col(aes(y="D_new",alpha=.5)) \
                + geom_col(aes(y="R_new",width=.6)) \
                + geom_line(aes(y='G'))
                #+ geom_line(aes(y="D_change"))
                #+ geom_col(aes(y="D_change", col='sgR_new')) #<-könnte später interessant werden, wenn in Simulationen die Ansteckungsraten langsamer sind, also sich D ändert, weil Leute sterben (-), genesen (-) und sich anstecken (+) 
       #+ geom_line(aes(y="G",fill='3')) \
        #+ geom_line(aes(y="H")) \
           )
    '''
    '''
    ggsave(filename = graphics + 'dunnowhat1.png', width=w, height=h, units=u, dpi=dpi, plot=
            ggplot(doc_change, aes(x='days'))  \
                + geom_col(aes(y="D_new_c", fill= 1), width=0.4) \
                + geom_col(aes(y='R_new_c', fill=2), width=0.4) \
                + scale_y_log10() \
                + geom_col(aes(y='T_new_log'),fill='red', width=0.4)
            )
    '''
    ggsave(filename = graphics + 'changes.png', width=w, height=h, units=u, dpi=dpi, plot=
            ggplot(doc_change, aes(x='days'))  \
                + geom_col(aes(y="D_new"), position='dodge',fill= 'orange', width=0.8) \
                + geom_col(aes(y='R_new'), position='dodge',fill='blue', width=0.8,alpha=.6) \
                + geom_col(aes(y='T_new_pos'),fill='red', width=1)\
                + labs(title='Daily new infected, recovered and deceased', x='', y='daily new cases') \
                + xlim(0,80) #+ scale_y_log10()
            )  #+ geom_point(aes(y='G'),fill='w') \
    #puts out errors: log10 divided by 0, removing missing values
    print('-'*80)
    print('Start at:', starttime)
    print('Fin.  at:', datetime.datetime.now())
    print('Graphics are saved in folder %s' %graphics)
    print("Done")

    '''
    To-do
    geom_line häufig problematisch, wenn es statt vieler lines nur eine ausspuckt, die alles verscuht zu kombinieren -> geom_line(aes(group = Subject ))

    of interest: differnce between iso and without iso?
    capacity when too much severe cases

    give some countries 'names' and characters, e.g. commonwealth, with a secluded AUS, a herd-immunity GBR and mixture of IRA. Then compare, and aggravate the cases across scenarios.

    https://www.nzz.ch/panorama/coronavirus-neuste-fallzahlen-in-der-schweiz-und-weltweit-ld.1542774?reduced=true
    oder siehe screenshot zib - instagramm
    '''

    
if __name__ == 'main':
    Step03_visualization()