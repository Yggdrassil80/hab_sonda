#!/usr/bin/python

import time
import datetime
import os, sys
import logging
from picamera2 import PiCamera2


#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_loggerCam')
loggerLog.setLevel(logging.INFO)
infCam = logging.FileHandler('/data/hab_sonda/logs/cameraV2Lib.log')
infCam.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
infCam.setFormatter(formatterInformer)
loggerLog.addHandler(infCam)


#Metodo que toma una imagen con una resolucion concreta, con un tiempo de exposicion concreto
# con un tipo (RF o HD) concreto y con un formato concreto.
def tomarImagen(res, baseImagePath, tiempoEspera, tipo, formato, ndviActive, redAWB, blueAWB):

    try:
        loggerLog.debug("[CamaraV2][tomarImagen] Inicio");
        camera = PiCamera2()
        loggerLog.debug("[CamaraV2][tomarImagen] PiCamera2 inicializado");
        camera_config = camera.create_still_configuration(main={"size": (int(res[0]), int(res[1]))}, lores={"size": (640, 480)}, display="lores")
        camera.configure(camera_config)
        loggerLog.debug("[CamaraV2][tomarImagen] Resolucion definida: " + res[0] + "x" + res[1]);
        camera.start()
        loggerLog.debug("[CamaraV2][tomarImagen] Tomando datos raw...");
        time.sleep(tiempoEspera)
        fecha = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        camera.capture_file(baseImagePath + fecha + '-' + tipo + '.' + formato)
        loggerLog.debug("[CamaraV2][tomarImagen] Foto tomada y guardada en: " + baseImagePath + fecha + "-" + tipo + "." + formato)
        camera.stop()
        loggerLog.debug("[CamaraV2][tomarImagen] Foto tomada y guardada en: " + baseImagePath + fecha + "-" + tipo + "." + formato );
        loggerLog.debug("[CamaraV2][tomarImagen] Fin");

        return baseImagePath + fecha + '-' + tipo + '.' + formato
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        loggerLog.error("[CamaraV2][tomarImagen] " + e.args[0])
        loggerLog.error("[CamaraV2][tomarImagen] ERROR. La imagen puedo no haberse tomado!");
        return "CamaraError"