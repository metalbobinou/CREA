# input
CSV = "CSV"
# output
EQUIVALENT = "EQUIVALENT"

#####
# Ecris le texte équivalent ne contenant que les bn:id dans leur ordre d'apparition.
#####
def equivalentText(db, name):
    f = open(EQUIVALENT + name, "w")
    with open(db + name, "r") as file:
        for line in file:
            f.write(line.rstrip().split(';')[0] + "\n")
    f.close()

###############
# Application #
###############
if __name__ == '__main__':
    from mapDB import mapDB
    mapDB(CSV, equivalentText)

    print(CSV, " -> ", EQUIVALENT)
