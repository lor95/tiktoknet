import pandas as pd
from ast import literal_eval
import lib.tiktok_network as ntx
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def graphStats(graph, _print=True):
    stats = {"nnodes":graph.number_of_nodes(),
             "nedges":graph.number_of_edges(),
             "density":nx.density(graph),
             "degree_centrality_media": sum(list(nx.degree_centrality(graph).values()))/len(list(nx.degree_centrality(graph).values())),
             "eigenvector_centrality": sum(list(nx.eigenvector_centrality(graph, max_iter=100000)))/len(list(nx.eigenvector_centrality(graph, max_iter=100000)))
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
    'numero_video':[]}

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
            "numero_video":[]
            }

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
    print("********************************************************")

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
        graph, labels, colors, pos, _, _, df_int = ntx.graphCalculation(row["challenge"],colorCriteria="createTime", lifespanCond=None, intervals=list(pairs), remAutoLikes=True)
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
        print_results(STATS)
dfdataintervals=pd.DataFrame.from_dict(dataintervals, orient='index')
dfdataintervals=dfdataintervals.transpose()
dfdataintervals.to_csv("dataset/dataintervals.csv", sep=';', index=False)
