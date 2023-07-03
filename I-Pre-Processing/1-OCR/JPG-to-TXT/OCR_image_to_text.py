import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd ='/usr/bin/tesseract'
from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path
import cv2

import language_tool_python

'''def OCR(path):
    result = reader.readtext(path, detail=0, paragraph=True)
    name = path.split(".")[0]
    with open(name + ".txt", 'w', encoding='utf-8') as f:
        for text in result:
            f.write(text)
            f.write("\n")'''


# Build new directory for output
def new_filename(img_filename):
    print("[0] initial name : \"" + img_filename + "\"")
    filename_no_ext = img_filename.replace(".jpg", "")
    print("[1] no ext : \"" + filename_no_ext + "\"")
    filename_new_basename = filename_no_ext.replace("image", "text")
    print("[2] new basename : \"" + filename_new_basename + "\"")
    filename_new_dirname = filename_new_basename.replace(filename_new_basename.split('/')[4],"")
    print("[3] new dirname : \"" + filename_new_dirname + "\"")
    if (not os.path.exists(filename_new_dirname)):
        os.makedirs(filename_new_dirname)
    return (filename_new_basename)

# Write out results
def write_out(filename, data):
    f = open(filename + ".txt", 'w', encoding="utf-8")
    f.write(data)
    f.close()
    '''with open(doc + ".txt", 'w') as f:
        f.write(text)'''

# Process each image
def to_txt(img):
    print("[DEBUG] to_txt : " + img)

    print("[DEBUG] " + img + " : image = cv2.imread")
    image = cv2.imread(img)
    print("[DEBUG] " + img + " : gray = cv2.cvtColor")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("[DEBUG] " + img + " : txt = pytesseract.image_to_string")
    txt = pytesseract.image_to_string(gray)

    '''try:
        text = pytesseract.image_to_string(gray)
    except:
        with open("text/log.txt", 'a', encoding='utf-8') as log:
            log.write("[ERROR] Could not extract text from" + img + "\n")
        return'''
    new_pathname = new_filename(img)
    print("[DEBUG] Write out pure text : " + new_pathname)
    write_out(new_pathname, txt)
    #print("[DEBUG] Language Tool french")
    #tool = language_tool_python.LanguageTool('fr-FR')
    print("[DEBUG] Language Tool processing : " + new_pathname)
    corrected_txt = tool.correct(txt)
    #corrected_pathname = new_pathname + "_corrected.txt"
    corrected_pathname = new_pathname + "corrected"
    print("[DEBUG] Write out corrected text : " + corrected_pathname)
    write_out(corrected_pathname, corrected_txt)

# Browse within the directories tree and process each file
def mapDB2(folder, f):
    for YEAR in os.listdir(folder):
        YEAR = "/" + YEAR

        if (os.path.isdir(folder + YEAR)):
            for MONTH in os.listdir(folder + YEAR):
                MONTH = YEAR + "/" + MONTH

                if (os.path.isdir(folder + MONTH)):
                    for doc in os.listdir(folder + MONTH):
                        doc = MONTH + "/" + doc
                        if (os.path.isdir(folder + doc)):
                            for file in os.listdir(folder + doc):
                                file = doc + "/" + file
                                # Apply
                                # print(folder + file)
                                # f(folder + file)
                                pathname = folder + file
                                print("-- [MapDB2]                  Processing file : --" + pathname + "--")
                                f(pathname)

# Main (build dir, open log, launch processing)
def main():
    if (not os.path.exists("text")):
        os.mkdir("text")
    l = open("text/log.txt", 'w')
    l.truncate(0)
    l.close()
    log = open("text/log.txt", 'a', encoding='utf-8')
    log.write("Image to text Started\n")
    # /MNSHS-SSD/Militarisation-Jeunesse/data/1-scrapping/DATABASE de 1881 a 1900 inclus

    # Launch process
    mapDB2("image", to_txt)
    log.close()


# GLOBAL DICTIONNARY LOADED ONLY ONCE
print("[DEBUG][GLOBAL] Language Tool french")
tool = language_tool_python.LanguageTool('fr-FR')

# Launch main program
main()
