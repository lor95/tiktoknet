import pandas as pd
from ast import literal_eval
import lib.tiktok_network as ntx
import networkx as nx
import matplotlib.pyplot as plt

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
        nx.draw_networkx_nodes(graph,pos,node_color=colors,node_size=60)     
        nx.draw_networkx_labels(graph, pos, labels,font_size=5)
        nx.draw_networkx_edges(graph,pos,arrows=True,arrowsize=3,arrowstyle="-|>",alpha=0.5)#edge_color='lightgrey'   
        ax= plt.gca()
        try:
            ax.collections[0].set_edgecolor("#000000")
        except:
            continue
        plt.show()
