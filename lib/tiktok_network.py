import pandas as pd
import networkx as nx
import numpy as np
from random import randrange
import math

def position_1(radius):
    x_coord = radius
    y_coord = radius
    return (x_coord, y_coord)

def graphStats(graph):
    print('Number of nodes: '+str(graph.number_of_nodes()))
    print('Number of edges: '+str(graph.number_of_edges()))
    print('Mean indegree: '+str(np.mean([x[1] for x in graph.in_degree()])))
    print('Mean indegree std: '+str(np.std([x[1] for x in graph.in_degree()])))
    print('Mean outdegree: '+str(np.mean([x[1] for x in graph.out_degree()])))
    print('Mean outdegree std: '+str(np.std([x[1] for x in graph.out_degree()])))
    print('Average clustering coefficient: '+str(nx.average_clustering(graph)))
    print('Density: '+str(nx.density(graph)))

def graphCalculation(dataset, colorCriteria):
    nodes = set()
    labels = dict()
    colors = list()
    edges = list()
    dmap = dict()
    pos = dict()
    df = pd.read_csv("./dataset/dataset_"+dataset+"_connections_etl.csv", sep=";")
    df = df[df["likedBy_uniqueId"]!= "-"]
    df = df[df["likedBy_uniqueId"]!=df["author_uniqueId"]] # remove unconnected nodes
    for index, row in df.iterrows():
        nodes.add(int(row["author_id"]))
        labels[int(row["author_id"])] = row["author_uniqueId"]
        nodes.add(int(row["likedBy_id"]))
        labels[int(row["likedBy_id"])] = row["likedBy_uniqueId"]
        edg=[]
        source=int(row['likedBy_id'])
        target=int(row['author_id'])
        edg.append(source)
        edg.append(target)
        edges.append(edg)
    if colorCriteria == 'createTime':
        df['createTime'] = pd.to_datetime(df['createTime']).astype(np.int64) / 10e9
        df['createTime'] = round((df['createTime']-df['createTime'].min())/(df['createTime'].max()-df['createTime'].min()) * 255) # RGB color
        for node in nodes:
            pos[node] = "" # prepare position dictionary
            if node in list(df['author_id'].astype(np.int64)):
                val = int(df.loc[df['author_id'].astype(np.int64) == node, 'createTime'].iloc[:].values[0])
                if df.loc[df['author_id'].astype(np.int64) == node, 'originalVideo'].iloc[:].values[0] == 1:
                    colors.append("#ff0000")
                else:
                    colors.append('#%02x%02x%02x' % (val, val, val))
            else:
                val = 256
                colors.append("#ffff57")
            try:
                dmap[val].append(node)
            except:
                dmap[val] = [node]
        dict_k = sorted(list(dmap.keys()))
        for val in dict_k:
            for node in dmap[val]:
                radius = val
                pos[node] = position_1(radius + 10) # calculate node position from radius
                angolo = randrange(361) 
                x = radius*(math.cos(angolo))
                y = radius*(math.sin(angolo))
                pos[node] = (x,y)

    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return [graph, labels, colors, pos]
    