#################################################################################
#               Proyecto: cameraService con libcamera2                        #
#               Autor: Joaquín Pertejo Martín                                   #
#                                                                               #
#################################################################################

import time
import logging
import Camara

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
loggerLog.info("[CameraService][Conf] ResolucionRF: " + str(resolucionRF))
resolucionMax = ConfigHelper.getResolucionImagenMax()
loggerLog.info("[CameraService][Conf] resolucionMax: " + str(resolucionMax))
basePathImage = ConfigHelper.getPathImagenesBase()
loggerLog.info("[CameraService][Conf] basePathImage: " + str(basePathImage))
tiempoTomaImagen = ConfigHelper.getTiempoTomaImagen()
loggerLog.info("[CameraService][Conf] tiempoTomaImagen: " + str(tiempoTomaImagen))
ndviActive=ConfigHelper.isNDVIConfigurationActivo()
loggerLog.info("[CameraService][Conf] ndviActive: " + str(ndviActive))
redAWB=ConfigHelper.getRedAWB()
loggerLog.info("[CameraService][Conf] redAWB: " + str(redAWB))
blueAWB=ConfigHelper.getBlueAWB()
loggerLog.info("[CameraService][Conf] blueAWB: " + str(blueAWB))

if act == 1:

    while True:
        try:
            #INICIO: Espacio para recuperar los datos del sensor a partir de la libreria
            loggerLog.info("[CameraServiceV2][Main] Inicio de toma de imagen de camara interna...")
            #Toma imagen de alta resolucion para despues
            nombreImagen = Camara.tomarImagen(resolucionMax, basePathImage, tiempoTomaImagen, "HD", "jpg", ndviActive, redAWB, blueAWB)
            loggerLog.info("[cameraServiceV2][Main] Imagen tomada OK")
            #Toma Image de baja resolucion para su envio
            #nombreImagen = Camara.tomarImagen(gpsData, resolucionRF, basePathImage, int(3), "RF", "jpeg")
            #nombreImagenRaw = Camara.convertirImagenToRaw(nombreImagen, basePathImage)
            #FINAL: Espacio para recuperar los datos del sensor a partir de la libreria

            time.sleep(tiempoTomaImagen)
            

        except Exception as e:
            loggerLog.error("[CameraServiceV2] Exception: " + str(e))
            loggerLog.error("[CameraServiceV2] Se ha producido un error, se sigue iterando...")
else:
    loggerLog.warn("[CamareServiceV2] La camara no ha sido activada!")
