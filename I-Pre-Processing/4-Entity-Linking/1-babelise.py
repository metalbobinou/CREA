# Clé Babelfy
BABEL_KEY = ""
# input
DATABASE = "DATABASE"
# output
CSV = "CSV"

#####
# Formatte une notion dans un texte au bon format dans un CSV.
#####
def tokenToCSV(token, text, start_index):
    relative_start = token.char_fragment_start()
    relative_end   = token.char_fragment_end()

    bn_id  = str( token.babel_synset_id()      )
    start  = str( relative_start + start_index )
    end    = str( relative_end   + start_index )
    score  = str( token.score()                )
    gscore = str( token.global_score()         )
    cscore = str( token.coherence_score()      )

    return bn_id + ";" + start + ";" + end + ";" + " ".join(text[relative_start : relative_end + 1].split('\n')) + ";" + score + ";" + gscore + ";" + cscore + "\n"

#####
# Traduit en CSV-Babelfy le texte "document" contenu dans "name".
from pybabelfy.babelfy import *
babelapi = Babelfy()
from distribution import cutByPack
#####
def textToCSV(document, name):
    csv_database = open(CSV + name + ".csv", "w")
    # Couper le document en bloc de caractères
    requests, indexes = cutByPack(document)
    print([indexes[i] - indexes[i-1] for i in range(1, len(indexes))])
    # Parcours des blocs
    for i in range(len(requests)):
        # Babelisation
        try:
            tokens = babelapi.disambiguate(requests[i], lang="FR", key=BABEL_KEY, anntype=AnnTypeValues.ALL)
            # Ajout des tokens au fichier CSV
            for token in tokens:
                csv_database.write( tokenToCSV(token, requests[i], indexes[i]) )
        except Exception as e:
            print(repr(e))
    csv_database.close()

#####
# Traduit un fichier en CSV-Babelfy
#####
def fileToCSV(DB, name):
    print(DB + name)
    file = open(DB + name, "r")
    textToCSV(file.read(), name)
    file.close()

###############
# Application #
###############
if __name__ == '__main__':
    from mapDB import mapDB
    mapDB(DATABASE, fileToCSV)

    print(DATABASE, " -> ", CSV)
