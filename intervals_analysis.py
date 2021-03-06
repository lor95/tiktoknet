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
    stats = {"nnodes":graph.number_of_nodes(),
             "nedges":graph.number_of_edges(),
             "density":nx.density(graph),
             "mindegree":np.mean([x[1] for x in graph.in_degree()]),
             "degree_centrality_media": sum(list(nx.degree_centrality(graph).values()))/len(list(nx.degree_centrality(graph).values())),
             "eigenvector_centrality": sum(list(nx.eigenvector_centrality(graph, max_iter=100000).values()))/len(list(nx.eigenvector_centrality(graph, max_iter=100000))),
             "number_connected_components": number_connected_components(unconnected_graph),
             "maxnodes_connected_components": unconnected_graph.subgraph(Gcc[0]).number_of_nodes(),
             "pagerank": sum(list(nx.pagerank(graph, alpha=0.9).values()))/len(list(nx.pagerank(graph, alpha=0.9).values())),
             "closeness_centrality": sum(list(nx.closeness_centrality(graph).values()))/len(list(nx.closeness_centrality(graph).values())),
             "betweenness_centrality": sum(list(nx.betweenness_centrality(graph).values()))/len(list(nx.betweenness_centrality(graph).values())),
             "average_clustering":nx.average_clustering(graph),
             "radius_max_connected_components":nx.radius(unconnected_graph.subgraph(Gcc[0])),
             "diameter_max_connected_components":nx.diameter(unconnected_graph.subgraph(Gcc[0]))
    }
    return stats

dataintervals={
    'nome_challenge':[],
    'intervallo':[],
    'numero_nodi':[],
    'numero_archi':[],
    'densità':[],
    'likes_totali_int':[],
    'numero_medio_likes':[],
    'numero_medio_likes_std':[],
    'numero_medio_commenti':[],
    'numero_medio_commenti_std':[],
    'numero_medio_condivisioni':[],
    'numero_medio_condivisioni_std':[],
    'numero_medio_views':[],
    'numero_medio_views_std':[],
    'likes_ricevuti_autore':[],
    'likes_ricevuti_autore_std':[],
    'follower_autore':[],
    'follower_autore_std':[],
    'following_autore':[],
    'following_autore_std':[],
    'degree_centrality_media':[],
    'eigenvector_centrality':[],
    'numero_video':[],
    'numero_utenti_verificati':[],
    'numero_componenti_connesse':[],
    'maxnodi_componenti_connesse':[],
    'lifespan':[],
    'mindegree':[],
    'mindegree_std':[],
    'pagerank':[],
    'closeness_centrality':[],
    'betweenness_centrality':[],
    'average_clustering':[],
    'radius_max_connected_components':[],
    'diameter_max_connected_components':[]}

def reset_stats():
    return {"nnodes":[],
            "nedges":[],
            "density":[],
            "stats_diggCount_tot":[],
            "stats_diggCount":[],
            "stats_commentCount":[],
            "stats_playCount":[],
            "stats_shareCount":[],
            "authorStats_diggCount":[],
            "authorStats_followingCount":[],
            "authorStats_heartCount":[],
            "authorStats_followerCount":[],
            "degree_centrality_media":[],
            "eigenvector_centrality":[],
            "numero_video":[],
            "numero_utenti_verificati":[],
            "numero_componenti_connesse":[],
            "maxnodi_componenti_connesse":[],
            "lifespan":[],
            "mindegree":[],
            "pagerank":[],
            "closeness_centrality":[],
            "betweenness_centrality":[],
            "average_clustering":[],
            "radius_max_connected_components":[],
            "diameter_max_connected_components":[]}

def print_results(arr, _type=False): 
    print("Mean number of nodes: " + str(np.mean(arr["nnodes"]))) 
    print("Mean number of edges: " + str(np.mean(arr["nedges"])))
    print("Mean density: " + str(np.mean(arr["density"])))
    print("Total likes count: " + str(np.sum(arr["stats_diggCount_tot"])))
    print("Mean shares count: " + str(np.mean(arr["stats_shareCount"])) + " (std: " + str(np.std(arr["stats_shareCount"])) + ")")
    print("Mean likes count: " + str(np.mean(arr["stats_diggCount"])) + " (std: " + str(np.std(arr["stats_diggCount"])) + ")")
    print("Mean comments count: " + str(np.mean(arr["stats_commentCount"])) + " (std: " + str(np.std(arr["stats_commentCount"])) + ")")
    print("Mean views count: " + str(np.mean(arr["stats_playCount"])) + " (std: " + str(np.std(arr["stats_playCount"])) + ")")
    print("Mean likes given by the author count: " + str(np.mean(arr["authorStats_diggCount"])) + " (std: " + str(np.std(arr["authorStats_diggCount"])) + ")")
    print("Mean author following count: " + str(np.mean(arr["authorStats_followingCount"])) + " (std: " + str(np.std(arr["authorStats_followingCount"])) + ")")
    print("Mean likes received by the author count: " + str(np.mean(arr["authorStats_heartCount"])) + " (std: " + str(np.std(arr["authorStats_heartCount"])) + ")")
    print("Mean author follower count: " + str(np.mean(arr["authorStats_followerCount"])) + " (std: " + str(np.std(arr["authorStats_followerCount"])) + ")")
    print("Degree centrality: " + str(arr["degree_centrality_media"]))
    print("Eigenvector centrality: " + str(arr["eigenvector_centrality"]))
    print("Number of videos: " + str(np.count_nonzero(arr["numero_video"])))
    print("Number of verified users: "+ str(np.count_nonzero(arr["numero_utenti_verificati"])))
    print("Number of connected components: " + str(arr["numero_componenti_connesse"]))
    print("Max number of nodes in connected components: " + str(arr["maxnodi_componenti_connesse"]))
    print("Lifespan: " + str(np.mean(arr["lifespan"])))
    print("Mean indegree: " + str(np.mean(arr["mindegree"])) +  " (std: " + str(np.std([x[1] for x in graph.in_degree()]))+ ")")
    print("Pagerank: "+str(np.mean(arr["pagerank"])))
    print("Closeness Centrality: " + str(np.mean(arr["closeness_centrality"])))
    print("Betweenness Centrality: " + str(np.mean(arr["betweenness_centrality"])))
    print("Average Clustering: " + str(np.mean(arr["average_clustering"])))
    print("Radius max connected components: " + str(np.mean(arr["radius_max_connected_components"])))
    print("Diameter max connected components: " + str(np.mean(arr["diameter_max_connected_components"])))
    print("********************************************************")
numero_video = 0
vid = []
std_times = []
mean_times = []
df = pd.read_csv("dataset/intervals.csv")
df["points"] = df["points"].apply(literal_eval)
for index, row in df.iterrows():
    intervals = row['points']
    if intervals[0] != 0:
        intervals.insert(0, 0)
    if intervals[-1] != 100:
        intervals.append(100)
    for pairs in zip(intervals, intervals[1:]):
        plt.figure(figsize=(15,15))
        print(pairs)
        graph, labels, colors, pos, _, _, df_int, lfd, _ = ntx.graphCalculation(row["challenge"],colorCriteria="createTime", lifespanCond=None, intervals=list(pairs), remAutoLikes=True)
        print(row["challenge"])
        challenge=(row["challenge"])
        nx.draw_networkx_nodes(graph,pos,node_color=colors,node_size=60)     
        nx.draw_networkx_labels(graph, pos, labels,font_size=5)
        nx.draw_networkx_edges(graph,pos,arrows=True,arrowsize=3,arrowstyle="-|>",alpha=0.5)#edge_color='lightgrey'   
        ax= plt.gca()
        try:
            ax.collections[0].set_edgecolor("#000000")
        except:
            continue
        #plt.show()
        gen_stats = graphStats(graph, _print=False)
        df_int["createTime"] = pd.to_datetime(df_int["createTime"]) # convert to datetime
        df_int = df_int.sort_values(by='createTime')
        timedelta = df_int["createTime"].max() - df_int["createTime"].min()
        STATS = reset_stats()
        STATS["nnodes"].append(gen_stats["nnodes"])
        STATS["nedges"].append(gen_stats["nedges"])
        STATS["density"].append(gen_stats["density"])
        STATS["degree_centrality_media"].append(gen_stats["degree_centrality_media"])
        STATS["eigenvector_centrality"].append(gen_stats["eigenvector_centrality"])
        STATS["stats_diggCount_tot"].append(df_int["stats_diggCount"])
        STATS["stats_diggCount"].append(df_int["stats_diggCount"])
        STATS["stats_commentCount"].append(df_int["stats_commentCount"])
        STATS["stats_playCount"].append(df_int["stats_playCount"])
        STATS["stats_shareCount"].append(df_int["stats_shareCount"])
        STATS["authorStats_diggCount"].append(df_int["authorStats_diggCount"])
        STATS["authorStats_followingCount"].append(df_int["authorStats_followingCount"])
        STATS["authorStats_followerCount"].append(df_int["authorStats_followerCount"])
        STATS["authorStats_heartCount"].append(df_int["authorStats_heartCount"])  
        STATS["numero_video"].append(df_int["id"])
        STATS["numero_utenti_verificati"].append(np.where(df_int["author_verified"])[0])
        STATS["numero_componenti_connesse"].append(gen_stats["number_connected_components"])
        STATS["maxnodi_componenti_connesse"].append(gen_stats["maxnodes_connected_components"])
        STATS["lifespan"].append(timedelta.days)
        STATS["mindegree"].append(gen_stats["mindegree"])
        STATS["pagerank"].append(gen_stats["pagerank"])
        STATS["closeness_centrality"].append(gen_stats["closeness_centrality"])
        STATS["betweenness_centrality"].append(gen_stats["betweenness_centrality"])
        STATS["average_clustering"].append(gen_stats["average_clustering"])
        STATS["radius_max_connected_components"].append(gen_stats["radius_max_connected_components"])
        STATS["diameter_max_connected_components"].append(gen_stats["diameter_max_connected_components"])
        dataintervals["nome_challenge"].append(challenge)
        dataintervals["intervallo"].append(pairs)
        dataintervals["numero_nodi"].append(gen_stats["nnodes"])
        dataintervals["numero_archi"].append(gen_stats["nedges"])
        dataintervals["densità"].append(gen_stats["density"])
        dataintervals["degree_centrality_media"].append(gen_stats["degree_centrality_media"])
        dataintervals["eigenvector_centrality"].append(gen_stats["eigenvector_centrality"])
        dataintervals["likes_totali_int"].append(df_int["stats_diggCount"].sum())
        dataintervals["numero_medio_likes"].append(df_int["stats_diggCount"].mean())
        dataintervals["numero_medio_likes_std"].append(np.std(df_int["stats_diggCount"]))
        dataintervals["numero_medio_commenti"].append(df_int["stats_commentCount"].mean())
        dataintervals["numero_medio_commenti_std"].append(np.std(df_int["stats_commentCount"]))
        dataintervals["numero_medio_condivisioni"].append(df_int["stats_shareCount"].mean())
        dataintervals["numero_medio_condivisioni_std"].append(np.std(df_int["stats_shareCount"]))
        dataintervals["numero_medio_views"].append(df_int["stats_playCount"].mean())
        dataintervals["numero_medio_views_std"].append(np.std(df_int["stats_playCount"]))
        dataintervals["likes_ricevuti_autore"].append(df_int["authorStats_heartCount"].mean())
        dataintervals["likes_ricevuti_autore_std"].append(np.std(df_int["authorStats_heartCount"]))
        dataintervals["follower_autore"].append(df_int["authorStats_followerCount"].mean())
        dataintervals["follower_autore_std"].append(np.std(df_int["authorStats_followerCount"]))
        dataintervals["following_autore"].append(df_int["authorStats_followingCount"].mean())
        dataintervals["following_autore_std"].append(np.std(df_int["authorStats_followingCount"]))
        dataintervals["numero_video"].append(df_int["id"].count())
        dataintervals["numero_utenti_verificati"].append(np.count_nonzero(np.where(df_int["author_verified"])[0]))
        dataintervals["numero_componenti_connesse"].append(gen_stats["number_connected_components"])
        dataintervals["maxnodi_componenti_connesse"].append(gen_stats["maxnodes_connected_components"])
        dataintervals["lifespan"].append(lfd)
        dataintervals["mindegree"].append(gen_stats["mindegree"])
        dataintervals["mindegree_std"].append(str(np.std([x[1] for x in graph.in_degree()])))
        dataintervals["pagerank"].append(gen_stats["pagerank"])
        dataintervals["closeness_centrality"].append(gen_stats["closeness_centrality"])
        dataintervals["betweenness_centrality"].append(gen_stats["betweenness_centrality"])
        dataintervals["average_clustering"].append(gen_stats["average_clustering"])
        dataintervals["radius_max_connected_components"].append(gen_stats["radius_max_connected_components"])
        dataintervals["diameter_max_connected_components"].append(gen_stats["diameter_max_connected_components"])
        if pairs[0] == 0:
            numero_video = df_int["id"].count()
            vid.append(numero_video)
            #times.append(0)
        else:  
            numero_video = df_int["id"].count() - numero_video
            vid.append(numero_video)
            numero_video = df_int["id"].count()
            #times.append(df_int['createTime'] - prev_time)
        
        times = []
        prev_time = 0
        fl = True
        for index1,row1 in df_int.iterrows():
            if fl:
                times.append(0)
            else:
                times.append((row1["createTime"]-prev_time)/ pd.Timedelta('1 hour'))
            prev_time = row1["createTime"]
            fl = False
        #print(times)
        mean_times.append(np.mean(times))
        std_times.append(np.std(times))
        print_results(STATS)
dfdataintervals=pd.DataFrame.from_dict(dataintervals, orient='index')
dfdataintervals=dfdataintervals.transpose()
dfdataintervals["diff_num_video_interv_prec"] = vid
dfdataintervals["hours_between_mean"] = mean_times
dfdataintervals["hours_between_std"] = std_times
dfdataintervals.to_csv("dataset/dataintervals.csv", sep=';', index=False)

