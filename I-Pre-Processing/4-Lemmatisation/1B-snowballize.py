# input
TOKENS = "TOKENS"
# output
SNOWBALL = "SNOWBALL"

#####
# Lemmatise les tokens donnés grâce à Snowball
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer(language='french')
#####
def tokensToSnowball(document, name):
    lemmes_database = open(SNOWBALL + name, "w")
    lemmes = [stemmer.stem(token) for token in document.split("\n")]
    # Ajout des lemmes au fichier
    for lemme in lemmes:
        lemmes_database.write(lemme + "\n")
    lemmes_database.close()

#####
# Lemmatise un fichier de tokens grâce à Snowball
#####
def fileToSnowball(DB, name):
    file = open(DB + name, "r")
    tokensToSnowball(file.read(), name)
    file.close()

###############
# Application #
###############
if __name__ == '__main__':
    from mapDB import mapDB
    mapDB(TOKENS, fileToSnowball)
    print(TOKENS, " -> ", SNOWBALL)
