# -*- coding: utf-8 -*-
'''
This script saves a numpy Matrix in its directory for k=[5,10,20]
The matrix can then be used for contact-tracing in the next step of simulating.
As it is only one matrix, it is assumed that the number of contacts, and the contact itself doesn't change over time

Problem: in adMatrix finden sich Zeilen mit weniger als 20 Einträgen. Es gibt aber keine Loesung, sodass alle Personen 20 Kontakte haben koennen
The loop for all three matrices takes about 7min
'''
def Step01_ADM():
    import numpy as np

    N = 5000    # populationsize
    k_l = [5,10,20]     # figure of social interactions per day

    adMatrix = np.zeros((N, N), dtype=bool)    # matrix which shows social contacts

    def indexfilter_2(matrix, row):
        hv = np.where(np.sum(matrix[:,row+1:N], axis=0) < k)
        potCon = hv[0] + (row + 1)
        return potCon

    for k in k_l:
        print('calculating and saving matrix...')    
        for i in np.arange(N):    # loop for every row
            potCon = indexfilter_2(adMatrix, i)    # list with potentional new contacs per row
            addCon = k - adMatrix[i,].sum()      # additional contacs for k entries in a row  

            if addCon > 0 and len(potCon) > 0:
                newCon = min(addCon, len(potCon))  # new social contacts     ## HIER WAR FEHLER IN ANGABE K MUSS DURCH addCon ERSETZT WERDEN
                indizes = np.random.choice(potCon, newCon, replace=False)   # chooses random indices out of potential indices
                adMatrix[i, indizes] = True   
                adMatrix[indizes, i] = True   # transpose the matrix

        np.save(f'adMatrix_k{k}.npy', adMatrix)   # saves adMatrix
        print(f'Saved adMatrix_k{k}.npy')

    print(f'{N}*{N}-adMatrices have been saved for three numbers of continued daily contacts per person {k_l}')

if __name__ == 'main':
    Step01_ADM()