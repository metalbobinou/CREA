absolute = "/MNSHS-SSD/Militarisation-Jeunesse/data/3-samuel/"

# input
CSV = absolute + "CSV"
# output
IMPACT_GRAPH = absolute + "IMPACT_GRAPH"

#####
# Prend une liste et renvoie une map (clé : index)
#####
def listToMap(l):
    return {index: value for index, value in enumerate(l)}

#####
# Prend une matrice d'impact mutuel et des labels, retourne un graphe NetworkX
import networkx as nx
#####
def graphFromMutualImpact(mutualImpact, labelsTerms, labelsDocuments):
    # Noeuds
    G = nx.Graph()
    G.add_nodes_from(labelsDocuments, bipartite=0)
    G.add_nodes_from(labelsTerms, bipartite=1)

    # Arrêtes
    lenDocuments = len(labelsDocuments)
    lenTerms = len(labelsTerms)
    for i in range(lenDocuments):
        for j in range(lenTerms):
            w = mutualImpact[j][i]
            if float(w) != 0.0:
                G.add_edge(labelsDocuments[i], labelsTerms[j], weight=w)

    return G

#####
# Créé un dégradé de {size} couleurs entre {colorA} et {colorB}
#####
def colorGradient(colorA, colorB, size):
    # Séparation en composante Rouge, Vert, Bleu
    start_rgb = [int(colorA[i:i+2], 16) for i in (1, 3, 5)]
    end_rgb   = [int(colorB[i:i+2], 16) for i in (1, 3, 5)]
    # Création du dégradé
    colors = []
    for i in range(size):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (size - 1))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (size - 1))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (size - 1))
        color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        colors.append(color)
    return colors

#####
# Utilise le degré des noeuds de {G} pour déterminer leur couleur
#####
def colorFromFun(G, colors, colorDoc, labelsDocuments):
    nodeColors = []
    for node in G.nodes():
        if node in labelsDocuments:
            nodeColors.append(colorDoc)
        else:
            res = G.degree[node]
            nodeColors.append(colors[res])
    return nodeColors

#####
# Cherche les notions clées du corpus en fonction de leur présence sur plusieurs documents
#####
def keyTerms(mutualImpact, labelsTerms, labelsDocuments, colorA, colorB, colorDoc):
    # Impact Mutuel + labels -> Graphe labellisé
    G = graphFromMutualImpact(mutualImpact, labelsTerms, labelsDocuments)

    # Coloration du graphe
    color_map = colorFromFun(G, colorGradient(colorA, colorB, 1 + len(labelsDocuments)), colorDoc, labelsDocuments)

    # Calcul des positions des noeuds (algo ressort)
    pos = nx.spring_layout(G)

    # Calcul de l'épaisseur des arrêtes
    weights = [10 * float(G[u][v]['weight']) for u, v in G.edges()]

    return G, pos, color_map, weights

#####
# Affiche un graphe selon différentes options
import matplotlib.pyplot as plt
#####
def visualize(G, pos, node_color, weights, labelsDocuments, title, year):
    node_sizes = [1000 if node in labelsDocuments else 300 for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_color)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=weights, edge_color='black', alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_color='black', font_size=10, labels={node: node if node in labelsDocuments else '\n'.join(node.split('_')) for node in G.nodes()})

    plt.axis('off')
    plt.title(title)
    plt.savefig(IMPACT_GRAPH + "/" + year + ".png")
    plt.clf()

# from networkx.algorithms import community
# Prend une matrice Numpy et des labels, renvoie un graphe NetworkX labellisé
#def adjMatrixToGraph(adjMatrix, labels):
#    G = nx.from_numpy_matrix(adjMatrix, create_using=nx.Graph)
#    return nx.relabel_nodes(G, listToMap(labels))

#def clusterTerm(adjMatrix, labels, colorFun):
#    G = adjMatrixToGraph(adjMatrix, labels)
#    clusters = community.greedy_modularity_communities(G)

#    color_map = {}
#    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
#    for i, cluster in enumerate(clusters):
#        for node in cluster:
#            color_map[node] = colors[i]

###############
# Application #
###############
import os
if __name__ == "__main__":
    from matrixToCSV import readMatrix, printMatrix, writeMatrix
    for YEAR in os.listdir(CSV):
        if (os.path.isdir(CSV + "/" + YEAR)):
            try:
                ID_File, IDs, Files, Examples = readMatrix(CSV + "/" + YEAR + "/ImpactMutuel.csv")
                Files = [os.path.basename(File).split(".")[0] for File in Files]

                G, pos, color_map, weights = keyTerms(ID_File, Examples, Files, "#FF5F5F", "#80E961", "#00B3FF")
                visualize(G, pos, color_map, weights, Files, "Impact Mutuel (" + YEAR + ")",  YEAR)
            except FileNotFoundError:
                continue
