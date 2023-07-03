import os

from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path


# Process each PDF file
def pdf_to_image(pdf, out_folder):
    print("[DEBUG] pdf : " + pdf)
    basename = os.path.basename(pdf)
    print("[DEBUG] name : " + basename)
    infos_PDF = pdfinfo_from_path(pdf)
    # print(infos_PDF)
    nb_pages = infos_PDF['Pages']
    begin_page = 3
    last_page = nb_pages
    iter_page = begin_page

    while (iter_page <= last_page):
        print("[P] page " + str(iter_page) + "/" + str(nb_pages))
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
        basename_no_ext = basename.replace(".pdf", "")
        # DOUBLE TITLE OF JOURNAL IN FOLDER AND BASENAME
        #out_filename = out_folder + "/" + basename_no_ext + '_page_' + str(i) + '.jpg'
        out_filename = out_folder + "/" '_page_' + str(i) + '.jpg'
        print("[DEBUG] Write out : \"" + out_filename + "\"")
        images[0].save(out_filename, 'JPEG')

        iter_page += 1

    # for i in range(len(images)):
    #    if i >= 3:
    #        name = name.split("/")
    #        if (len(name) == 4):
    #            name = name[3]
    #        else:
    #            name = name[0]
    #        images[i].save(folder+"/"+name+'_page' + str(i) + '.jpg', 'JPEG')


# Build new directory for output
def build_outpath(pdf_filename):
    print("[0] initial name : \"" + pdf_filename + "\"")
    split_pathname = pdf_filename.split("/")
    print("[1] split name : \"" + str(split_pathname) + "\"")

    new_pathname = split_pathname[3] + "/" + split_pathname[4] + "/" + split_pathname[5]
    print("[2] new pathname : \"" + new_pathname + "\"")
    out_pathname = "image/" + new_pathname
    print("[3] out pathname : \"" + out_pathname + "\"")

    out_dirname = out_pathname.replace(".pdf", "")
    print("[4] out dirname : \"" + out_dirname + "\"")
    if (not os.path.exists(out_dirname)):
        os.makedirs(out_dirname)

    return (out_pathname)


# "../1-scrapping/DATABASE/1885/10/Mon journal_18851015.pdf"
def to_images(pdf_filename):
    print("[DEBUG] to_image : " + pdf_filename)
    out_pathname = build_outpath(pdf_filename)
    out_dirname = out_pathname.replace(".pdf", "")
    pdf_to_image(pdf_filename, out_dirname)


# Browse within the directories tree and process each file
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
                        # pathname = "\"" + folder + doc + "\""
                        pathname = folder + doc
                        print("-- [MapDB]                           Processing file : --" + pathname + "--")
                        f(pathname)

# Main (build dir, open log, launch processing)
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
