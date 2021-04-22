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


def base64toTxt(base64String):
    bytesStr = b64decode(base64String, validate=True) #de base 64 a bytes

    if bytesStr[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')


    pages = convert_from_bytes(bytesStr, fmt='jpeg', poppler_path=r'.\venv\poppler\bin') #convierte de  bytes a imagen en formato PIL

    reader = easyocr.Reader(["es"]) # need to run only once to load model into memory
    results=[]
    for page in pages:
        result=reader.readtext(pil_to_cv2(page),detail=0) #Lee la imagen y devuelve el texto en lista de palabras
        for i in range(len(result)):
            results.append(result[i])
    #return results
    #de aquí se empieza a clasificar el texto para devolver los parametros requeridos forma de diccionario
    #cara frontal
    for i in range(len(results)):
        if results[i].upper() == "NUMERO" or results[i] == "NÚMERO":

            if results[i+3].upper() == "APELLIDOS" and results[i+4].upper() != "NOMBRES":
                datos={"Nombre": str(results[i+4]), "Apellidos": str(results[i+2]), "Número": str(results[i+1])}
                break
            elif results[i+2].upper() == "APELLIDOS" and results[i+3].upper() != "NOMBRES" and results[i-2].upper() == "CEDULA DE CIUDADANIA" or results[i-2].upper() == "CÉDULA DE CIUDADANIA":
                datos={"Nombre": str(results[i+3]), "Apellidos": str(results[i+1]), "Número": str(results[i-1])}
                break
        
        elif results[i].upper() == "APELLIDOS":
            if results[i-3].upper() == "CEDULA DE CIUDADANIA" or results[i-3].upper() == "CÉDULA DE CIUDADANIA" and results[i+1].upper() != "NOMBRES":
                datos={"Nombre": str(results[i+1]), "Apellidos": str(results[i-1]), "Número": str(results[i-2])}
                break  
            else:
                raise ValueError("La cara frontal de la cedula no es clara. Por favor subir otro archivo")
                break

    #reverso de la cedula   
    for i in range(len(results)):
        if results[i].upper() == "FECHA DE NACIMIENTO" or results[i].upper() == "Fecha de nacimiento":
            datos["Fecha de nacimiento"] = str(results[i+1])
            datos["Lugar de nacimiento"] = str(results[i+2])
            break
        
        elif results[i].upper() == "ESTATURA":
            if results[i-1].upper() == "M" or results[i-1].upper() == "F":
                datos["Estatura"] = str(results[i-3])
                datos["RH"] = str(results[i-2])
                datos["Sexo"] = str(results[i-1])
                break
            else:
                datos["Estatura"] = str(results[i-2])
                datos["RH"] = str(results[i-1])
                break
        

    return datos

            

    

@app.route('/cedula', methods=['GET'])
@cross_origin()
def leerCedula():
    string = request.get_json()
    if (string.get('base64String', None) is not None):
        pdf64 = string['base64String']

    datos=base64toTxt(pdf64)
    json_object = json.dumps(datos, indent = 4)  
    return json_object 

    


########################### FIN DE LOS SERVICIOS #############################
if __name__ == "__main__":
    app.run(debug=True)