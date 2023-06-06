#################################################################################
#               Proyecto: cameraService con libcamera2                        #
#               Autor: Joaquín Pertejo Martín                                   #
#                                                                               #
#################################################################################

import time
import datetime
import logging
from picamera2 import Picamera2

import ConfigHelper

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/hab_sonda/logs/CameraService-v2.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

act = ConfigHelper.isCamaraActivo()
resolucionRF = ConfigHelper.getResolucionImagenRF()
loggerLog.info("[CameraServiceV2][Conf] ResolucionRF: " + str(resolucionRF))
resolucionMax = ConfigHelper.getResolucionImagenMax()
loggerLog.info("[CameraServiceV2][Conf] resolucionMax: " + str(resolucionMax))
basePathImage = ConfigHelper.getPathImagenesBase()
loggerLog.info("[CameraServiceV2][Conf] basePathImage: " + str(basePathImage))
tiempoTomaImagen = ConfigHelper.getTiempoTomaImagen()
loggerLog.info("[CameraServiceV2][Conf] tiempoTomaImagen: " + str(tiempoTomaImagen))
ndviActive=ConfigHelper.isNDVIConfigurationActivo()
loggerLog.info("[CameraServiceV2][Conf] ndviActive: " + str(ndviActive))
redAWB=ConfigHelper.getRedAWB()
loggerLog.info("[CameraServiceV2][Conf] redAWB: " + str(redAWB))
blueAWB=ConfigHelper.getBlueAWB()
loggerLog.info("[CameraServiceV2][Conf] blueAWB: " + str(blueAWB))

if act == 1:

    loggerLog.debug("[CamaraV2][tomarImagen] Inicio");
    camera = Picamera2()
    loggerLog.debug("[CamaraV2][tomarImagen] Picamera2 inicializado");
    camera_config = camera.create_still_configuration(main={"size": (int(resolucionMax[0]), int(resolucionMax[1]))}, lores={"size": (640, 480)}, display="lores")
    camera.configure(camera_config)
    loggerLog.debug("[CamaraV2][tomarImagen] Resolucion definida: " + resolucionMax[0] + "x" + resolucionMax[1]);

    while True:
        try:
            camera.start()
            loggerLog.debug("[CamaraV2][tomarImagen] Tomando datos raw...");
            #time.sleep(tiempoEspera)
            fecha = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
            camera.capture_file(basePathImage + fecha + '-' + 'HD' + '.' + 'jpg')
            loggerLog.debug("[CamaraV2][tomarImagen] Foto tomada y guardada en: " + basePathImage + fecha + "-" + 'HD' + "." + 'jpg')
            camera.stop()
            loggerLog.debug("[CamaraV2][tomarImagen] Foto tomada y guardada en: " + basePathImage + fecha + "-" + 'HD' + "." + 'jpg')
            loggerLog.debug("[CamaraV2][tomarImagen] Fin");

            time.sleep(tiempoTomaImagen)
            
        except Exception as e:
            loggerLog.error("[CameraServiceV2] Exception: " + str(e))
            loggerLog.error("[CameraServiceV2] Se ha producido un error, se sigue iterando...")
else:
    loggerLog.warn("[CamareServiceV2] La camara no ha sido activada!")
