from networkx.algorithms.components.connected import number_connected_components
from networkx.classes.function import subgraph
import pandas as pd
from ast import literal_eval
import lib.tiktok_network as ntx
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def graphStats(graph, _print=True):
    unconnected_graph = graph.to_undirected()
    Gcc = sorted(nx.connected_components(unconnected_graph), key=len, reverse=True) 
    Test = sorted(nx.strongly_connected_components(graph), key=len, reverse=True)
    nnodes_ego = []
    for node in graph.nodes:
        ego = nx.ego_graph(graph, node)
        if (ego.number_of_nodes()-1) >= 3 and nx.average_clustering(ego) == 0:
            nnodes_ego.append((ego.number_of_nodes()-1))
    avg_nodes_ego = 0
    max_nodes_ego = 0
    try:
        avg_nodes_ego = sum(nnodes_ego)/len(nnodes_ego)
        max_nodes_ego = max(nnodes_ego)
    except:
        avg_nodes_ego = 0
        max_nodes_ego = 0
    avg_shpath = 0
    try:
        avg_shpath = nx.average_shortest_path_length(graph.subgraph(Test[0]).to_undirected())
    except:
        avg_shpath = 0
    stats = {"nnodes":graph.number_of_nodes(),
             "nedges":graph.number_of_edges(),
             "density":nx.density(graph),
             "mean_degree":np.mean([x[1] for x in graph.in_degree()]),
             "degree_centrality_media": sum(list(nx.degree_centrality(graph).values()))/len(list(nx.degree_centrality(graph).values())),
             "eigenvector_centrality": sum(list(nx.eigenvector_centrality(graph, max_iter=100000).values()))/len(list(nx.eigenvector_centrality(graph, max_iter=100000))),
             "number_connected_components": nx.number_connected_components(unconnected_graph),
             "maxnodes_connected_components": unconnected_graph.subgraph(Gcc[0]).number_of_nodes(),
             "pagerank": sum(list(nx.pagerank(graph, alpha=0.9).values()))/len(list(nx.pagerank(graph, alpha=0.9).values())),
             "closeness_centrality": sum(list(nx.closeness_centrality(graph).values()))/len(list(nx.closeness_centrality(graph).values())),
             "indegree_centrality": sum(list(nx.in_degree_centrality(graph).values()))/len(list(nx.in_degree_centrality(graph).values())),
             "average_clustering":nx.average_clustering(graph),
             "radius_max_connected_components":nx.radius(unconnected_graph.subgraph(Gcc[0])),
             "diameter_max_connected_components":nx.diameter(unconnected_graph.subgraph(Gcc[0])),
             "perc_nodes_in_max_connected_component": unconnected_graph.subgraph(Gcc[0]).number_of_nodes()/graph.number_of_nodes(),
             "mean_eccentricity": sum(list(nx.eccentricity(unconnected_graph.subgraph(Gcc[0])).values()))/unconnected_graph.subgraph(Gcc[0]).number_of_nodes(),
             "avg_path_length": avg_shpath,
             "numero_ego_network": len(nnodes_ego),
             "max_numero_nodi_ego_network": max_nodes_ego,
             "mean_numero_nodi_ego_network": avg_nodes_ego
    }
    return stats

dataintervals={
    'nome_challenge':[],
    'intervallo':[],
    'numero_nodi':[],
    'numero_archi':[],
    'densità':[],
    'degree_centrality_media':[],
    'eigenvector_centrality':[],
    'numero_componenti_connesse':[],
    'numero_nodi_max_componente_connessa':[],
    'mean_degree':[],
    'mean_degree_std':[],
    'pagerank':[],
    'closeness_centrality':[],
    'average_clustering':[],
    'radius_max_connected_components':[],
    'diameter_max_connected_components':[],
    'indegree_centrality': [],
    "perc_nodes_in_max_connected_component": [],
    "mean_eccentricity": [],
    "avg_path_length": [],
    "numero_ego_network": [],
    "max_numero_nodi_ego_network": [],
    "mean_numero_nodi_ego_network": []}

df = pd.read_csv("dataset/intervals.csv")
df["points"] = df["points"].apply(literal_eval)
for index, row in df.iterrows():
    intervals = row['points']
    if intervals[0] != 0:
        intervals.insert(0, 0)
    if intervals[-1] != 100:
        intervals.append(100)
    for pairs in zip(intervals, intervals[1:]):
        print(pairs)
        graph, labels, colors, pos, _, _, df_int, lfd, _ = ntx.graphCalculation(row["challenge"],colorCriteria="createTime", lifespanCond=None, intervals=list(pairs), remAutoLikes=True)
        print(row["challenge"])
        challenge=(row["challenge"])
        if graph.number_of_nodes() == 0:
            continue
        gen_stats = graphStats(graph, _print=False)
        df_int["createTime"] = pd.to_datetime(df_int["createTime"]) # convert to datetime
        df_int = df_int.sort_values(by='createTime')
        # STATS = reset_stats()
        dataintervals["nome_challenge"].append(challenge)
        dataintervals["intervallo"].append(pairs)
        dataintervals["numero_nodi"].append(gen_stats["nnodes"])
        dataintervals["numero_archi"].append(gen_stats["nedges"])
        dataintervals["densità"].append(gen_stats["density"])
        dataintervals["degree_centrality_media"].append(gen_stats["degree_centrality_media"])
        dataintervals["eigenvector_centrality"].append(gen_stats["eigenvector_centrality"])
        dataintervals["numero_componenti_connesse"].append(gen_stats["number_connected_components"])
        dataintervals["numero_nodi_max_componente_connessa"].append(gen_stats["maxnodes_connected_components"])
        dataintervals["mean_degree"].append(gen_stats["mean_degree"])
        dataintervals["mean_degree_std"].append(str(np.std([x[1] for x in graph.in_degree()])))
        dataintervals["pagerank"].append(gen_stats["pagerank"])
        dataintervals["closeness_centrality"].append(gen_stats["closeness_centrality"])
        dataintervals["average_clustering"].append(gen_stats["average_clustering"])
        dataintervals["radius_max_connected_components"].append(gen_stats["radius_max_connected_components"])
        dataintervals["diameter_max_connected_components"].append(gen_stats["diameter_max_connected_components"])
        dataintervals["indegree_centrality"].append(gen_stats["indegree_centrality"])
        dataintervals["mean_eccentricity"].append(gen_stats["mean_eccentricity"])
        dataintervals["perc_nodes_in_max_connected_component"].append(gen_stats["perc_nodes_in_max_connected_component"])
        dataintervals["avg_path_length"].append(gen_stats["avg_path_length"])
        dataintervals["numero_ego_network"].append(gen_stats["numero_ego_network"])
        dataintervals["max_numero_nodi_ego_network"].append(gen_stats["max_numero_nodi_ego_network"])
        dataintervals["mean_numero_nodi_ego_network"].append(gen_stats["mean_numero_nodi_ego_network"])

dfdataintervals=pd.DataFrame.from_dict(dataintervals, orient='index')
dfdataintervals=dfdataintervals.transpose()
dfdataintervals.to_csv("dataset/dataintervals1.csv", sep=';', index=False)

