import networkx as nx
import matplotlib.pyplot as plt
import lib.tiktok_network as ntx

plt.figure(figsize=(15,15))
graph, labels, colors = ntx.graphCalculation("emojichallenge",colorCriteria="createTime")
ntx.graphStats(graph)
pos = nx.spring_layout(graph, k=0.20, iterations=20)
nx.draw_networkx_nodes(graph,pos,node_color=colors,node_size=60)     
nx.draw_networkx_labels(graph, pos, labels,font_size=5)
nx.draw_networkx_edges(graph,pos,arrows=True,arrowsize=3,arrowstyle="-|>",alpha=0.5)#edge_color='lightgrey'   
ax= plt.gca()
ax.collections[0].set_edgecolor("#000000")
plt.show()
