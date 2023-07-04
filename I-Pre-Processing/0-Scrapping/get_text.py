from pyllicalabs import *
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

relativePath = "/.../"

allPath   = relativePath + "/all_texts.txt"
getPath   = relativePath + "/get_text.txt"
outputDir = relativePath + "/DATABASE/"

def scrapping():
    # Récupération de l'état
    getFile = open(getPath, "r")
    getInfos = [int(getFile.readline().replace('\n', '')) for _ in range(8)]
    getFile.close()

    # Récupération de la base de données
    allFile = open(allPath, "r")
    paths = [allFile.readline().replace('\n', '') for _ in range(1500)]
    allFile.close()

    # Récupération du champ d'action
    startIndex = getInfos[6] - 1
    endIndex   = getInfos[7] - 1

    if startIndex > endIndex :
        print("Travail terminé.")
        return

    if getInfos[0] == 0 :
        print("Préparation pour le premier document")
        startDate  = datetime.datetime(int(paths[2::11][startIndex]),
                                       int(paths[3::11][startIndex]),
                                       int(paths[4::11][startIndex]))
        endDate    = datetime.datetime(int(paths[5::11][startIndex]),
                                       int(paths[6::11][startIndex]),
                                       int(paths[7::11][startIndex]))
    else:
        startDate  = datetime.datetime(getInfos[0], getInfos[1], getInfos[2])
        endDate    = datetime.datetime(getInfos[3], getInfos[4], getInfos[5])

    if startDate > endDate :
        print("Préparation pour le prochain document")
        startIndex += 1
        
        # Incrément du texte et réinitialisation de la date de début
        getFile = open(getPath, "w")
        getFile.writelines([paths[2::11][startIndex] + "\n",
                            paths[3::11][startIndex] + "\n",
                            paths[4::11][startIndex] + "\n",
                            paths[5::11][startIndex] + "\n",
                            paths[6::11][startIndex] + "\n",
                            paths[7::11][startIndex] + "\n",
                            str(startIndex + 1)      + "\n",
                            str(endIndex   + 1)])
        getFile.close()
        return

    # --- Traitement du texte actuel à la date actuelle ---
    # 1) Mémorisation des paramètres à utiliser
    text_url = paths[1::11][startIndex]
    text_year = startDate.year
    text_month = startDate.month
    text_day = startDate.day
    text_title = outputDir + str(text_year) + "/" + str(text_month) + "/" + paths[::11][startIndex]

    # 2) Incrémentation
    if paths[9::11][startIndex] == 'j':
        startDate += datetime.timedelta(days = int(paths[8::11][startIndex]))
    elif paths[9::11][startIndex] == 'm':
        startDate += relativedelta(months =+ int(paths[8::11][startIndex]))
    
    # 3) Préparation de la valeur suivante
    getFile = open(getPath, "w")
    getFile.writelines([str(startDate.year ) + "\n",
                        str(startDate.month) + "\n",
                        str(startDate.day  ) + "\n",
                        str(endDate.year   ) + "\n",
                        str(endDate.month  ) + "\n",
                        str(endDate.day    ) + "\n",
                        str(startIndex + 1 ) + "\n",
                        str(endIndex   + 1 ) + "\n"])

    # 4) Récupération de la donnée
    print("Appel de :")
    print("pdfpress(url=\""  + text_url        + "\",")
    print("    title=\""     + text_title      + "\",")
    print("    year="        + str(text_year)  + ",")
    print("    month="       + str(text_month) + ",")
    print("    day="         + str(text_day)   + ",")
    print("    item=1,\nrate=1)\n")

    pdfpress(url=      text_url,
             title=    text_title,
             year=     text_year,
             month=    text_month,
             day=      text_day,
             item=     1,
             rate=     1)

scrapping()
