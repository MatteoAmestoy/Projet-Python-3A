
import pandas as pd
import numpy as np


part=pd.read_pickle("part_ord.pkl")



#Fonction trouvant les trois mots les plus presents dans une liste

def mot_plus(l):
    d={}
    for i in l:
        d[i]=d.get(i,0)+1
        
    lu=[]
    for i in d:
        lu.append((i,d[i]))

    lu=np.array(lu,dtype=[('x', 'S16'), ('y', int)])
   
    lu.sort(order='y')
    sol=''
    for i,j in lu[-3:]:
        sol= sol+' '+i.decode('utf-8')
    print(sol)
    return(sol)
  

 #enleve les majuscules

def minus(l):  
    for i in range(len(l)):
        l[i]=l[i].lower()
    return(list(set(l)))    



def trouver_mot(dic,DA):
    d={}
    for i in dic:
        text=[]
        for t in dic[i]:            
            text=text+minus(DA.loc[t]['Subject'])
        tmax=mot_plus(text)
        d[i]=tmax
    return(d)
    
    
#cree le dictionnaire des auteurs d'une communaute    
d={}
for i in part:
    d[part[i]]=d.get(part[i],[])+[i]


DataAuthor=pd.read_pickle("DataAuthor.pkl")

for j,i in enumerate(DataAuthor['Subject']):
    DataAuthor['Subject'][j]=[item for sublist in i for item in sublist]

DataAuthor.index=DataAuthor['ID']
    
do=trouver_mot(d,DataAuthor)

lu=[]
for i in do:
    lu.append([i,do[i]])  

