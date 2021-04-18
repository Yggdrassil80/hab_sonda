#!/usr/bin/python

import time
import datetime
import os, sys
import logging
from PIL import Image
from picamera import PiCamera


#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_loggerCam')
loggerLog.setLevel(logging.INFO)
infCam = logging.FileHandler('/data/hab_sonda/logs/cameraLib.log')
infCam.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
infCam.setFormatter(formatterInformer)
loggerLog.addHandler(infCam)


#Metodo que toma una imagen con una resolucion concreta, con un tiempo de exposicion concreto
# con un tipo (RF o HD) concreto y con un formato concreto.
def tomarImagen(res, baseImagePath, tiempoEspera, tipo, formato, ndviActive, redAWB, blueAWB):

    try:
        loggerLog.debug("[Camara][tomarImagen] Inicio");
        camera = PiCamera()
        loggerLog.debug("[Camara][tomarImagen] PiCamera inicializado");
        if ndviActive == 1:
             loggerLog.debug("[Camara][tomarImagen] modo NDVI activado con redAWB: " + str(redAWB) + " y blueAWB: " + str(blueAWB))
             customGains = (redAWB, blueAWB)
             camera.awb_mode = "off"
             camera.awb_gains = customGains

        camera.resolution = (int(res[0]), int(res[1]))
        loggerLog.debug("[Camara][tomarImagen] Resolucion definida: " + res[0] + "x" + res[1]);
        camera.start_preview()
        loggerLog.debug("[Camara][tomarImagen] Tomando datos raw...");
        time.sleep(tiempoEspera)
        fecha = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        camera.capture(baseImagePath + fecha + '-' + tipo + '.' + formato, formato)
        loggerLog.debug("[Camara][tomarImagen] Foto tomada y guardada en: " + baseImagePath + fecha + "-" + tipo + "." + formato)
        camera.stop_preview()
        camera.close()
        loggerLog.debug("[Camara][tomarImagen] Foto tomada y guardada en: " + baseImagePath + fecha + "-" + tipo + "." + formato );
        loggerLog.debug("[Camara][tomarImagen] Fin");

        return baseImagePath + fecha + '-' + tipo + '.' + formato
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        loggerLog.error("[Camara][tomarImagen] " + e.args[0])
        loggerLog.error("[Camara][tomarImagen] ERROR. La imagen puedo no haberse tomado!");
        return "CamaraError"

#metodo que convierte una imagen dada en Raw RGB de 24 bits para hacerla mas robusta al envio por RF
def convertirImagenToRaw(nombreImagen, baseImagePath):

    Image.open(nombreImagen).convert('RGB').save(baseImagePath + "rgbaux.rgb")
    #print("[Camara][convertirImagenToRaw] nombreImagen.rgb: " + baseImagePath + "rgbaux.rgb")
    return nombreImagen

#Metodo que borra una imagen dada del FS de la Raspberry
def eliminarImagenRaw(nombreImagen):
    print("Imagen borrada")
