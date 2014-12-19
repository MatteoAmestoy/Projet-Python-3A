# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 09:25:42 2014

@author: mamestoy
"""



def affichage(Label,edges):
    sol='graph G {'
    for i in Label:
        sol=sol + '\n' +str(i)+ '[label = \' ' +Label[i]+' \', fontsize=8,fixedsize=True, heigth=0.2,shape=rounded];'
    sol=sol+'\n'
    for i,j in edges:
        sol=sol+ '\n'+str(i)+' -- '+ str(j)+ '[constraint=false,color=blue];'
    return(sol)
