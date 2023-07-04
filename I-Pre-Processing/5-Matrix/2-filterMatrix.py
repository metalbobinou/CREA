## Filtrage
# input
CSV = "CSV"
# output
FILTER = "FILTER"
##
limit = 0.5

#####
# Calcule en mémoire la taille de la matrice filtrée.
#####
def fillMatrix(document, csv, Documents, Id, Id_Example):
    if not document in Documents:
        Documents.append(document)
    if not csv[0] in Id:
        Id.append(csv[0])
        Id_Example.append(csv[3])

#####
# Filtre le ficher CSV name en ne gardant que les notions
# de cohérence supérieures ou égales à limit.
#####
def filterCoherence(db, name, Documents, Id, Id_Example):
    filter_db = open(FILTER + name, "w")

    # Parcours des lignes
    with open(db + name) as file:
        for line in file:
            # Obtenir les valeurs CSV
            values = line.rstrip().split(';')
            if float(values[-1]) >= limit:
                fillMatrix(name, values, Documents, Id, Id_Example)
                filter_db.write(line)

    filter_db.close()

#####
# Filtre les notions dans chaque document, et calcule leur
# occurence par fichier pour chaque année.
import os
from matrixToCSV import writeMatrix #, printMatrix
#####
def filterAndOccurence():
    Occurence = []
    def incrementOccurence(db, name):
        with open(FILTER + name, "r") as file:
            for line in file:
                values = line.rstrip().split(';')
                Occurence[Documents.index(name)][Id.index(values[0])] += 1

    for YEAR in os.listdir(CSV):
        YEAR = "/" + YEAR

        if (os.path.isdir(CSV + YEAR)):
            Documents = []
            Id = []
            Id_Example = []

            # Filter
            for MONTH in os.listdir(CSV + YEAR):
                MONTH = YEAR + "/" + MONTH

                if (os.path.isdir(CSV + MONTH)):
                    for doc in os.listdir(CSV + MONTH):
                        doc = MONTH + "/" + doc

                        filterCoherence(CSV, doc, Documents, Id, Id_Example)

            if len(Documents) == 0:
                continue

            Occurence = [[0 for _ in range(len(Id))] for _ in range(len(Documents))]
            # Occurences
            for MONTH in os.listdir(CSV + YEAR):
                MONTH = YEAR + "/" + MONTH

                if (os.path.isdir(CSV + MONTH)):
                    for doc in os.listdir(CSV + MONTH):
                        doc = MONTH + "/" + doc

                        incrementOccurence(CSV, doc)

            # printMatrix(Occurence, Documents, Id_Example )
            writeMatrix(Occurence, Documents, Id, Id_Example, CSV + YEAR + "/Occurence.csv")

###############
# Application #
###############
if __name__ == '__main__':
    filterAndOccurence()
    print(CSV, "\n -> ", FILTER, "\n -> ", CSV + "/*/Occurence.csv")
