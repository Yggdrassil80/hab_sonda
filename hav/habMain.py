#################################################################################
#               Proyecto:   MainHAB                                             #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import os
import glob
import time
import logging

import random

import ConfigHelper

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/hab_sonda/logs/sensores.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(message)s', datefmt='%H%M%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/hab_sonda.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%$
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#######################################################################################

#pseudocodigo

#1. Recuperar la configuracion de la traza a enviar
# aqui lo que hay que hacer es saber que datos se quieren enviar. La traza ha de poder ser configurable
# en funcion de los datos de sensores disponibles. El timestamp es fijo y se define en el propio logger
# pero el resto de campos podrian ser configurables mediante archivo de configuracion

trazaConf = ConfigHelper.getConfiguracionTraza()

#2. Para cada tipo de dato definido en la traza a enviar hacer.

trazaBase = trazaConf.split(',')
trazaDatos = ""

try:

    for sensorType in trazaBase:
        #2.1. Identificar el archivo de log donde se encuentran los datos.
        pathSensor = checkValidSensorLogFile(sensorType)
        #2.2. comprobar si el archivo de log del sensor existe.
        if [-f pathSensor]:
            loggerLog.debug("[HABMain] Apertura del archivo de datos...");
            f=file(pathSensor,"r")
            loggerLog.debug("[HABMain] Archivo abierto OK!");
            #2.3. Si existe, recuperar la ultima traza escrita (aunque tengan tiempos de muestreo diferentes, son pocos
            # segundos de diferencia, luego se entiende que pueden estar asociados al timestamp del logger principal)
            lastLine = f.readlines()[-1]
            loggerLog.debug("[HABMain] Lectura de la ultima linea de datos: " + lastLine);
            f.close()
            #2.4. Asociar los datos recuperados del log del sensor S a la traza principal.
            trazaDatos = trazaDatos + lastLine

    #3. Finalizado el proceso para todos los sensores, escribir la traza en el archivo sensores.log
    logger.info(trazaDatos)

except Exception e:
    loggerLog.error("[HABMain][ERROR] " + e)

#NOTA: El proceso de envio, se va fuera de este programa, se entiende a partir de ahora que el envio de
# datos puede realizarse con diversos mecanismos. Lora, GSM, etc. estos mecanismos de envio, ahora se cons
# tituiran como servicios aparte.
