import pandas as pd
import lib.challenges as challenges
import lib.tiktok_network as nx
import numpy as np


POS_CHALLENGES = ["bussitchallenge",
                  "copinesdancechallenge",
                  "emojichallenge",
                  "itookanap"]
'''
                  "boredinthehouse",
                  "plankchallenge",
                  "makeupchallenge",
                  "colpiditesta"] # list of selected positive challenges
'''
NEG_CHALLENGES = ["silhouettechallenge"]
                 # "bugsbunnychallenge"] # list of selected negative challenges
ALL_CHALLENGES = [POS_CHALLENGES, NEG_CHALLENGES]

def reset_stats():
    return {"nnodes":[],
            "nedges":[],
            "mindegree":[],
            "moutdegree":[],
            "avgclust":[],
            "density":[],
            "5_lifespan":[],
            "25_lifespan":[],
            "50_lifespan":[],
            "75_lifespan":[],
            "video_duration":[],
            "stats_shareCount":[],
            "stats_commentCount":[],
            "stats_diggCount":[],
            "stats_playCount":[],
            "music_id_count":[]}

def print_results(arr, _type=False):
    text = "POSITIVE"
    if _type:
        text = "NEGATIVE"
    print("************************"+text+"************************")
    print("Mean number of nodes: " + str(np.mean(arr["nnodes"])) + " (std: " + str(np.std(arr["nnodes"])) + ")")
    print("Mean number of edges: " + str(np.mean(arr["nedges"])) + " (std: " + str(np.std(arr["nedges"])) + ")")
    print("Mean indegree: " + str(np.mean(arr["mindegree"])) + " (std: " + str(np.std(arr["mindegree"])) + ")")
    print("Mean outdegree: " + str(np.mean(arr["moutdegree"])) + " (std: " + str(np.std(arr["moutdegree"])) + ")")
    print("Mean clustering coefficient: " + str(np.mean(arr["avgclust"])) + " (std: " + str(np.std(arr["avgclust"])) + ")")
    print("Mean 5percent lifespan number of nodes: " + str(np.mean(arr["5_lifespan"])) + " (std: " + str(np.std(arr["5_lifespan"])) + ")")
    print("Mean 25percent lifespan number of nodes: " + str(np.mean(arr["25_lifespan"])) + " (std: " + str(np.std(arr["25_lifespan"])) + ")")
    print("Mean 50percent lifespan number of nodes: " + str(np.mean(arr["50_lifespan"])) + " (std: " + str(np.std(arr["50_lifespan"])) + ")")
    print("Mean 75percent lifespan number of nodes: " + str(np.mean(arr["75_lifespan"])) + " (std: " + str(np.std(arr["75_lifespan"])) + ")")
    print("Mean density: " + str(np.mean(arr["density"])) + " (std: " + str(np.std(arr["density"])) + ")")
    print("Mean video duration: " + str(np.mean(arr["video_duration"])) + " (std: " + str(np.std(arr["video_duration"])) + ")")
    print("Mean shares count: " + str(np.mean(arr["stats_shareCount"])) + " (std: " + str(np.std(arr["stats_shareCount"])) + ")")
    print("Mean likes count: " + str(np.mean(arr["stats_diggCount"])) + " (std: " + str(np.std(arr["stats_diggCount"])) + ")")
    print("Mean comments count: " + str(np.mean(arr["stats_commentCount"])) + " (std: " + str(np.std(arr["stats_commentCount"])) + ")")
    print("Mean views count: " + str(np.mean(arr["stats_playCount"])) + " (std: " + str(np.std(arr["stats_playCount"])) + ")")
    print("Mean different music count: " + str(np.mean(arr["music_id_count"])) + " (std: " + str(np.std(arr["music_id_count"])) + ")")
    print("********************************************************")

flag = False
for elem in ALL_CHALLENGES:
    STATS = reset_stats()
    for challenge in elem:
        df = pd.DataFrame()
        graph, _, _, _, nodestats = nx.graphCalculation(challenges.getChallenge(challenge)["name"].split(",")[0])
        gen_stats = nx.graphStats(graph, _print=False)
        for node in nodestats:
            df = df.append(nodestats[node], ignore_index=True)
        df["createTime"] = pd.to_datetime(df["createTime"]) # convert to datetime
        timedelta = df["createTime"].max() - df["createTime"].min()
        STATS["nnodes"].append(gen_stats["nnodes"])
        STATS["nedges"].append(gen_stats["nedges"])
        STATS["mindegree"].append(gen_stats["mindegree"])
        STATS["moutdegree"].append(gen_stats["moutdegree"])
        STATS["avgclust"].append(gen_stats["avgclust"])
        STATS["density"].append(gen_stats["density"])
        STATS["5_lifespan"].append(df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*5/100))].shape[0])
        STATS["25_lifespan"].append(df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*25/100))].shape[0])
        STATS["50_lifespan"].append(df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*50/100))].shape[0])
        STATS["75_lifespan"].append(df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*75/100))].shape[0])
        STATS["video_duration"].append(df["video_duration"].mean())
        STATS["stats_shareCount"].append(df["stats_shareCount"].mean())
        STATS["stats_diggCount"].append(df["stats_diggCount"].mean())
        STATS["stats_commentCount"].append(df["stats_commentCount"].mean())
        STATS["stats_playCount"].append(df["stats_playCount"].mean())
        STATS["music_id_count"].append(df['music_id'].value_counts().count())
    print_results(STATS, flag)
    flag = True