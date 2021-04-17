import pandas as pd
import lib.challenges as challenges
import lib.tiktok_network as nx
import numpy as np

POS_CHALLENGES = ["bussitchallenge",
                  "copinesdancechallenge",
                  "emojichallenge",
                  "itookanap",
                  "boredinthehouse",
                  "plankchallenge",
                  "makeupchallenge",
                  "colpiditesta"] # list of selected positive challenges
NEG_CHALLENGES = ["silhouettechallenge",
                  "bugsbunnychallenge"] # list of selected negative challenges

def reset_stats():
    return {"nnodes":[],
            "nedges":[],
            "mindegree":[],
            "moutdegree":[],
            "avgclust":[],
            "density":[],
            "video_duration":[],
            "stats_shareCount":[],
            "stats_commentCount":[],
            "stats_diggCount":[],
            "stats_playCount":[],
            "music_id_count":[]}

STATS = reset_stats()
for elem in POS_CHALLENGES:
    df = pd.DataFrame()
    graph, _, _, _, nodestats = nx.graphCalculation(challenges.getChallenge(elem)["name"].split(",")[0])
    gen_stats = nx.graphStats(graph, _print=False)
    for node in nodestats:
        df = df.append(nodestats[node], ignore_index=True)
    STATS["nnodes"].append(gen_stats["nnodes"])
    STATS["nedges"].append(gen_stats["nedges"])
    STATS["mindegree"].append(gen_stats["mindegree"])
    STATS["moutdegree"].append(gen_stats["moutdegree"])
    STATS["avgclust"].append(gen_stats["avgclust"])
    STATS["density"].append(gen_stats["density"])
    STATS["video_duration"].append(df["video_duration"].mean())
    STATS["stats_shareCount"].append(df["stats_shareCount"].mean())
    STATS["stats_diggCount"].append(df["stats_diggCount"].mean())
    STATS["stats_commentCount"].append(df["stats_commentCount"].mean())
    STATS["stats_playCount"].append(df["stats_playCount"].mean())
    STATS["music_id_count"].append(df['music_id'].value_counts().count())
