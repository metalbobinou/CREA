# Dossier Tree Tagger
TreeTagger = "TreeTagger"
# input
TOKENS = "TOKENS"
# output
TREETAGGER = "TREETAGGER"

#####
# Lemmatise les tokens donnés grâce à TreeTagger
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import treetaggerwrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR=TreeTagger)
#####
def tokensToTreeTagger(document, name):
    lemmes_database = open(TREETAGGER + name, "w")
    lemmes = treetaggerwrapper.make_tags(tagger.tag_text(document))
    # Ajout des lemmes au fichier
    for lemme in lemmes:
        if hasattr(lemme, "what"):
            print(lemme)
            continue
        if lemme.lemma == "@card@":
            continue
        lemmes_database.write(lemme.lemma + "\n")
    lemmes_database.close()

#####
# Lemmatise un fichier de tokens grâce à TreeTagger
#####
def fileToTreeTagger(DB, name):
    file = open(DB + name, "r")
    tokensToTreeTagger(file.read(), name)
    file.close()

###############
# Application #
###############
if __name__ == '__main__':
    from mapDB import mapDB
    mapDB(TOKENS, fileToTreeTagger)
    print(TOKENS, " -> ", TREETAGGER)
