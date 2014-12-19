

import pandas as pd
import numpy as np
import networkx as nx



""" output txt """

#crée le graph pour graphviz
def affichage(Label,edges,di,do):
    m=0
    m2=0
    m3=0
    for i,j in edges:
        if i!=j:
            m=max(m,di[(i,j)])
        else:
            m2=max(m2,di[(i,j)])
            m3=max(m2,do[i])
    sol='graph G { '
    for i in Label:
        sol=sol + '\n' +str(i)+ '[style=filled,color=\"#0000FF'+str(hex(int((255*di[(i,i)])/float(m2))))[2:]+ '\",label = \" ' +Label[i]+' \", fontsize=8, heigth=0.1,shape=rounded,fillcolor=\"#FF0000'+str(hex(int((255*do[i])/float(m3))))[2:]+ '\"];'
    sol=sol+'\n'
    for i,j in edges:
        if i!=j:
            sol=sol+ '\n'+str(i)+' -- '+ str(j)+ '[color=\"#0000FF'+str(hex(int((255*di[(i,j)])/float(m))))[2:]+ '\" ];'
    sol=sol+'\n }'
    return(sol)


def generate_txt(fil,txt):
    f=open(fil,"w")
    f.write(txt)
    f.close()


def create_graph(g_name,lis,dd,d,pickle=False):
    g_name=nx.Graph()
    for node in lis:
        g_name.add_node(node)    
    g_name.add_weighted_edges_from(dd)
    g_name.add_edges_from(d)
    
    if pickle:
        pd.to_pickle(g_name,g_name+".pkl")
    
    return g_name

def Recup(part,N):
    dic={}
    for i in part.keys():
        dic[part[i]]=dic.get(part[i],0)+1
        l=[]
    for i in dic.keys():
        if (dic[i]<N):
            l.append(i)
    for i in l:
        del dic[i]
    return list(dic.keys())

part=pd.read_pickle("part_rnd.pkl")

di=pd.read_pickle("di_wedges_bigcom_rnd.pkl")
labels=np.load("labelrnd.npy")


def d_nparc(part):
    dic={}
    for i in part.keys():
        dic[part[i]]=dic.get(part[i],0)+1
    return(dic)


d={}
for u in di.keys():
    if di[u]>60:
        d[u]=di[u]

dd=[u+(v,) for u,v in d.iteritems()]

a=[]
for t in dd:
    a.extend(t[0:1])

a=list(set(a))

d_labels={}
for i in labels:
    if float(i[0]) in a:
        d_labels[int(i[0])]=i[1]

do=d_nparc(part)
Gfin=create_graph("Gfin",Recup(part,100),dd,d)

generate_txt("gviz_rnd.txt",affichage(d_labels,Gfin.edges(),di,do))