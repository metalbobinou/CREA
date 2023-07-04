# input/output
CSV = "CSV"
# output
XML = "lattice.xml"

#####
# Génère les matrices d'impact mutuel et de similarité conceptuelle
# à partir d'un Contexte Formel (utilisant le Treillis de Galois)
import concepts 
#####
def contextToMatrix(file, xml=False):
    context = concepts.load_csv(file)
    treillis = context.lattice

    if xml:
        latticeToXML(treillis)

    BnIds = context.extension([])
    Documents = context.intension([])

    AND_ID_DOC = [[0 for _ in range(len(Documents))] for _ in range(len(BnIds))]
    AND_ID_ID = [[0 for _ in range(len(BnIds))] for _ in range(len(BnIds))]
    AND_DOC_DOC = [[0 for _ in range(len(Documents))] for _ in range(len(Documents))]
    ID = [0 for _ in range(len(BnIds))]
    DOC = [0 for _ in range(len(Documents))]

    # Parcours du treillis
    for extent, intent in context.lattice:
        # OCCURENCE D'ID
        for bn in range(len(extent)):
            a = BnIds.index(extent[bn])
            ID[a] += 1
            # OCCURENCE D'ID & ID
            for bn2 in range(bn + 1, len(extent)):
                b = BnIds.index(extent[bn2])
                AND_ID_ID[a][b] += 1
                AND_ID_ID[b][a] += 1
            # OCCURENCE D'ID & DOCUMENT
            for doc in range(len(intent)):
                b = Documents.index(intent[doc])
                AND_ID_DOC[a][b] += 1

        # OCCURENCE DE DOCUMENT
        for doc in range(len(intent)):
            a = Documents.index(intent[doc])
            DOC[a] += 1
            # OCCURENCE DE DOCUMENT & DOCUMENT
            for doc2 in range(doc + 1, len(intent)):
                b = Documents.index(intent[doc2])
                AND_DOC_DOC[a][b] += 1
                AND_DOC_DOC[b][a] += 1

    ID_DOC  = [[AND_ID_DOC[i][j]  / (ID[i]  + DOC[j] - AND_ID_DOC[i][j] ) for j in range(len(Documents))] for i in range(len(BnIds))]
    ID_ID   = [[1. if i==j else AND_ID_ID[i][j]   / (ID[i]  + ID[j]  - AND_ID_ID[i][j]  ) for j in range(len(BnIds))]     for i in range(len(BnIds))]
    DOC_DOC = [[1. if i==j else AND_DOC_DOC[i][j] / (DOC[i] + DOC[j] - AND_DOC_DOC[i][j]) for j in range(len(Documents))] for i in range(len(Documents))]

    return ID_DOC, ID_ID, DOC_DOC

#####
# Génère la représentation XML du treillis de Galois.
# from graphviz2drawio import graphviz2drawio
#####
#def latticeToXML(treillis):
#    graphviz = "\n".join(str(treillis.graphviz()).split("\n")[1:])
#    xml = graphviz2drawio.convert(graphviz)
#    with open(XML, "w") as f:
#        f.write(xml)

#####
# Calcule les similarités conceptuelles et l'impact mutuel pour chaque année
import os
from matrixToCSV import readMatrix, writeMatrix #, printMatrix
#####
def treillis():
    for YEAR in os.listdir(CSV):
        YEAR = "/" + YEAR

        if (os.path.isdir(CSV + YEAR)):
            try:
                ID_DOC, ID_ID, DOC_DOC = contextToMatrix(CSV + YEAR + "/Context.csv")
                _, ID, DOC, ID_EX = readMatrix(CSV + YEAR + "/Frequence.csv")

                #print("\nImpact Mutuel")
                #printMatrix(ID_DOC, ID_EX, DOC)
                writeMatrix(ID_DOC, ID, DOC, ID_EX, CSV + YEAR + "/ImpactMutuel.csv")

                #print("\nSimilarité Conceptuelle (Id)")
                #printMatrix(ID_ID, ID_EX, ID_EX)
                writeMatrix(ID_ID, ID, ID, ID_EX, CSV + YEAR + "/SimilariteID.csv")

                #print("\nSimilarité Conceptuelle (Doc)")
                #printMatrix(DOC_DOC, DOC, DOC)
                writeMatrix(DOC_DOC, DOC, DOC, DOC, CSV + YEAR + "/SimilariteDoc.csv")

            except FileNotFoundError:
                continue
    

###############
# Application #
###############

if __name__ == '__main__':
    treillis()

    print(CSV + "/Context.csv ; " + CSV + "/Frequence.csv\n"
          + " -> " + CSV + "/ImpactMutuel.csv\n"
          + " -> " + CSV + "/SimilariteID.csv\n"
          + " -> " + CSV + "/SimilariteDoc.csv")
