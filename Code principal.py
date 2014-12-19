

""" import """
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from random import shuffle
import community
# il faut installer community via https://pypi.python.org/pypi/python-louvain/0.3


""" data """

y=np.load(r"Edges.npy")
df=pd.DataFrame(y)


""" create basic graph """
G=nx.Graph()

#==============================================================================
# nodes
#==============================================================================
nodes=set(df.iloc[:,0]).union(set(df.iloc[:,1]))
nodes=list(nodes)

#Si on veut melanger les aretes

def my_shuffle(array):
        shuffle(array)
        return array

for node in my_shuffle(nodes): 
    G.add_node(node)

#sinon
#for node in nodes: # +shuffle
#    G.add_node(node)


#==============================================================================
#  edges
#==============================================================================
for i in range(df.shape[0]):
    G.add_edge(df.iloc[i,0],df.iloc[i,1])

#pd.to_pickle(G,"G.pkl")
G=pd.read_pickle("G.pkl")


""" get partition """
part = community.best_partition(G)



    
#pd.to_pickle(part,"part_rnd.pkl")

#values = [part.get(node) for node in G.nodes()]
#pd.to_pickle(values,"values.pkl")

part_rnd=pd.read_pickle("part_rnd.pkl")
part_ord=pd.read_pickle("part_ord.pkl")
part_rev=pd.read_pickle("part_rev.pkl")
#values=pd.read_pickle("values.pkl")

#plt.hist(part_ord.values(),bins=range(len(part_ord)))

""" creation and selection of group """
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

lis=Recup(part_ord,100)

def elim(part,l):
    lsommet=[]
    for i in l:
        lsommet=lsommet+[c for c,v in part.items() if v==i]
    return lsommet

l_nodes=elim(part_ord,lis)


#""" graph of group : get rid of small communities """
# cette partie du code n'est pas utilispe dans la suite, elle nous a servi temporairement a voir les donnees
#G2=nx.Graph()
#for node in l_nodes:
#    G2.add_node(node)
#
#for i in range(df.shape[0]):
#    if df.iloc[i,0] in l_nodes:
#        if df.iloc[i,1] in l_nodes:
#            G2.add_edge(df.iloc[i,0],df.iloc[i,1])
#
#pd.to_pickle(G2,"G2_rnd.pkl")
##G2=pd.read_pickle("G2_rnd.pkl")
#
#partition2=community.best_partition(G2)
#pd.to_pickle(partition2,"partition2.pkl")

""" selection of large groups """
#==============================================================================
# # new data
#==============================================================================
df2=pd.DataFrame(columns=["From","To"])
for i in range(df.shape[0]):
    u,v=df.iloc[i,:]
    if u in l_nodes and v in l_nodes:
        df2.loc[df2.shape[0]+1]=[u,v]

pd.to_pickle(df2,"df_edges_bigcom_rnd.pkl")
#df2=pd.read_pickle("df_edges_bigcom_rnd.pkl")

#==============================================================================
# # new dictionnary
#==============================================================================
di={}
for i in range(df2.shape[0]):
    u,v=df2.iloc[i,:]
    k=part_ord[u]
    l=part_ord[v]
    p=min(k,l),max(k,l)
    di[p]=di.get(p,0)+1

pd.to_pickle(di,"di_wedges_bigcom_rnd.pkl")
#di=pd.read_pickle("di_wedges_bigcom_rnd.pkl")
#
labels=np.load("label_rnd.npy")


#==============================================================================
# # selection on the dictionnary
#==============================================================================
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


""" stat """
def stat(g,ind=None,plot=False):
    df_stat=pd.DataFrame(columns=["Number of nodes","Number of edges","Sum of degrees","Mean of degrees"])
    df_stat["Number of nodes"]=[g.number_of_nodes()]
    df_stat["Number of edges"]=[g.number_of_edges()]
    df_stat["Sum of degrees"]=[np.sum(g.degree().values())]
    df_stat["Mean of degrees"]=[np.mean(g.degree().values())]
    
    if ind!=None:
        df_stat.index=[ind]
    
    if plot:
        degree_sequence=sorted(nx.degree(g).values(),rnderse=True)
        plt.hist(degree_sequence,normed=True)
        plt.figure()
        plt.loglog(degree_sequence,'b-',marker='o')
        plt.title("Degree rank plot")
        plt.ylabel("degree")
        plt.xlabel("rank")
        plt.show()
    
    return df_stat

""" graph of large groups """
def create_graph(g_name,lis,dd,d,pickle=True):
    g_name=nx.Graph()
    for node in lis:
        g_name.add_node(node)    
    g_name.add_weighted_edges_from(dd)
    g_name.add_edges_from(d)
    
    if pickle:
        pd.to_pickle(g_name,g_name+".pkl")
    
    return g_name


def draw(g,d,labels):
    pos = nx.spring_layout(g)
    nx.draw_networkx_edge_labels(g,pos,edge_labels=d)
    nx.draw(g,pos,node_size=30)
    nx.draw_networkx_nodes(g,pos,nodelist=g.node.keys(),node_color='r',node_size=30)
    nx.draw_networkx_labels(g,pos,labels,font_size=16)



def get_subgraph(g,partition):
    l=Recup(partition,100)
    l_subgraph=[]
    for i in l:
        l_subgraph.append(g.subgraph([c for c,v in partition.items() if v==i]))
    return l_subgraph

def stat_subgraph(g,partition,labels,plot=False):
    return pd.concat([stat(sg,ind=str(labels.values()[i]),plot=plot).T for i,sg in enumerate(get_subgraph(g,partition))],axis=1).T

#print(stat_subgraph(G,part_ord,d_labels))
#print(stat_subgraph(G,part_ord,d_labels).describe())

nx.draw_spring(G,node_size=3)


def mod(graph,partition):
    return community.modularity(partition, graph)

print(mod(G,part_rnd))
print(mod(G,part_ord))
print(mod(G,part_rev)-mod(G,part_rnd))