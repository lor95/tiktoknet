import pandas as pd
import lib.challenges as challenges
import lib.tiktok_network as ntx
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

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
PLOTNODES = [[[] for x in POS_CHALLENGES],[[] for x in NEG_CHALLENGES]]

def reset_stats():
    return {"density": [[] for x in range(0,20)],
            "coeff": [[] for x in range(0,20)],
            "n_ccomponents": [[] for x in range(0,20)],
            "n_nodes%": [[] for x in range(0, 10)]}

def print_results(arr, _type=False):
    if _type:
        # for val in arr["density"]:
        #     for i in range(len(NEG_CHALLENGES)):
        #         PLOTDENSITY[1][i].append(val[i])
        # for val in arr["coeff"]:
        #     for i in range(len(NEG_CHALLENGES)):
        #         PLOTCOEFF[1][i].append(val[i])
        # for val in arr["n_ccomponents"]:
        #     for i in range(len(NEG_CHALLENGES)):
        #         PLOTNCC[1][i].append(val[i])
        for val in arr["n_nodes%"]:
            for i in range(len(NEG_CHALLENGES)):
                PLOTNODES[1][i].append(val[i])
    else:
        # for val in arr["density"]:
        #     for i in range(len(POS_CHALLENGES)):
        #         PLOTDENSITY[0][i].append(val[i])
        # for val in arr["coeff"]:
        #     for i in range(len(POS_CHALLENGES)):
        #         PLOTCOEFF[0][i].append(val[i])
        # for val in arr["n_ccomponents"]:
        #     for i in range(len(POS_CHALLENGES)):
        #         PLOTNCC[0][i].append(val[i])
        for val in arr["n_nodes%"]:
            for i in range(len(POS_CHALLENGES)):
                PLOTNODES[0][i].append(val[i])
    return True
    
flag = False
core_df = pd.DataFrame()
for elem in ALL_CHALLENGES:
    STATS = reset_stats()
    for challenge in elem:
        df_main = pd.DataFrame()
        df_main['in_degree'] = 0
        df_main['out_degree'] = 0
        maingraph, _, _, _, _, _, _, _, dtemp = ntx.graphCalculation(challenges.getChallenge(challenge)["name"].split(",")[0])
        a = nx.in_degree_centrality(maingraph)
        list_a = list(a.values())
        val = 'positive'
        if flag:
            val = 'negative'
        print(max(list_a))
        bin1 = len([item for item in list_a if (item >= 0 and item <= 0.005)])
        bin2 = len([item for item in list_a if (item > 0.005 and item <= 0.01)])
        bin3 = len([item for item in list_a if (item > 0.01 and item <= 0.015)])
        bin4 = len([item for item in list_a if (item > 0.015 and item <= 0.02)])
        bin5 = len([item for item in list_a if (item > 0.02 and item <= 0.025)])
        bin6 = len([item for item in list_a if (item > 0.025 and item <= 0.03)])
        bin7 = len([item for item in list_a if (item > 0.03 and item <= 0.035)])
        bin8 = len([item for item in list_a if (item > 0.035 and item <= 0.04)])
        bin9 = len([item for item in list_a if (item > 0.04 and item <= 0.045)])
        bin10 = len([item for item in list_a if (item > 0.045 and item <= 0.05)])
        bin11 = len([item for item in list_a if (item > 0.05 and item <= 0.055)])
        bin12 = len([item for item in list_a if (item > 0.055 and item <= 0.06)])
        bin13 = len([item for item in list_a if (item > 0.06 and item <= 0.065)])
        bin14 = len([item for item in list_a if (item > 0.065 and item <= 0.07)])
        bin15 = len([item for item in list_a if (item > 0.07 and item <= 0.075)])
        bin16 = len([item for item in list_a if (item > 0.075 and item <= 0.08)])
        bin17 = len([item for item in list_a if (item > 0.08 and item <= 0.085)])
        bin18 = len([item for item in list_a if (item > 0.085 and item <= 0.09)])
        bin19 = len([item for item in list_a if (item > 0.09 and item <= 0.095)])
        bin20 = len([item for item in list_a if (item > 0.095 and item <= 0.1)])
        bin21 = len([item for item in list_a if (item > 0.1)])
        core_df = core_df.append({'challenge': challenge, 'type': val, 
        'bin0-0.005': round(bin1/maingraph.number_of_nodes()*100,2), 
        'bin0.005-0.01': round(bin2/maingraph.number_of_nodes()*100,2), 
        'bin0.01-0.015': round(bin3/maingraph.number_of_nodes()*100,2), 
        'bin0.015-0.02': round(bin4/maingraph.number_of_nodes()*100,2), 
        'bin0.02-0.025': round(bin5/maingraph.number_of_nodes()*100,2), 
        'bin0.025-0.03': round(bin6/maingraph.number_of_nodes()*100,2), 
        'bin0.03-0.035': round(bin7/maingraph.number_of_nodes()*100,2), 
        'bin0.035-0.04': round(bin8/maingraph.number_of_nodes()*100,2), 
        'bin0.04-0.045': round(bin9/maingraph.number_of_nodes()*100,2), 
        'bin0.045-0.05': round(bin10/maingraph.number_of_nodes()*100,2), 
        'bin0.05-0.055': round(bin11/maingraph.number_of_nodes()*100,2), 
        'bin0.055-0.06': round(bin12/maingraph.number_of_nodes()*100,2), 
        'bin0.06-0.065': round(bin13/maingraph.number_of_nodes()*100,2), 
        'bin0.065-0.07': round(bin14/maingraph.number_of_nodes()*100,2), 
        'bin0.07-0.075': round(bin15/maingraph.number_of_nodes()*100,2), 
        'bin0.075-0.08': round(bin16/maingraph.number_of_nodes()*100,2), 
        'bin0.08-0.085': round(bin17/maingraph.number_of_nodes()*100,2), 
        'bin0.085-0.09': round(bin18/maingraph.number_of_nodes()*100,2), 
        'bin0.09-0.095': round(bin19/maingraph.number_of_nodes()*100,2), 
        'bin0.095-0.1': round(bin20/maingraph.number_of_nodes()*100,2), 
        'bin0.1': round(bin21/maingraph.number_of_nodes()*100,2)}
        ,ignore_index=True)
        # plt.figure(figsize=(20,5))
        # print(len(a.values()))
        # sns.histplot(list(a.values()), color = 'seagreen',binwidth = 0.001, kde=True)
        # plt.gca().set_xlim(xmin=0, xmax=0.035)
        # plt.title(challenge + ' outdegree centrality distribution')
        # plt.ylabel("number of nodes")
        # plt.xlabel("outdegree centrality")
        # plt.savefig('images/outdegree_'+challenge+'.png')
        # plt.show()
        # for i in range(0,100,10):
        #     graph, _, _, _, _, _, _, _, dtemp = ntx.graphCalculation(challenges.getChallenge(challenge)["name"].split(",")[0], intervals = [0,i+10])
        #     graph = graph.to_undirected()
        #     nnodes = graph.number_of_nodes()
        #     print(int(round(i/10)))
        #     STATS['n_nodes%'][int(round(i/10))].append(nnodes/m_nnodes)
        #     if i == 90:
        #         print(i)
        #         Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
        #         giant = graph.subgraph(Gcc[0])
        #         lab = ''
        #         if flag:
        #             lab = 'negative'
        #         else:
        #             lab = 'positive'
        #         core_df = core_df.append({'challenge_type': lab, 'challenge':challenge, 'number_of_nodes': m_nnodes, 'number_of_connected_components_100%': nx.number_connected_components(graph),
        #         'number_of_nodes_of_max_connected_component_100%': giant.number_of_nodes(), 'number_of_nodes_of_max_connected_component_over_total_of_nodes_100%': giant.number_of_nodes()/m_nnodes}, ignore_index=True)
        #     if i == 95:
        #         for id_, value in graph.in_degree(): #influencer
        #             if value > 2:
        #                 df_main = df_main.append(dtemp.loc[dtemp['author_id'].astype(np.int64) == id_].iloc[:])
        #                 df_main.loc[df_main['author_id'] == id_, ['in_degree']] = value
        #         for id_, value in graph.out_degree(): #influenced
        #             if value > 2:
        #                 df_main = df_main.append(dtemp.loc[dtemp['author_id'].astype(np.int64) == id_].iloc[:])
        #                 df_main.loc[df_main['author_id'] == id_, ['out_degree']] = value
        #         df_main.drop_duplicates(subset ='author_id', keep = 'first', inplace = True)
        #         df_main['in_degree'] = df_main['in_degree'].replace(np.nan, 0)
        #         df_main['out_degree'] = df_main['out_degree'].replace(np.nan, 0)
        #         df_main = df_main.drop(['id','createTime','video_id','video_duration','music_id',
        #         'music_title','music_authorName','stats_diggCount','stats_shareCount',
        #         'stats_commentCount','stats_playCount','duetInfo_duetFromId','duetEnabled',
        #         'likedBy_id','likedBy_secUid','likedBy_uniqueId', 'author_secUid'], axis=1)
        #         df_main['author_id'] = df_main['author_id'].astype("string")
        #         df_main.to_csv('dataset/authors/' + challenge + '_inf.csv', sep=';', index=False)
        #     graph = graph.to_undirected()
        #     c_number = list(nx.core_number(graph).values())
        #     core_df = core_df.append({'challenge':challenge+str(i)+"/"+str(i+5),
        #                                 "number_of_1_core":c_number.count(1),
        #                                 "number_of_2_core": c_number.count(2),
        #                                 "number_of_3_core":c_number.count(3),
        #                                 "number_of_4_core":c_number.count(4)}, ignore_index=True)
        #     STATS['n_ccomponents'][int(round(i/5))].append(nx.number_connected_components(graph))
    # print_results(STATS, flag)
    flag = True
core_df.to_csv('dataset/indegree_tab.csv', sep=',', index=False)
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
    plt.title(POS_CHALLENGES[i]+" percentage of nodes (positive)")
    plt.ylabel("percentage of nodes")
    plt.xlabel("% lifespan")
    plt.xticks(range(0,101,10))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    #plt.plot(range(0,101,5), [0]+[x / max(PLOTNCC[0][i]) for x in PLOTNCC[0][i]], label=POS_CHALLENGES[i])
    plt.plot(range(0,101,10), [0]+PLOTNODES[0][i], label=NEG_CHALLENGES[i])
    #    if point != 100:
    #        plt.axvline(x=point,color='r', linewidth=2)
    #plt.savefig('images/pos_percnodes_'+POS_CHALLENGES[i]+'.png')
    plt.show()

for i in range(len(NEG_CHALLENGES)):
    plt.title(NEG_CHALLENGES[i]+" percentage of nodes (negative)")
    plt.ylabel("percentage of nodes (normalized)")
    plt.xlabel("% lifespan")
    plt.xticks(range(0,101,10))
    plt.grid("--")
    plt.gca().set_xlim(xmin=0, xmax=100)
    #plt.plot(range(0,101,5), [0]+[x / max(PLOTNCC[1][i]) for x in PLOTNCC[1][i]], label=NEG_CHALLENGES[i])
    plt.plot(range(0,101,10), [0]+PLOTNODES[1][i], label=NEG_CHALLENGES[i])
    #    if point != 100:
    #        plt.axvline(x=point,color='r', linewidth=2)
    #plt.savefig('images/neg_percnodes_'+NEG_CHALLENGES[i]+'.png')
    plt.show()