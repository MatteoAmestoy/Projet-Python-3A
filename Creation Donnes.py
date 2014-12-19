# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 20:26:41 2014

@author: Matteo
"""

import os
import pandas as pd
import numpy as np
import operator

chemin=r"C:/Users/Matteo/Desktop/Projet_python/1992/9201001.abs"

def all_path_files(path=os.curdir):
    l_full_files=[]
#    for fold in os.walk(path).next()[1]: Si Pyton < 3
    for fold in next(os.walk(path))[1]:
        dir_name=os.path.join(path,fold)
        l_files=os.listdir(dir_name)
        for file in l_files:
            l_full_files.append(os.path.join(dir_name, file))
    return(l_full_files)

#print(all_path_files())
che=all_path_files()

def selection(path,l,lmots):
    Author=[]
    Title=[]
    for line in open(path):
        line=line.replace('.',' ').replace(',',' ').replace('(',' ').replace(')',' ')
        fld = line.split()
        
        if len(fld)>0:
            if fld[0]=='Authors:':
                for a in fld[1:]:
                    if len(a)>3:
                        if a not in l:
                            Author.append(a)
            if fld[0]=='Title:':
                for a in fld[1:]:
                    if len(a)>3:
                        if a not in lmots:
                            Title.append(a)
    return({"Title":Title,"Authors":Author})


def create_table(paths,l,lmots):
    D_Id={}
    D_Subj={}
    ID_dispo=1
    L_edges=[]
    D_poub={}
    for p in paths:
        o=selection(p,l,lmots)
        ID_aut_art=[]
        for aut in o['Authors']:
            D_poub[aut]=D_poub.get(aut,0)+1
            D_Id[aut]=D_Id.get(aut,ID_dispo)
            D_Subj[aut]=D_Subj.get(aut,[])
            D_Subj[aut].append(o['Title'])
#            D_Subj[aut]=list(set(D_Subj[aut]))
            e=D_Id[aut]
            ID_aut_art.append(e)
            if e==ID_dispo:
                ID_dispo=ID_dispo+1
        for i,j in ((i, j) for i in ID_aut_art for j in ID_aut_art):
            if i>j:
                L_edges.append([i,j])       
#    Author_lis=pd.DataFrame([[aut,D_Id[aut],D_Subj[aut]] for aut in D_Id.iterkeys()]  ,columns=["Name",'ID',"Subject"])
    Author_lis=pd.DataFrame([[aut,D_Id[aut],D_Subj[aut]] for aut in list(D_Id.keys())]  ,columns=["Name",'ID',"Subject"])
    return( Author_lis,L_edges)
     
    
    
    
lmots=['Theory','Theories','theory','theories','with','from']   
   
l=['Mario','Carolina','Chicago','Boston','university','University','Jean-Paul','PUC-Chile','Sapienza''','Sapienza','Budapest','Rome','Roma','Paris','Berkeley','Beijing','Berlin','China','Università','Amsterdam','Institute','Paul','Park','Martin','Univ','Davic','Michael','Sergei','Thomas','West','Department',
'Kyoto','Pisa','Klaus','Alexander','John','Physics','Peter','Princeton','Richard','Carlos','Mark','Andrew','CERN','INFN','Cambridge','Bergshoeff','Germany','Townsend', 'Ghosh', 'Alberto', 'Sabra', 'Klemm', 'Hyun', 'Suzuki', 'Pierre', 'Inst', 'Lozano', 'Sorella', 'Renata', 'Jackiw', 'Gordon', 'Kiyoshi', 'Zhang', 'Frolov', 'Ivanov', 'Duff', 'Johnson', 'Dorey', 'Cumrun', 'Christian', 'Antonio', 'David', 'Tseytlin', 'Klebanov', 'Fuchs', 'Behrndt', 'Burt', 'Odintsov', 'Igor', 'Mikhail', 'Robert', 'Boer', 'Henneaux', 'Schaposnik', 'Sonnenschein', 'Joseph', 'Kraus', 'Moore', 'DAMTP', 'Brandt', 'Gomez', 'Gomes', 'Szabo', 'Silva', 'Steven', 'Dunne', "D'Auria", 'Abdalla', 'Dmitri', 'Gomis', 'Sergey', 'Sezgin', 'Patrick', 'Kallosh', 'Andrea', 'Andrei', 'Gates', 'Daniel', 'Nathan', 'Papadopoulos', 'Radu', 'Yuji', 'Elizalde', 'Sasaki', 'Larsen', 'Oleg', 'Hitoshi', 'Anton', 'Gibbons', 'Paolo', 'Hiroshi', 'Ketov', 'Victor', 'Taylor', 'Ohta', 'Matthias', 'George', 'Yang', 'Eric', 'Jens', 'Russo', 'Vladimir', 'Alex', 'Sergio', 'Stephen', 'Antoniadis', 'Evans', "Shin'ichi", 'Stefan', 'Strominger', 'Seiberg', 'Andreas', 'Rafael', 'Jose', 'Howe', 'Marco', 'Moscow', 'State', 'Semenoff', 'Chen', 'Andre', 'Kumar', 'Douglas', 'Gerald', 'Ovrut', 'Ashok', 'Alvarez', 'Theoretical', 'Kogan', 'Vafa', 'Juan', 'Nishino', 'Mirjam', 'Nojiri', 'Washington', 'Buchbinder', 'Mavromatos', 'Bernard', 'Zwiebach', 'Hollowood', 'CBPF', 'Hashimoto', 'Jorge', 'Gregory', 'Lust', 'Tokyo', 'Sato', 'Dieter', 'Edward', 'Ferrara', 'James', 'Myers', 'Susskind', 'Nick', 'Roberto', 'Hanany', 'Stefano', 'Cvetic', 'Wang', 'Pope', 'Lebedev', 'Gary', 'Hull', 'Ferreira', 'Witten']

#
## 
a,b=create_table(che,l,lmots)
#
#pd.to_pickle(a,"DataAuthor.pkl")
#np.save('Edges',b)


edge=np.load (Edges.npy')


print(len(edge[:,1]))  
DataAuthor=pd.read_pickle("DataAuthor.pkl")
print(DataAuthor.iloc[:,0])
