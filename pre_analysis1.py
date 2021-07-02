import pandas as pd
import lib.challenges as challenges
import lib.tiktok_network as ntx
import numpy as np
import networkx as nx
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

#POS_CHALLENGES_COND = [None, None, None, None, None, None, None]
#NEG_CHALLENGES_COND = [None, None, None, None, None, None, None]
ALL_CHALLENGES = [POS_CHALLENGES, NEG_CHALLENGES]
PLOTDENSITY = [[[] for x in POS_CHALLENGES],[[] for x in NEG_CHALLENGES]]
PLOTCOEFF = [[[] for x in POS_CHALLENGES],[[] for x in NEG_CHALLENGES]]
PLOTNCC = [[[] for x in POS_CHALLENGES],[[] for x in NEG_CHALLENGES]]

def reset_stats():
    return {"density": [[] for x in range(0,20)],
            "coeff": [[] for x in range(0,20)],
            "n_ccomponents": [[] for x in range(0,20)]}

def print_results(arr, _type=False):
    if _type:
        # for val in arr["density"]:
        #     for i in range(len(NEG_CHALLENGES)):
        #         PLOTDENSITY[1][i].append(val[i])
        # for val in arr["coeff"]:
        #     for i in range(len(NEG_CHALLENGES)):
        #         PLOTCOEFF[1][i].append(val[i])
        for val in arr["n_ccomponents"]:
            for i in range(len(NEG_CHALLENGES)):
                PLOTNCC[1][i].append(val[i])
    else:
        # for val in arr["density"]:
        #     for i in range(len(POS_CHALLENGES)):
        #         PLOTDENSITY[0][i].append(val[i])
        # for val in arr["coeff"]:
        #     for i in range(len(POS_CHALLENGES)):
        #         PLOTCOEFF[0][i].append(val[i])
        for val in arr["n_ccomponents"]:
            for i in range(len(POS_CHALLENGES)):
                PLOTNCC[0][i].append(val[i])
    return True
    
flag = False
# core_df = pd.DataFrame()
for elem in ALL_CHALLENGES:
    STATS = reset_stats()
    for challenge in elem:
        df_main = pd.DataFrame()
        df_main['in_degree'] = 0
        df_main['out_degree'] = 0
        for i in range(0,100,5):
            graph, _, _, _, _, _, _, _, dtemp = ntx.graphCalculation(challenges.getChallenge(challenge)["name"].split(",")[0], intervals = [0,i+5])
            if i == 95:
                for id_, value in graph.in_degree(): #influencer
                    if value > 2:
                        df_main = df_main.append(dtemp.loc[dtemp['author_id'].astype(np.int64) == id_].iloc[:])
                        df_main.loc[df_main['author_id'] == id_, ['in_degree']] = value
                for id_, value in graph.out_degree(): #influenced
                    if value > 2:
                        df_main = df_main.append(dtemp.loc[dtemp['author_id'].astype(np.int64) == id_].iloc[:])
                        df_main.loc[df_main['author_id'] == id_, ['out_degree']] = value
                df_main.drop_duplicates(subset ='author_id', keep = 'first', inplace = True)
                df_main['in_degree'] = df_main['in_degree'].replace(np.nan, 0)
                df_main['out_degree'] = df_main['out_degree'].replace(np.nan, 0)
                df_main = df_main.drop(['id','createTime','video_id','video_duration','music_id',
                'music_title','music_authorName','stats_diggCount','stats_shareCount',
                'stats_commentCount','stats_playCount','duetInfo_duetFromId','duetEnabled',
                'likedBy_id','likedBy_secUid','likedBy_uniqueId', 'author_secUid'], axis=1)
                df_main['author_id'] = df_main['author_id'].astype("string")
                df_main.to_csv('dataset/authors/' + challenge + '_inf.csv', sep=';', index=False)
            graph = graph.to_undirected()
            # c_number = list(nx.core_number(graph).values())
            # core_df = core_df.append({'challenge':challenge+str(i)+"/"+str(i+5),
            #                             "number_of_1_core":c_number.count(1),
            #                             "number_of_2_core": c_number.count(2),
            #                             "number_of_3_core":c_number.count(3),
            #                             "number_of_4_core":c_number.count(4)}, ignore_index=True)
            STATS['n_ccomponents'][int(round(i/5))].append(nx.number_connected_components(graph))

            '''
            STATS['density'][int(round(i/5))].append(nx.density(graph))
            if(graph.number_of_nodes() == 0):
                STATS['coeff'][int(round(i/5))].append(0)
            else:
                STATS['coeff'][int(round(i/5))].append(nx.average_clustering(graph))
            '''
    print_results(STATS, flag)
    flag = True
# core_df.to_csv("dataset/core_number_nodi.csv")
'''
#plotpos
for i in range(len(POS_CHALLENGES)):
    plt.title(POS_CHALLENGES[i]+" graph avg clustering coefficient (positive)")
    plt.ylabel("clustering coefficient")
    plt.xlabel("% lifespan")
    plt.xticks(range(0,101,5))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    plt.plot(range(0,101,5), [0]+PLOTCOEFF[0][i], label=POS_CHALLENGES[i])
    #    if point != 100:
    #        plt.axvline(x=point,color='r', linewidth=2)
    plt.savefig('images/pos_clust_'+POS_CHALLENGES[i]+'.png')
    plt.show()

for i in range(len(NEG_CHALLENGES)):
    plt.title(NEG_CHALLENGES[i]+" graph avg clustering coefficient (positive)")
    plt.ylabel("clustering coefficient")
    plt.xlabel("% lifespan")
    plt.xticks(range(0,101,5))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    plt.plot(range(0,101,5), [0]+PLOTCOEFF[1][i], label=NEG_CHALLENGES[i])
    #    if point != 100:
    #        plt.axvline(x=point,color='r', linewidth=2)
    plt.savefig('images/neg_clust_'+NEG_CHALLENGES[i]+'.png')
    plt.show()

for i in range(len(POS_CHALLENGES)):
    plt.title(POS_CHALLENGES[i]+" graph density (positive)")
    plt.ylabel("density")
    plt.xlabel("% lifespan")
    plt.xticks(range(0,101,5))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    plt.plot(range(0,101,5), [0]+PLOTDENSITY[0][i], label=POS_CHALLENGES[i])
    #    if point != 100:
    #        plt.axvline(x=point,color='r', linewidth=2)
    plt.savefig('images/pos_density_'+POS_CHALLENGES[i]+'.png')
    plt.show()

for i in range(len(NEG_CHALLENGES)):
    plt.title(NEG_CHALLENGES[i]+" graph density (positive)")
    plt.ylabel("density")
    plt.xlabel("% lifespan")
    plt.xticks(range(0,101,5))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    plt.plot(range(0,101,5), [0]+PLOTDENSITY[1][i], label=NEG_CHALLENGES[i])
    #    if point != 100:
    #        plt.axvline(x=point,color='r', linewidth=2)
    plt.savefig('images/neg_density_'+NEG_CHALLENGES[i]+'.png')
    plt.show()
'''
for i in range(len(POS_CHALLENGES)):
    plt.title(POS_CHALLENGES[i]+" number of connected components (positive)")
    plt.ylabel("number of connected components (normalized)")
    plt.xlabel("% lifespan")
    plt.xticks(range(0,101,5))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    plt.plot(range(0,101,5), [0]+[x / max(PLOTNCC[0][i]) for x in PLOTNCC[0][i]], label=POS_CHALLENGES[i])
    #    if point != 100:
    #        plt.axvline(x=point,color='r', linewidth=2)
    plt.savefig('images/pos_ncc_'+POS_CHALLENGES[i]+'.png')
    plt.show()

for i in range(len(NEG_CHALLENGES)):
    plt.title(NEG_CHALLENGES[i]+" number of connected components (positive)")
    plt.ylabel("number of connected components (normalized)")
    plt.xlabel("% lifespan")
    plt.xticks(range(0,101,5))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    plt.plot(range(0,101,5), [0]+[x / max(PLOTNCC[1][i]) for x in PLOTNCC[1][i]], label=NEG_CHALLENGES[i])
    #    if point != 100:
    #        plt.axvline(x=point,color='r', linewidth=2)
    plt.savefig('images/neg_ncc_'+NEG_CHALLENGES[i]+'.png')
    plt.show()