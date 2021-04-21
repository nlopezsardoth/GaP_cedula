
AMBIENTE VIRTUAL
Para crear el ambiente virtual
    virtualenv venv
Para iniciar el ambiente virtual
    venv\Scripts\activate



PAQUETES A INSTALAR

pip3 install flask   

pip3 install flask_cors

pip3 install flask_pymongo

pip3 install pdf2image

pip3 install easyocr

pip3 install numpy



PARA INSTALAR POPPLER
 -> poppler-0.68.0_x86

http://blog.alivate.com.au/poppler-windows/ 

descargar de la url y dentro de venv (ambiente virtual) crear una carpeta llamada "popler" y copiar los archivos que se cuentran dentro del zip descargado dentro de esta..

para utilizar en 

pages = convert_from_bytes(bytesStr, fmt='jpeg', poppler_path=r'.\venv\poppler\bin')

donde poppler_path=r'.\venv\poppler\bin' es la ruta a poppler.

