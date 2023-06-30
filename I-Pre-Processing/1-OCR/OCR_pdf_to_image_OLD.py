import os

from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path

def pdf_to_image(pdf, folder=None):
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    name = pdf.split(".")[0]
    infos_PDF = pdfinfo_from_path(pdf)
    # print(infos_PDF)
    nb_pages = infos_PDF['Pages']
    begin_page = 3
    last_page = nb_pages
    iter_page = begin_page

    while (iter_page <= last_page):
        # print("DEBUBUBUBUBUG : " + str(nb_pages))
        try:
            # Sur Windows
            # images = convert_from_path(pdf, 200, poppler_path=r'C:\Users\alexa\poppler-23.01.0\Library\bin')
            # Sur Linux (avec poppler-utils)
            # images = convert_from_path(pdf, 200)
            images = convert_from_path(pdf,
                                       200,
                                       first_page=iter_page,
                                       last_page=iter_page)
        except:
            with open("image/log.txt", 'a', encoding='utf-8') as log:
                log.write("[ERROR] Could not convert" + pdf + "\n")
            return
        i = iter_page
        name = name.split("/")
        if (len(name) == 4):
            name = name[3]
        else:
            name = name[0]
        images[0].save(folder + "/" + name + '_page_' + str(i) + '.jpg', 'JPEG')

        iter_page += 1

    # for i in range(len(images)):
    #    if i >= 3:
    #        name = name.split("/")
    #        if (len(name) == 4):
    #            name = name[3]
    #        else:
    #            name = name[0]
    #        images[i].save(folder+"/"+name+'_page' + str(i) + '.jpg', 'JPEG')



# "../1-scrapping/DATABASE/1885/10/Mon journal_18851015.pdf"
def to_images(doc):
    d = doc.split("/")
    doc2 = d[3] + "/" + d[4] + "/" + d[5]
    doc2 = doc2.replace(".pdf", "")
    pdf_to_image(doc, "image/" + doc2)


def mapDB(folder, f):
    for YEAR in os.listdir(folder):
        if (int(YEAR) < 1880) or (int(YEAR) > 1900):
            continue
        YEAR = "/" + YEAR

        # print("DEBUG : --" + folder + YEAR + "--")
        if (os.path.isdir(folder + YEAR)):
            for MONTH in os.listdir(folder + YEAR):
                MONTH = YEAR + "/" + MONTH
                # print("DEBUG : --" + folder + MONTH + "--")
                if (os.path.isdir(folder + MONTH)):
                    for doc in os.listdir(folder + MONTH):
                        doc = MONTH + "/" + doc

                        # Apply
                        # print("DEBUG : --" + folder + doc + "--")
                        # f(folder + doc)
                        # protec = "\"" + folder + doc + "\""
                        protec = folder + doc
                        print("DEBUG [MapDB] : --" + protec + "--")
                        f(protec)


def main():
    if (not os.path.exists("image")):
        os.mkdir("image")
    l = open("image/log.txt", 'w')
    l.truncate(0)
    l.close()
    log = open("image/log.txt", 'a', encoding='utf-8')
    log.write("Program Started\n")
    # /MNSHS-SSD/Militarisation-Jeunesse/data/1-scrapping/DATABASE de 1881 a 1900 inclus

    # Launch process
    mapDB("../1-scrapping/DATABASE", to_images)
    log.close()

main()