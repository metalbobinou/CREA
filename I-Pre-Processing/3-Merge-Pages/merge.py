# input
TEXT = "text"
# output
MERGED = "../3-samuel/text-merged"

filtrage = True
#####
# Prend un dossier en entrée et calcule la fusion des fichiers qu'il contient,
# Permet de retirer le bruit
bruit = ['<', '>', '#', '%', '{', '}', '|', '\"', '^', '~', '[', ']', '`', '$',
         '*', '+', ';', '/', '@', '=', '&', '—', '©', '¢', '°', '_',
         '‘', 'œ', '↔', '^L']
filtre = str.maketrans("", "", ''.join(bruit))
#####
def merge(folder, name):
    merged_file = open(MERGED + name + ".txt", "w")

    # Les fichiers sont en doubles car il y a les versions non corrigées
    l = len(os.listdir(folder + name)) // 2
    for i in range(4, l+4):
        try:
            page = open(TEXT + name + "/_page_" + str(i) + "corrected.txt", "r")
            for line in page:
                if filtrage:
                    line = line.translate(filtre)
                merged_file.write(line)
            page.close()
        except FileNotFoundError:
            print(TEXT + name + "/_page_" + str(i) + "corrected.txt not found.")
            continue

    merged_file.close()

#####
# Itère l'application de f sur l'arborescance folder
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

###############
# Application #
###############

if __name__ == '__main__':
    mapDB(TEXT, merge)
    print(TEXT, " -> ", MERGED)
