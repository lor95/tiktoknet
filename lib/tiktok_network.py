import pandas as pd
import networkx as nx

def graphCalculation(dataset, colorCriteria):
    df = pd.read_csv("./dataset/dataset_"+dataset+"_connections_etl.csv", sep=";")
    df = df[df["likedBy_uniqueId"]!= "-"]
    df = df[df["likedBy_uniqueId"]!=df["author_uniqueId"]] # remove unconnected nodes
    nodes = set()
    labels = {}
    colors = list()
    edges = list()
    for index, row in df.iterrows():
        nodes.add(int(row["author_id"]))
        labels[int(row["author_id"])] = row["author_uniqueId"]
        nodes.add(int(row["likedBy_id"]))
        labels[int(row["likedBy_id"])] = row["likedBy_uniqueId"]
        list_to_append=[]
        source=int(row['likedBy_id'])
        target=int(row['author_id'])
        value = 1
        list_to_append.append(source)
        list_to_append.append(target)
        list_to_append.append(value)
        edges.append(list_to_append)
    if colorCriteria == 'createTime':
        df['createTime'] = pd.to_datetime(df['createTime']).astype(int) / 10e9
        df['createTime'] = round((df['createTime']-df['createTime'].min())/(df['createTime'].max()-df['createTime'].min()) * 255) # RGB color
        for node in nodes:
            if node in list(df['author_id'].astype(int)):
                if df.loc[df['author_id'].astype(int) == node, 'originalVideo'].iloc[:].values[0] == 1:
                    colors.append("#ff0000")
                else:
                    val = int(df.loc[df['author_id'].astype(int) == node, 'createTime'].iloc[:].values[0])
                    colors.append('#%02x%02x%02x' % (val, val, val))
            else:
                colors.append("#ffff57")
    
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(edges)
    return [graph, labels, colors]

graphCalculation("ITookANap","createTime")