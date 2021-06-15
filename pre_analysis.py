import pandas as pd
import lib.challenges as challenges
import lib.tiktok_network as nx
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval

POS_CHALLENGES = ["bussitchallenge",
                  "copinesdancechallenge",
                  "emojichallenge",
                  "colpiditesta",
                  "boredinthehouse",
                  "ITookANap",
                  "plankchallenge"] # list of selected positive challenges

NEG_CHALLENGES = ["silhouettechallenge",
                  "bugsbunny",
                  "strippatiktok",
                  "firewroks",
                  "fightchallenge",
                  "updownchallenge",
                  "sugarbaby"] #list of selected negative challenges

POS_CHALLENGES_COND = [None, None, None, None, None, None, None]
NEG_CHALLENGES_COND = [None, None, None, None, None, None, None]
ALL_CHALLENGES = [POS_CHALLENGES, NEG_CHALLENGES]
PLOT = [[],[]]
PLOTPOS = [[] for x in POS_CHALLENGES]
PLOTNEG = [[] for x in NEG_CHALLENGES]
PLOTCOUNT = [[],[]]
PLOTPOSCOUNT = [[] for x in POS_CHALLENGES]
PLOTNEGCOUNT = [[] for x in NEG_CHALLENGES]
PLOTPOSMEANLIKESCOUNT = [[] for x in POS_CHALLENGES]
PLOTNEGMEANLIKESCOUNT = [[] for x in NEG_CHALLENGES]
PLOTPOSVIDEOCOUNT = [[] for x in POS_CHALLENGES]
PLOTNEGVIDEOCOUNT = [[] for x in NEG_CHALLENGES]
PLOTPOSFOLLOWINGCOUNT = [[] for x in POS_CHALLENGES]
PLOTNEGFOLLOWINGCOUNT = [[] for x in NEG_CHALLENGES]

def reset_stats():
    return {"span":[[] for x in range(0,100)],
            "n_nodes":[[] for x in range(0,100)],
            "mlikes":[[] for x in range(0,20)],
            "n_video":[[] for x in range(0,20)],
            "following":[[] for x in range(0,20)],
            "nnodes":[],
            "nedges":[],
            "mindegree":[],
            "moutdegree":[],
            "avgclust":[],
            "density":[],
            "lifespan":[],
            "5_lifespan":[],
            "25_lifespan":[],
            "50_lifespan":[],
            "75_lifespan":[],
            "video_duration":[],
            "stats_shareCount":[],
            "stats_commentCount":[],
            "stats_diggCount":[],
            "stats_playCount":[],
            "music_id_count":[],
            "authorStats_diggCount":[],
            "authorStats_followingCount":[],
            "authorStats_heartCount":[],
            "authorStats_followerCount":[],
            "authorStats_videoCount":[]}
def print_results(arr, _type=False):
    text = "POSITIVE"
    if _type:
        text = "NEGATIVE"
        for val in arr["span"]:
            PLOT[1].append(np.mean(val))
            for i in range(len(NEG_CHALLENGES)):
                PLOTNEG[i].append(val[i])
        for val in arr["n_nodes"]:
            PLOTCOUNT[1].append(np.mean(val))
            for i in range(len(NEG_CHALLENGES)):
                PLOTNEGCOUNT[i].append(val[i])
        for val in arr["mlikes"]:
            for i in range(len(NEG_CHALLENGES)):
                PLOTNEGMEANLIKESCOUNT[i].append(val[i])
        for val in arr["n_video"]:
            for i in range(len(NEG_CHALLENGES)):
                PLOTNEGVIDEOCOUNT[i].append(val[i])
        for val in arr["following"]:
            for i in range(len(NEG_CHALLENGES)):
                PLOTNEGFOLLOWINGCOUNT[i].append(val[i])
    else:
        for val in arr["span"]:
            PLOT[0].append(np.mean(val))
            for i in range(len(POS_CHALLENGES)):
                PLOTPOS[i].append(val[i])
        for val in arr["n_nodes"]:
            PLOTCOUNT[0].append(np.mean(val))
            for i in range(len(POS_CHALLENGES)):
                PLOTPOSCOUNT[i].append(val[i])
        for val in arr["mlikes"]:
            for i in range(len(POS_CHALLENGES)):
                PLOTPOSMEANLIKESCOUNT[i].append(val[i])
        for val in arr["n_video"]:
            for i in range(len(POS_CHALLENGES)):
                PLOTPOSVIDEOCOUNT[i].append(val[i])
        for val in arr["following"]:
            for i in range(len(POS_CHALLENGES)):
                PLOTPOSFOLLOWINGCOUNT[i].append(val[i])
    print("************************"+text+"************************")
    print("Mean number of nodes: " + str(np.mean(arr["nnodes"])) + " (std: " + str(np.std(arr["nnodes"])) + ")")
    print("Mean number of edges: " + str(np.mean(arr["nedges"])) + " (std: " + str(np.std(arr["nedges"])) + ")")
    print("Mean indegree: " + str(np.mean(arr["mindegree"])) + " (std: " + str(np.std(arr["mindegree"])) + ")")
    print("Mean outdegree: " + str(np.mean(arr["moutdegree"])) + " (std: " + str(np.std(arr["moutdegree"])) + ")")
    print("Mean clustering coefficient: " + str(np.mean(arr["avgclust"])) + " (std: " + str(np.std(arr["avgclust"])) + ")")
    print("Mean lifespan (days): " + str(np.mean(arr["lifespan"])) + " (std: " + str(np.std(arr["lifespan"])) + ")")
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
    print("Mean likes given by the author count: " + str(np.mean(arr["authorStats_diggCount"])) + " (std: " + str(np.std(arr["authorStats_diggCount"])) + ")")
    print("Mean author following count: " + str(np.mean(arr["authorStats_followingCount"])) + " (std: " + str(np.std(arr["authorStats_followingCount"])) + ")")
    print("Mean likes received by the author count: " + str(np.mean(arr["authorStats_heartCount"])) + " (std: " + str(np.std(arr["authorStats_heartCount"])) + ")")
    print("Mean author follower count: " + str(np.mean(arr["authorStats_followerCount"])) + " (std: " + str(np.std(arr["authorStats_followerCount"])) + ")")
    print("Mean published videos by the author count: " + str(np.mean(arr["authorStats_videoCount"])) + " (std: " + str(np.std(arr["authorStats_videoCount"])) + ")")
    print("********************************************************")

flag = False
counter = 0
for elem in ALL_CHALLENGES:
    STATS = reset_stats()
    for challenge in elem:
        if not flag:
            cond = POS_CHALLENGES_COND[counter]
        else:
            cond = NEG_CHALLENGES_COND[counter]
        df = pd.DataFrame()
        graph, _, _, _, nodestats, df, _, _ = nx.graphCalculation(challenges.getChallenge(challenge)["name"].split(",")[0], lifespanCond=cond)
        gen_stats = nx.graphStats(graph, _print=False)
        #for node in nodestats:
        #    df = df.append(nodestats[node], ignore_index=True)
        df["createTime"] = pd.to_datetime(df["createTime"]) # convert to datetime
        timedelta = df["createTime"].max() - df["createTime"].min()
        incr = 0
        for i in range(0,100):
            STATS["span"][i].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta/100 * (i+1)))].shape[0])/gen_stats["nnodes"])
            mask = (df["createTime"] <= (df["createTime"].min() + (timedelta/100 * (i+1)))) & (df["createTime"] >= (df["createTime"].min() + (timedelta/100 * i)))
            STATS["n_nodes"][i].append(df.loc[mask].shape[0])
        for i in range(0,100,5):
            mask = (df["createTime"] <= (df["createTime"].min() + (timedelta/100 * (i+5)))) & (df["createTime"] >= (df["createTime"].min() + (timedelta/100 * i)))
            if not np.isnan(df.loc[mask]["stats_diggCount"].mean()):
                STATS["mlikes"][int(round(i/5))].append(df.loc[mask]["stats_diggCount"].mean())
            else:
                STATS["mlikes"][int(round(i/5))].append(0)
            if not np.isnan(df.loc[mask]["authorStats_followingCount"].sum()):
                STATS["following"][int(round(i/5))].append(df.loc[mask]["authorStats_followingCount"].sum())
            else:
                STATS["following"][int(round(i/5))].append(0)
            STATS["n_video"][int(round(i/5))].append(df.loc[mask].shape[0])
        STATS["nnodes"].append(gen_stats["nnodes"])
        STATS["nedges"].append(gen_stats["nedges"])
        STATS["mindegree"].append(gen_stats["mindegree"])
        STATS["moutdegree"].append(gen_stats["moutdegree"])
        STATS["avgclust"].append(gen_stats["avgclust"])
        STATS["density"].append(gen_stats["density"])
        STATS["lifespan"].append(timedelta.days)
        STATS["5_lifespan"].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta/100 * 5))].shape[0])/gen_stats["nnodes"])
        STATS["25_lifespan"].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta/100 * 25))].shape[0])/gen_stats["nnodes"])
        STATS["50_lifespan"].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta/100 * 50))].shape[0])/gen_stats["nnodes"])
        STATS["75_lifespan"].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta/100 * 75))].shape[0])/gen_stats["nnodes"])
        STATS["video_duration"].append(df["video_duration"].mean())
        STATS["stats_shareCount"].append(df["stats_shareCount"].mean())
        STATS["stats_diggCount"].append(df["stats_diggCount"].mean())
        STATS["stats_commentCount"].append(df["stats_commentCount"].mean())
        STATS["stats_playCount"].append(df["stats_playCount"].mean())
        STATS["music_id_count"].append(df['music_id'].value_counts().count())
        STATS["authorStats_diggCount"].append(df["authorStats_diggCount"].mean())
        STATS["authorStats_followingCount"].append(df["authorStats_followingCount"].mean())
        STATS["authorStats_heartCount"].append(df["authorStats_heartCount"].mean())
        STATS["authorStats_followerCount"].append(df["authorStats_followerCount"].mean())
        STATS["authorStats_videoCount"].append(df["authorStats_videoCount"].mean())
        counter += 1
    print_results(STATS, flag)
    flag = True
    counter = 0

intervals = pd.read_csv('dataset/intervals.csv', sep=',')

#plotpos

for i in range(len(POS_CHALLENGES)):
    int_ = intervals.loc[intervals['challenge'] == POS_CHALLENGES[i]].iloc[:].values[0]
    plt.title(POS_CHALLENGES[i]+" graph's expansion (positive)")
    plt.ylabel("mean number of nodes")
    plt.xlabel("% trend's lifespan")
    plt.xticks(range(0,101,5))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    plt.plot(range(0,101,5), [0]+PLOTPOSFOLLOWINGCOUNT[i], label=POS_CHALLENGES[i]) #PLOTPOSCOUNT
    for point in literal_eval(int_[2]):
        if point != 100:
            plt.axvline(x=point,color='r', linewidth=2)
    plt.show()

#plotneg

for i in range(len(NEG_CHALLENGES)):
    int_ = intervals.loc[intervals['challenge'] == NEG_CHALLENGES[i]].iloc[:].values[0]
    plt.title(NEG_CHALLENGES[i]+" graph's expansion (negative)")
    plt.ylabel("mean number of nodes")
    plt.xlabel("% trend's lifespan")
    plt.xticks(range(0,101,5))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    plt.plot(range(0,101,5), [0]+PLOTNEGFOLLOWINGCOUNT[i], label=NEG_CHALLENGES[i]) #PLOTNEGCOUNT
    for point in literal_eval(int_[2]):
        if point != 100:
            plt.axvline(x=point, color='r', linewidth=2)
    plt.show()
