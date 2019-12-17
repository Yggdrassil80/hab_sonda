#!/usr/bin/python

import time
import datetime
import os, sys
from PIL import Image
from picamera import PiCamera

#import logging
#loggerLog1 = logging.getLogger('server_logger')
#loggerLog1.setLevel(logging.INFO)
#inf1 = logging.FileHandler('/data/wsp-virolai/logs/wsp-Camara.log')
#inf1.setLevel(logging.INFO)
#formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
#inf1.setFormatter(formatterInformer)
#loggerLog1.addHandler(inf1)


#Metodo que toma una imagen con una resolucion concreta, con un tiempo de exposicion concreto
# con un tipo (RF o HD) concreto y con un formato concreto.
def tomarImagen(res, baseImagePath, tiempoEspera, tipo, formato):

	try:
		#loggerLog1.info("[Camara][tomarImagen] Inicio");
		camera = PiCamera()
		#loggerLog1.info("[Camara][tomarImagen] PiCamera inicializado");
		camera.resolution = (int(res[0]), int(res[1]))
		#loggerlog1.info("[Camara][tomarImagen] Resolucion definida: " + res[0] + "x" + res[1]);
    		camera.start_preview()
		#loggerLog.info("[Camara][tomarImagen] Tomando datos raw...");
    		time.sleep(tiempoEspera)
		fecha = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    		camera.capture(baseImagePath + fecha + '-' + tipo + '.' + formato, formato)
    		#print('Foto tomada y guardada en: ' + baseImagePath + fecha + '-' + tipo + '.' + formato)
		camera.stop_preview()
                camera.close()
		#loggerLog1.info("[Camara][tomarImagen] Foto tomada y guardada en: " + baseImagePath + fecha + '-' + tipo + '.' + formato );
		#loggerLog1.info("[Camara][tomarImagen] Fin");

		return baseImagePath + fecha + '-' + tipo + '.' + formato
	except Exception:
    		e = sys.exc_info()[1]
		print(e.args[0])
		#loggerLog1.error("[Camara][tomarImagen] " + e.args[0])
		#loggerLog1.error("[Camara][tomarImagen] ERROR. La imagen puedo no haberse tomado!");
		return "CamaraError"

#metodo que convierte una imagen dada en Raw RGB de 24 bits para hacerla mas robusta al envio por RF
def convertirImagenToRaw(nombreImagen, baseImagePath):

	Image.open(nombreImagen).convert('RGB').save(baseImagePath + "rgbaux.rgb")
	#print("[Camara][convertirImagenToRaw] nombreImagen.rgb: " + baseImagePath + "rgbaux.rgb")
	return nombreImagen

#Metodo que borra una imagen dada del FS de la Raspberry
def eliminarImagenRaw(nombreImagen):
	print("Imagen borrada")
