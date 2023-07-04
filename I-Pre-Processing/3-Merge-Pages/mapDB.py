#####
# Itère sur la base de donnée contenue dans folder et applique f à chaque fichier
# f(chemin vers la db, chemin à coller à celui de la db pour avoir le document)
import os
#####
def mapDB(folder, f):
    for YEAR in os.listdir(folder):
        YEAR = "/" + YEAR

        if (os.path.isdir(folder + YEAR)):
            for MONTH in os.listdir(folder + YEAR):
                MONTH = YEAR + "/" + MONTH

                if (os.path.isdir(folder + MONTH)):
                    for doc in os.listdir(folder + MONTH):
                        doc = MONTH + "/" + doc

                        # Apply
                        f(folder, doc)
