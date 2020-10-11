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

BASE_PATH_LOG = "/data/hab_sonda/logs/"

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/hab_sonda/logs/sensores.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s%(message)s', datefmt='%H%M%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/hab_sonda.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#######################################################################################

#Metodo que dado un identificador de sensor (UV, BMP, MPU, etc) es capaz de retornar su archivo de dados "data" con el path completo.
#algo asi como /data/hab_sonda/logs/[id_sensor]data.log
def sensorLogFile(idSensor):
    path = BASE_PATH_LOG + idSensor + "data.log"
    loggerLog.debug("[sensorLogFile] Archivo de sensores recuperado: " + str(path))
    return path

#######################################################################################

#pseudocodigo

#1. Recuperar la configuracion de la traza a enviar
# aqui lo que hay que hacer es saber que datos se quieren enviar. La traza ha de poder ser configurable
# en funcion de los datos de sensores disponibles. El timestamp es fijo y se define en el propio logger
# pero el resto de campos podrian ser configurables mediante archivo de configuracion

t = ConfigHelper.getTiempoMuestreoConf()
trazaConf = ConfigHelper.getConfiguracionTraza()
loggerLog.debug("[HABMain] Sensores configurados: " + str(trazaConf))
#2. Para cada tipo de dato definido en la traza a enviar hacer.

trazaBase = trazaConf.split(',')

while True:

    try:
        trazaDatos = ""

        for sensorType in trazaBase:
            #2.1. Identificar el archivo de log donde se encuentran los datos.
            loggerLog.debug("[HABMain][sensor: " + sensorType + "]")
            pathSensor = sensorLogFile(sensorType)
            #2.2. comprobar si el archivo de log del sensor existe.
            if (os.path.exists(pathSensor)):
                f=open(pathSensor,"r")
                isSensorFileFull = os.stat(pathSensor).st_size>0

                #2.2.1 Si existe y es el archivo de gps (critico) y esta vacio, se trarta de un error de inicializacion o que el GPS
                #no ha cogido cobertura aun. Se ha de seguir iterando pero sin procesar ningun sensor, ya que sin GPS los datos no tienen contexto
                if (sensorType == "gps" and isSensorFileFull):

                    #2.3. Si existe, recuperar la ultima traza escrita (aunque tengan tiempos de muestreo diferentes, son pocos
                    # segundos de diferencia, luego se entiende que pueden estar asociados al timestamp del logger principal)
                    lastLine = f.readlines()[-1]
                    loggerLog.debug("[HABMain] Ultima linea leida [" + lastLine + "]")
                    #2.3.1 Para evitar el procesamiento del ultimo "|" se elimina.
                    ll = lastLine[:-2]
                    loggerLog.debug("[HABMain] Linea leida: [" + ll + "]")
                    dataSensorArray = ll.split('|')
                    #2.4. Se procesa la linea para eliminar el primer datos de la linea, que corresponde siempre al timestamp.
                    i = 0
                    datosProcesados = ""
                    for data in dataSensorArray:
                        if (i > 0):
                            datosProcesados = datosProcesados + "|" + data
                        i = i + 1
                        loggerLog.debug("[HABMain][datosProcesados: " + datosProcesados + "]")
                    f.close()
            	    #2.5. Asociar los datos recuperados del log del sensor S a la traza principal.
                    trazaDatos = trazaDatos + datosProcesados
                    loggerLog.debug("[HABMain][trazaDatos: " + trazaDatos + "]")

                    #3. Finalizado el proceso para todos los sensores, escribir la traza en el archivo sensores.log
                    logger.info(trazaDatos)
                else:
                    loggerLog.warn("[HABMain] OJO, si el sensor era el gps probablemente su archivo de datos este aun vacio...")
            else:
                loggerLog.warn("[HABMain] OJO, no se ha encontrado archivo de datos del sensor [" + sensorType + "]")

    except Exception as e:
        loggerLog.error("[HABMain][ERROR] " + str(e))

    time.sleep(t)


#NOTA: El proceso de envio, se va fuera de este programa, se entiende a partir de ahora que el envio de
# datos puede realizarse con diversos mecanismos. Lora, GSM, etc. estos mecanismos de envio, ahora se cons
# tituiran como servicios aparte.

