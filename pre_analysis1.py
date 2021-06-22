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

def reset_stats():
    return {"density":[[] for x in range(0,20)]}

def print_results(arr, _type=False):
    text = "POSITIVE"
    if _type:
        text = "NEGATIVE"
        for val in arr["density"]:
            for i in range(len(NEG_CHALLENGES)):
                PLOTDENSITY[1][i].append(val[i])
    else:
        for val in arr["density"]:
            for i in range(len(POS_CHALLENGES)):
                PLOTDENSITY[0][i].append(val[i])
    
flag = False
counter = 0
for elem in ALL_CHALLENGES:
    STATS = reset_stats()
    for challenge in elem:
        for i in range(0,100,5):
            graph, _, _, _, _, _, _, _ = ntx.graphCalculation(challenges.getChallenge(challenge)["name"].split(",")[0], intervals = [i,i+5])
            STATS['density'][int(round(i/5))].append(nx.density(graph))
        counter += 1
    print_results(STATS, flag)
    flag = True
    counter = 0

#plotpos
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
    plt.show()
