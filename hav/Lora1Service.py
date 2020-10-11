#################################################################################
#               Proyecto:   Lora1Service                                        #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import os
import glob
import time
import logging

import RFHelper
import ConfigHelper

SENSOR_FILE = "/data/hab_sonda/logs/sensores.log"

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/Lora1Service.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%$')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#pseudocodigo

#1.   Inicializar el Lora1

tiempoEnvio = ConfigHelper.getTiempoMuestreoConf()
loggerLog.info("[Lora1Service][Conf] Tiempo envio LoRa: " + str(tiempoEnvio));
usbRF = ConfigHelper.getUsbRF()
loggerLog.info("[Lora1Service][Conf] Puerto USB RF: " + usbRF);

while True:
    try:
        #2.   Comprobar que el archivo sensores.log existe
        if [-f SENSOR_FILE]:
            #2.1. si existe
            #2.2. coger la ultima linea y enviar. Esperar tiempodeenvioRF y volver a comprobar si el archivo sensores.log existe
            loggerLog.debug("[Lora1Service] Envio de traza almacenada en log por RF...")
            RFHelper.putUltimoDatoRF(usbRF, '/data/hab_sonda/logs/sensores.log')
            loggerLog.debug("[Lora1Service] Traza enviada OK")
        #2.3. si no existe
        else:
            #2.4.   Esto seria un estado de emergencia en el cual se asume que no hay datos de sensores.
            # Se pasaria a intentar enviar la ultima linea del archivo de log del servicio de GPS
            loggerLog.warn("[Lora1Service] Envio de traza de GPS, no archivo de datos detectado...")
            RFHelper.putUltimoDatoRF(usbRF, '/data/hab_sonda/logs/gpsdata.log')
            loggerLog.warn("[Lora1Service] Traza enviada OK")

    except Exception as a:
        loggerLog.error("[Lora1Service][ERROR] " + e)
        time.sleep(5)

    time.sleep(tiempoEnvio)
