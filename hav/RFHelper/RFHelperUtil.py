#!/usr/bin/python

import os
import time
import serial
import logging
import sys

from pathlib import Path

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/lora1.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#Metodo que recupera la ultima linea de un arhivo y la envia por RF
def putUltimoDatoRF(usbPort, archivoDatos):

    try:
        loggerLog.debug("[RFHelper][putUltimoDatoRF] Inicio");
        loggerLog.debug("[RFHelper][putUltimoDatoRF] usbPort: " + usbPort + " archivoDatos: " + archivoDatos);

        loggerLog.debug("[RFHelper][putUltimoDatoRF] Apertura puerto serie para leer...");
        #abrir el puerto para poder enviar datos al chip de RF
        puertoUSB=serial.Serial(usbPort)
        loggerLog.debug("[RFHelper][putUltimoDatoRF] Puerto abierto");
        #abrir el archivo de datos de los sensores y recuperar la ultima linea
        loggerLog.debug("[RFHelper][putUltimoDatoRF] Apertura archivo de log de datos...");

        #verificar que el archivo exista y tenga datos
        sensor_file = Path(archivoDatos)
        isSensorFileFull = os.stat(sensor_file).st_size>0
        if (sensor_file.is_file() and isSensorFileFull):
            f=open(archivoDatos,"r")


            lastLine = f.readlines()[-1]
            #print ('Datos leidos: ' + lastLine)
            loggerLog.debug("[RFHelper][putUltimoDatoRF] Datos leidos");
            f.close()
            loggerLog.debug("[RFHelper][putUltimoDatoRF] Archivo cerrado");

            #Enviar byte a byte por RF
            for dato in lastLine:
                loggerLog.debug("[RFHelper][putUltimoDatoRF] Inicio envio datos...");
                bytesEscritos = puertoUSB.write(dato)
                loggerLog.debug("[RFHelper][putUltimoDatoRF] Dato enviado!");
                time.sleep(0.05)

                #print ('Datos enviados: ' + str(dato))

	        #loggerLog.debug("[RFHelper][putUltimoDatoRF] Todos los datos enviados OK");

                #bytesEscritos = puertoUSB.write(lastLine.encode('utf-8'))
                #print ('Datos enviados: ' + str(bytesEscritos))	

                #vaciar el buffer de salida para asegurarse que no se queda nada que pueda mezclarse con el siguiente dato
                #puertoUSB.flushInput()
                #puertoUSB.flushOutput()
                #Cerrar el puerto USB
            puertoUSB.close()
            #loggerLog.info("[RFHelper][putUltimoDatoRF] Puerto Serial cerrado. Final");
            return bytesEscritos
        else:
            loggerLog.warn("[RFHelper][putUltimoDatoRF] OJO el archivo de datos o no existe o no tiene contenido")
            return 0
    except Exception as e:
        loggerLog.error("[RFHelper][ERROR] " + str(e))

        #loggerLog.error("[RFHelper][putUltimoDatoRF] " + e.args[0]);
        #loggerLog.error("[RFHelper][putUltimoDatoRF] Error");
        return 0





