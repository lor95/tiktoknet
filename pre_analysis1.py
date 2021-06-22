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
PLOT = [[],[]]
PLOTDENSITY = [[[] for x in POS_CHALLENGES],[[] for x in NEG_CHALLENGES]]
PLOTCOEFF = [[[] for x in POS_CHALLENGES],[[] for x in NEG_CHALLENGES]]

def reset_stats():
    return {"density":[[] for x in range(0,20)],
            "coeff": [[] for x in range(0,20)]}

def print_results(arr, _type=False):
    if _type:
        for val in arr["density"]:
            for i in range(len(NEG_CHALLENGES)):
                PLOTDENSITY[1][i].append(val[i])
        for val in arr["coeff"]:
            for i in range(len(NEG_CHALLENGES)):
                PLOTCOEFF[1][i].append(val[i])
    else:
        for val in arr["density"]:
            for i in range(len(POS_CHALLENGES)):
                PLOTDENSITY[0][i].append(val[i])
        for val in arr["coeff"]:
            for i in range(len(POS_CHALLENGES)):
                PLOTCOEFF[0][i].append(val[i])
    
flag = False
for elem in ALL_CHALLENGES:
    STATS = reset_stats()
    for challenge in elem:
        for i in range(0,100,5):
            graph, _, _, _, _, _, _, _ = ntx.graphCalculation(challenges.getChallenge(challenge)["name"].split(",")[0], intervals = [1,i+5])
            graph = graph.to_undirected()
            STATS['density'][int(round(i/5))].append(nx.density(graph))
            if(graph.number_of_nodes() == 0):
                STATS['coeff'][int(round(i/5))].append(0)
            else:
                STATS['coeff'][int(round(i/5))].append(nx.average_clustering(graph))
    print_results(STATS, flag)
    flag = True

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
