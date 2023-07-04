# input
DATABASE = "DATABASE"
# output
TOKENS = "TOKENS"

#####
# Transforme en tokens (un par ligne) le texte "document" contenu dans "name".
from nltk.corpus import stopwords
from nltk import word_tokenize

fr_useless = set(stopwords.words('french'))
fr_punctuation = ['.', ',', '«', '»', '?', '!', '[', ']', '(', ')', ';', '%', '@']
fr_other = ["a", "le", "la", "les", "des", "un", "une", "où", "ou",
            "l", "ni", "si", "ce", "cette", "cet", "donc", "dont"]
fr_useless.update(fr_other)
fr_useless.update(fr_punctuation)

filtre = lambda text: [token for token in text if token.lower() not in fr_useless]
#####
def textToTokens(document, name):
    tokens = filtre(word_tokenize(document, language="french"))

    token_database = open(TOKENS + name, "w")
    # Ajout des tokens au fichier
    for token in tokens:
        token_database.write(token + "\n")
    token_database.close()

#####
# Traduit un fichier en tokens
#####
def fileToTokens(DB, name):
    file = open(DB + name, "r")
    textToTokens(file.read(), name)
    file.close()

#import warnings
#with warnings.catch_warnings():
#    warnings.simplefilter("ignore")
#    import treetaggerwrapper

###############
# Application #
###############
if __name__ == '__main__':
    from mapDB import mapDB
    mapDB(DATABASE, fileToTokens)
    print(DATABASE, " -> ", TOKENS)
