#####
# Transforme le vecteur L en ligne dans le fichier CSV f.
#####
def writeLine(f, L, separator = ";"):
    f.write(L[0])
    for i in range(1, len(L)):
        f.write(separator + L[i])
    f.write('\n')

#####
# Stocke la matrice M d'abscisses X et d'ordonnées Y sous
# format CSV dans file. (Y2 : Exemple de terme de Y)
#####
def writeMatrix(M, X, Y, Y2, file):
    f = open(file, "w")
    writeLine(f, X)
    writeLine(f, Y)
    writeLine(f, Y2)
    for x in range(len(X)):
        for y in range(len(Y)):
            f.write(X[x] + ";" + Y[y] + ";" + str(M[x][y]) + '\n')
    f.close()

#####
# Lis le fichier CSV file en tant que matrice de type typef.
#####
def readMatrix(file, typef = str):
    f = open(file, "r")
    X  = f.readline().rstrip().split(';')
    Y  = f.readline().rstrip().split(';')
    Y2 = f.readline().rstrip().split(';')
    M = [[None for _ in Y] for _ in X]
    for line in f:
        values = line.rstrip().split(';')
        M[X.index(values[0])][Y.index(values[1])] = typef(values[2])
    f.close()
    return M, X, Y, Y2

#####
# Affiche la matrice M d'abscisses X et d'ordonnées Y.
#####
def printMatrix(M, X, Y):
    for x in range(len(M)):
        for y in range(len(M[0])):
            print('[', X[x], "] [", Y[y], "] =", M[x][y])

#####
# Stocke la matrice sous forme compatible avec Concepts.
#####
def matrixToConcepts(M, X, Y, file):
    f = open(file, "w")
    f.write(',')
    writeLine(f, Y, ',')
    for x in range(len(X)):
        f.write(X[x] + ',')
        writeLine(f, M[x], ',')
    f.close()
