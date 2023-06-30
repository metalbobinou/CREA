import os
import pytesseract, cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\alexa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
#from pytesseract import pytesseract

from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path
#import cv2

'''def OCR(path):
    result = reader.readtext(path, detail=0, paragraph=True)
    name = path.split(".")[0]
    with open(name + ".txt", 'w', encoding='utf-8') as f:
        for text in result:
            f.write(text)
            f.write("\n")'''

import language_tool_python
tool = language_tool_python.LanguageTool('fr-FR')

def to_txt(img):
    print(img)
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    '''try:
        text = pytesseract.image_to_string(gray)
    except:
        with open("text/log.txt", 'a', encoding='utf-8') as log:
            log.write("[ERROR] Could not extract text from" + img + "\n")
        return'''
    doc = img.replace(".jpg", "")
    #os.mkdir("text/image/La_Jeune_France_19170107/")
    #doc = doc.replace("image", "text")
    with open("text/"+doc + ".txt", 'w') as f:
        f.write(text)


    txt = tool.correct(text)
    with open(doc + "corrected.txt", 'w', encoding='utf-8') as f:
        f.write(txt)


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
                                protec = folder + file
                                print("DEBUG [MapDB2] : --" + protec + "--")
                                f(protec)


def main():
    for doc in os.listdir("image/La_Jeune_France_19170107/"):
        doc = "image/La_Jeune_France_19170107/" + doc
        to_txt(doc)
    '''if (not os.path.exists("text")):
        os.mkdir("text")
    l = open("text/log.txt", 'w')
    l.truncate(0)
    l.close()
    log = open("text/log.txt", 'a', encoding='utf-8')
    log.write("Image to text Started\n")
    # /MNSHS-SSD/Militarisation-Jeunesse/data/1-scrapping/DATABASE de 1881 a 1900 inclus

    # Launch process
    mapDB2("image", to_txt)
    log.close()'''


main()
