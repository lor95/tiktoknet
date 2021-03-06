import pandas as pd
import networkx as nx
import numpy as np
from random import randrange
import math
import datetime

def ETL2(dataFrame, remAutoLikes):
    dataFrame = dataFrame[dataFrame["likedBy_uniqueId"]!= "-"]
    if remAutoLikes:
        dataFrame = dataFrame[dataFrame["likedBy_uniqueId"]!=dataFrame["author_uniqueId"]] # remove unconnected nodes
    return dataFrame

def position_1(radius):
    angle = randrange(361) #calcolo un numero casuale da 0 a 360
    x_coord = radius*(math.cos(angle))
    y_coord = radius*(math.sin(angle))
    return (x_coord, y_coord)

def graphStats(graph, _print=True):
    stats = {"nnodes":graph.number_of_nodes(),
             "nedges":graph.number_of_edges(),
             "mindegree":np.mean([x[1] for x in graph.in_degree()]),
             "moutdegree":np.mean([x[1] for x in graph.out_degree()]),
             "avgclust":nx.average_clustering(graph),
             "density":nx.density(graph)}
    if _print:
        print('Number of nodes: '+str(stats["nnodes"]))
        print('Number of edges: '+str(stats["nedges"]))
        print('Mean indegree: '+str(stats["mindegree"]))
        print('Mean indegree std: '+str(np.std([x[1] for x in graph.in_degree()])))
        print('Mean outdegree: '+str(stats["moutdegree"]))
        print('Mean outdegree std: '+str(np.std([x[1] for x in graph.out_degree()])))
        print('Average clustering coefficient: '+str(stats["avgclust"]))
        print('Density: '+str(stats["density"]))
    return stats

def graphCalculation(dataset, colorCriteria = "createTime", lifespanCond = None, intervals = None, remAutoLikes = True):
    nodes = set()
    labels = dict()
    dates = dict()
    colors = list()
    edges = list()
    dmap = dict()
    pos = dict()
    lifespan_stats_days = 0
    nodestats = dict()
    df = pd.read_csv("./dataset/dataset_"+dataset+"_connections_etl.csv", sep=";")
    df['createTime'] = pd.to_datetime(df['createTime'])
    dtemp = df.copy()
    df = ETL2(df, remAutoLikes)
    max_ = df['createTime'].max()
    lifespan = max_ - df['createTime'].min()
    if intervals is not None:
        lifespanCond = None
        lim_sup = df["createTime"].min() + (lifespan/100 * intervals[1])
        lim_inf = df["createTime"].min() + (lifespan/100 * intervals[0])
        lifespan_stats_days = (lim_sup - lim_inf).days
        df = df.loc[df["createTime"].between(lim_inf, lim_sup)]
    if lifespanCond is not None:
        df = df.loc[df['createTime'] >= (df['createTime'].min() + (lifespan/100 *lifespanCond))]
    dfnet = df.copy()
    for index, row in df.iterrows():
        nodes.add(int(row["author_id"]))
        labels[int(row["author_id"])] = row["author_uniqueId"]
        dates[int(row["author_id"])] = int((row["createTime"] - pd.Timestamp('19700101')).total_seconds())
        nodes.add(int(row["likedBy_id"]))
        labels[int(row["likedBy_id"])] = row["likedBy_uniqueId"]
        dates[int(row["likedBy_id"])] = int((max_ - pd.Timestamp('19700101')).total_seconds())
        edg=[]
        source=int(row['likedBy_id'])
        target=int(row['author_id'])
        edg.append(source)
        edg.append(target)
        edges.append(edg)
    if colorCriteria == 'createTime':
        df['createTime_norm'] = df['createTime'].astype(np.int64) / 10e9
        df['createTime_norm'] = round((df['createTime_norm']-df['createTime_norm'].min())/(df['createTime_norm'].max()-df['createTime_norm'].min()) * 255) # RGB color
        for node in nodes:
            pos[node] = "" # prepare position dictionary
            if node in list(df['author_id'].astype(np.int64)):
                nodestats[node] = {"createTime":df.loc[df['author_id'].astype(np.int64) == node, 'createTime'].iloc[:].values[0],
                                   "music_id":str(df.loc[df['author_id'].astype(np.int64) == node, 'music_id'].iloc[:].values[0]),
                                   "video_duration": df.loc[df['author_id'].astype(np.int64) == node, 'video_duration'].iloc[:].values[0],
                                   "stats_diggCount":df.loc[df['author_id'].astype(np.int64) == node, 'stats_diggCount'].iloc[:].values[0],
                                   "stats_shareCount":df.loc[df['author_id'].astype(np.int64) == node, 'stats_shareCount'].iloc[:].values[0],
                                   "stats_commentCount":df.loc[df['author_id'].astype(np.int64) == node, 'stats_commentCount'].iloc[:].values[0],
                                   "stats_playCount":df.loc[df['author_id'].astype(np.int64) == node, 'stats_playCount'].iloc[:].values[0],
                                   "authorStats_diggCount":df.loc[df['author_id'].astype(np.int64) == node, 'authorStats_diggCount'].iloc[:].values[0],
                                   "authorStats_followingCount":df.loc[df['author_id'].astype(np.int64) == node, 'authorStats_followingCount'].iloc[:].values[0],
                                   "authorStats_heartCount":df.loc[df['author_id'].astype(np.int64) == node, 'authorStats_heartCount'].iloc[:].values[0],
                                   "authorStats_followerCount":df.loc[df['author_id'].astype(np.int64) == node, 'authorStats_followerCount'].iloc[:].values[0],
                                   "authorStats_videoCount":df.loc[df['author_id'].astype(np.int64) == node, 'authorStats_videoCount'].iloc[:].values[0]}
                try:
                    val = int(df.loc[df['author_id'].astype(np.int64) == node, 'createTime_norm'].iloc[:].values[0])
                except:
                    val = 0
                if df.loc[df['author_id'].astype(np.int64) == node, 'originalVideo'].iloc[:].values[0] == 1:
                    colors.append("#ff0000")
                else:
                    colors.append('#%02x%02x%02x' % (val, val, val))
            else:
                dfnet = dfnet.append(dtemp.loc[dtemp['author_id'].astype(np.int64) == node].iloc[:])
                val = 256
                colors.append("#ffff57")
            try:
                dmap[val].append(node)
            except:
                dmap[val] = [node]
        dict_k = sorted(list(dmap.keys()))
        for val in dict_k:
            for node in dmap[val]:
                pos[node] = position_1(val)
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    nx.set_node_attributes(graph, labels, "label")
    nx.set_node_attributes(graph, dates, "datetime")
    graph.add_edges_from(edges)
    dfnet.drop_duplicates(subset ='author_id',keep = 'first', inplace = True)
    dfinterval = df # represents the dataset of the net
    return [graph, labels, colors, pos, nodestats, dfnet, dfinterval, lifespan_stats_days, dtemp]
