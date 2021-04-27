import pandas as pd
import lib.challenges as challenges
import lib.tiktok_network as nx
import numpy as np
import matplotlib.pyplot as plt


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
ALL_CHALLENGES = [POS_CHALLENGES, NEG_CHALLENGES]
PLOT = [[],[]]
PLOTPOS = [[],[],[],[],[],[],[]]
PLOTNEG = [[],[],[],[],[],[],[]]

def reset_stats():
    return {"span":[[] for x in range(0,100)],
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
            for i in range (0,6):
                PLOTNEG[i].append(val[i])
    else:
        for val in arr["span"]:
            PLOT[0].append(np.mean(val))
            for i in range (0,6):
                PLOTPOS[i].append(val[i])
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
        for i in range(0,100):
            STATS["span"][i].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*(i+1)/100))].shape[0])/gen_stats["nnodes"])
        STATS["nnodes"].append(gen_stats["nnodes"])
        STATS["nedges"].append(gen_stats["nedges"])
        STATS["mindegree"].append(gen_stats["mindegree"])
        STATS["moutdegree"].append(gen_stats["moutdegree"])
        STATS["avgclust"].append(gen_stats["avgclust"])
        STATS["density"].append(gen_stats["density"])
        STATS["lifespan"].append(timedelta.days)
        STATS["5_lifespan"].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*5/100))].shape[0])/gen_stats["nnodes"])
        STATS["25_lifespan"].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*25/100))].shape[0])/gen_stats["nnodes"])
        STATS["50_lifespan"].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*50/100))].shape[0])/gen_stats["nnodes"])
        STATS["75_lifespan"].append((df.loc[df["createTime"] <= (df["createTime"].min() + (timedelta*75/100))].shape[0])/gen_stats["nnodes"])
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
    print_results(STATS, flag)
    flag = True

# plot
plt.title("TikTok graph's expansion")
plt.ylabel("mean number of nodes (normalized)")
plt.xlabel("% trend's lifespan")
plt.xticks(range(0,101,5))
plt.grid("--")
plt.gca().set_ylim(ymin=0, ymax=1)
plt.gca().set_xlim(xmin=0, xmax=100)
plt.plot(range(1,101), PLOT[0])
plt.plot(range(1,101), PLOT[1])
plt.legend(["positive trend's graph expansion", "negative trend's graph expansion"])
plt.show()

#plotpos
plt.title("TikTok graph's expansion (positive challenges)")
plt.ylabel("mean number of nodes (normalized)")
plt.xlabel("% trend's lifespan")
plt.xticks(range(0,101,5))
plt.grid("--")
plt.gca().set_ylim(ymin=0, ymax=1)
plt.gca().set_xlim(xmin=0, xmax=100)
for i in range (0,6):
    plt.plot(range(1,101), PLOTPOS[i], label=POS_CHALLENGES[i])
plt.plot(range(1,101), PLOT[0], linestyle='dashed', color='red', label='mean positive challenges graph expansion') #add mean positive dashed line
#plt.legend(["positive trend's graph expansion", "mean positive trend's graph expansion"])
plt.legend()
plt.show()

#plotneg
plt.title("TikTok graph's expansion (negative challenges)")
plt.ylabel("mean number of nodes (normalized)")
plt.xlabel("% trend's lifespan")
plt.xticks(range(0,101,5))
plt.grid("--")
plt.gca().set_ylim(ymin=0, ymax=1)
plt.gca().set_xlim(xmin=0, xmax=100)
for i in range (0,6):
    plt.plot(range(1,101), PLOTNEG[i], label=NEG_CHALLENGES[i])
plt.plot(range(1,101), PLOT[1], linestyle='dashed', color='red', label='mean negative challenges graph expansion') 
#plt.legend(["negative trend's graph expansion", "mean negative trend's graph expansion"])
plt.legend()
plt.show()