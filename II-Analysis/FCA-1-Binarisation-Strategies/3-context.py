# input / output
CSV = "CSV"

#####
# Normalise le vecteur (la somme des valeurs donne 1)
#####
def normaliseLine(L):
    s = sum(L)
    for i in range(len(L)):
        L[i] /= s

#####
# Normalise une matrice (en normalisant tous ses vecteurs)
#####
def normaliseMatrix(M):
    for L in M:
        normaliseLine(L)

#####
# Génère la matrice de fréquence d'une matrice d'occurence
# (double normalisation)
#####
def frequenceMatrix(M):
    normaliseMatrix(M)
    M = [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
    normaliseMatrix(M)
    return M

#####
# Génère le contexte formel à partir d'une matrice de fréquence
#####
def contextMatrix(M):
    return [[ 'X' if M[i][j] > 0.0 else '' for j in range(len(M[0]))] for i in range(len(M))]

#####
# Calcule le contexte formel pour chaque année
import os
from matrixToCSV import readMatrix, writeMatrix, matrixToConcepts #, printMatrix
#####
def context():
    for YEAR in os.listdir(CSV):
        YEAR = "/" + YEAR

        if (os.path.isdir(CSV + YEAR)):
            try:
                Occurence, Documents, Id, Id_Example = readMatrix(CSV + YEAR + "/Occurence.csv", int)
                
                #print("FREQUENCE :")
                Frequence = frequenceMatrix(Occurence)
                #printMatrix( Frequence, Id_Example, Documents )
                writeMatrix( Frequence, Id, Documents, Id_Example, CSV + YEAR + "/Frequence.csv")

                #print("\nCONTEXT :")
                Context = contextMatrix(Frequence)
                #printMatrix( Context, Id_Example, Documents )
                matrixToConcepts( Context, Id, Documents, CSV + YEAR + "/Context.csv")

            except FileNotFoundError:
                continue

###############
# Application #
###############

if __name__ == '__main__':
    context()
    print(CSV + "/*/Occurence.csv", " -> ", CSV + "/*/Frequence.csv", " -> ", CSV + "/*/Context.csv")
