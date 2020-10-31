#pseudocodigo

#1.   Inicializar el GSM
#2.   Comprobar que el archivo sensores.log existe
#2.1. si existe
#2.2.   coger la ultima linea y enviar. Esperar tiempodeenvioGSM y volver a comprobar si el archivo sensores.log$
#2.3. si no existe
#2.4.   Esto seria un estado de emergencia en el cual se asume que no hay datos de sensores.
# Se pasaria a intentar enviar la ultima linea del archivo de log del servicio de GPS

#################################################################################
#               Proyecto:   GSM  Service                                        #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import os
import glob
import time
import logging

import RFHelper
import GPSHelper
import ConfigHelper

from pathlib import Path

SENSOR_FILE = "/data/hab_sonda/logs/sensores.log"
GPS_DATA_FILE = "/data/hab_sonda/logs/gpsdata.log"

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/GSMService.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#pseudocodigo

#1.   Inicializar el GSM

tiempoEnvio = ConfigHelper.getMaxTiempoTrazaGSM()
loggerLog.info("[GSMService][Conf] Tiempo envio GSM: " + str(tiempoEnvio));
usbGSM = ConfigHelper.getUsbGSM()
loggerLog.info("[GSMService][Conf] Puerto USB GSM: " + usbGSM);
listaMoviles = ConfigHelper.getListaMoviles()
loggerLog.info("[GSMService][Conf] Lista moviles: " + usbGSM);
pin = ConfigHelper.getPinGSM()
loggerLog.info("[GSMService][Conf] pin: " + usbGSM);
alturaDesactivacionGSM = ConfigHelper.leerAlturaGSMDesactivacion()
loggerLog.info("[GSMService][Conf] Altura de desactivacion del GSM: " + alturaDesactivacionGSM);
alturaActivacionGMS = ConfigHelper.leerAlturaGSMActivacion()
loggerLog.info("[GSMService][Conf] Altura de activacion del GSM: " + alturaActivacionGMS);

while True:

    try:
        #1.1 Recuperar la altura del GPS
        gpsdata = GPSHelper.getGPSDataFromFile()
        alt = gpsdata[0]

        if (alt > alturaActivacionGMS and alt < alturaDesactivacionGSM):
            #2.   Comprobar que el archivo sensores.log existe
            sensor_file = Path(SENSOR_FILE)
            isSensorFileFull = os.stat(sensor_file).st_size>0
            if (sensor_file.is_file() and isSensorFileFull):
                #2.1. si existe y tiene contenido 

                #2.2. coger la ultima linea y enviar. Esperar tiempodeenvioRF y volver a comprobar si el archivo sensores.log existe
                loggerLog.debug("[GSMService] Envio de traza almacenada en log por GSM...")
                GSMHelper.putDatosGSM(usbGSM, SENSOR_FILE, listaMoviles, pin) 
                loggerLog.debug("[GSMService] Traza enviada OK")
            #2.3. si no existe
            else:
                #2.4.   Esto seria un estado de emergencia en el cual se asume que no hay datos de sensores.
                # Se pasaria a intentar enviar la ultima linea del archivo de log del servicio de GPS
                loggerLog.debug("[GSMService] Envio de traza almacenada en log por GSM...")
                GSMHelper.putDatosGSM(usbGSM, GPS_DATA_FILE, listaMoviles, pin) 
                loggerLog.debug("[GSMService] Traza enviada OK")
        else:
            loggerLog.info("[GSMService] Fuera del rango de GSM, no se envia nada [alt actual]: " + alt)

    except Exception as e:
        loggerLog.error("[GSMService][ERROR] " + str(e))
        time.sleep(5)

    time.sleep(tiempoEnvio)

