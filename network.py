import networkx as nx
import matplotlib.pyplot as plt
import lib.tiktok_network as ntx

#plt.figure(figsize=(15,15))
for i in range(0,100,10):
    graph, labels, colors, pos, _, _, _, _ = ntx.graphCalculation("silhouettechallenge",colorCriteria="createTime", intervals=[0,i+10])
    nx.write_gexf(graph, "dataset/silhouettechallenge"+str(int(i+10))+".gexf", prettyprint=True)
'''
ntx.graphStats(graph)
nx.draw_networkx_nodes(graph,pos,node_color=colors,node_size=60)     
nx.draw_networkx_labels(graph, pos, labels,font_size=5)
nx.draw_networkx_edges(graph,pos,arrows=True,arrowsize=3,arrowstyle="-|>",alpha=0.5)#edge_color='lightgrey'   
ax= plt.gca()
ax.collections[0].set_edgecolor("#000000")
plt.show()
'''
