import base64
import sys, os
from typing import Text
sys.path.append('./venv/lib/site-packages')
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo, ObjectId
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import loads, dumps
from bson.objectid import ObjectId

# https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
# Import libraries 
from PIL import Image 
import sys 
from pdf2image import convert_from_path, convert_from_bytes
from base64 import b64decode
import codecs

import easyocr
import io
import numpy as np

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost/GaP_cedula"
CORS(app, resources={r"*": {"origins": "*"}})
mongo = PyMongo(app)


#with tesseract
#def base64toText(base64String):

    #here we convert from base64 to binary
    #bytesStr = b64decode(base64String, validate=True)

    #if bytesStr[0:4] != b'%PDF':
        #raise ValueError('Missing the PDF file signature')

    #binary to images
    #pages = convert_from_bytes(bytesStr, fmt='jpeg', poppler_path=r'.\venv\poppler\bin')

    #the path to the pytesseract library
    #pytesseract.pytesseract.tesseract_cmd = './venv/Tesseract-OCR/tesseract.exe'

    #from images to text usung tesseract
    #text=[]
    #for page in pages:
        #text.append(pytesseract.image_to_string(page, lang='spa'))

    #return text

    def pil_to_cv2(image):
        open_cv_image = np.array(image)
        return open_cv_image[:, :, ::-1].copy()


    def base64toTxt(base64Str):
        bytesStr = b64decode(base64Str, validate=True)

        if bytesStr[0:4] != b'%PDF':
            raise ValueError('Missing the PDF file signature')


        pages = convert_from_bytes(bytesStr, fmt='jpeg', poppler_path=r'.\venv\poppler\bin')

        reader = easyocr.Reader(["es"]) # need to run only once to load model into memory

        results=[]
        for page in pages:
            result=reader.readtext(pil_to_cv2(page),detail=0)
            for i in range(len(result)):
                results.append(result[i])
        return results

            

    



#@app.route('/cedula/<pdf64>', methods=['GET'])
#def leerCedula(pdf64):

    


########################### FIN DE LOS SERVICIOS #############################
if __name__ == "__main__":
    app.run(debug=True)