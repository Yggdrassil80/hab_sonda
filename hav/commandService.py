##################################################################################
#Proyecto: lora2Service					                                         #
#Autor: Yggdrassil80				                                             #
#Descricpión: Servicio de recepcion de datos de comando y control de hab_sonda   #
##################################################################################

import os
import glob
import serial
import time
import datetime
import binascii
import logging
import ConfigHelper
import CommandHelper

#Se espera que la antena pueda enviar datos de comando y control de este tipo
#{tokenServiceName}:{variableServiceName}:{variableValue}
#o bien
#{tokenServiceName}:{0/1}
#
#Estos comandos se representaran como un token equivalente del servicio de motor de reglas (ruleEngine)

#Creacion del logger para los logs del servicio
loggerLog = logging.getLogger('server_logger')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/commandService.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

usbRF2 = ConfigHelper.getUsbCommand()
loggerLog.info("[CommandService][Conf] Puerto USB RF2: " + usbRF2);

#Se dejan las configuraciones de prueba para PC
#puertoUSB=serial.Serial('/dev/ttyUSB0',baudrate=9600, timeout = 5.0)
#puertoUSB=serial.Serial('COM4', baudrate=115200, timeout = 5.0)
puertoUSB=serial.Serial(usbRF2)

#Archivo donde almacenaran los comandos recibidos
TOKEN_PATH = ConfigHelper.getTokenPath()
LOG_PATH = ConfigHelper.getRecivedCommand()
LOG_PATH_RAW = ConfigHelper.getRecivedCommandRaw()

recieved = ""
buffer = ""
loggerLog.info("[CommandService][Conf] Arrancando receptor de comandos...: " + puertoUSB.portstr)

encontrado = 0
traza = ""
newTraza = ""
trozoFinal = bytearray()
trozoNoFinal = bytearray()

while True:
    try:
        while (puertoUSB.inWaiting() > 0):
            loggerLog.debug("[CommandService] Comando entrante...")
            buffer = puertoUSB.read(128)
            loggerLog.debug("[CommandService] Comnado leido: " + str(buffer))
            loggerLog.debug("[CommandService] Generando archivo de comandos raw...")
            fraw = open (LOG_PATH_RAW, "a")
            fraw.write(buffer.decode())
            fraw.close()
            loggerLog.debug("[CommandService] Archivo de comandos en raw cerrado")
            loggerLog.debug("[CommandService] Generando tokens de comandos ...")
            for i in range(len(buffer)):
                 if (buffer[i] == 10):
                     #salto de carro encontrado, los datos van de i=0 a i.
                     encontrado = 1
                     trozoFinal = buffer[0:i+1]
                     trozoNoFinal = buffer[i+1:len(buffer)] 
                     loggerLog.debug("[CommandService] byte leido: " + str(buffer[i]) + " en posicion: " + str(i))
                     break

            if (encontrado == 1): 
                #Existe un trozo final
                traza+=trozoFinal.decode()
                newTraza = trozoNoFinal.decode() 
                f = open (LOG_PATH, "a")
                loggerLog.debug("[CommandService] Fragmento final recuperado:" + trozoFinal.decode())
                loggerLog.debug("[CommandService] Escribiendo en archivo de comandos definitivo...")
                loggerLog.info("[CommandService] Comando a escribir: " + str(traza))
                try:
                    f.write(traza)
                    #En este momento, ya se tiene registrado un comando en una linea del archivo recivedCommands.log
                    #Ahora es momento de generar los tokens de control para que los servicios puedan interpretarlos
                    #0. Verificar que se trata de un token valido
                    if CommandHelper.isValidCommand(traza):
                        #1. Escribir el token de control en TOKEN_PATH para que el servicio correspondiente lo lea
                        loggerLog.debug("[CommandService] Comando [" + str(traza) + "] valido, se ejecuta")
                        CommandHelper.writeCommnad(traza)
                    else:
                        loggerLog.debug("[CommandService] Comando [" + str(traza) + "] no valido, no se ejecuta")


                except Exception as eGps:
                    #Si hubiera un error, se notifica, pero se intenta guardar datos que hubiera en el buffer igualmente
                    loggerLog.error("[CommandService][ERROR] Ha habido un problema con la recepción de los comandos: " + str(eGps))
                    f.write(traza)
                f.close()
                loggerLog.debug("[CommandService] Archivo de comandos cerrado")
                traza = newTraza
                newTraza = ""
                encontrado = 0
                loggerLog.info("[CommandService] Fragmento inicial de comando: " + traza)
            else:
                trozoNoFinal = buffer[0:len(buffer)]
                loggerLog.debug("[CommandService] Fragmento recuperado:" + trozoNoFinal.decode())
                traza+=trozoNoFinal.decode()
                loggerLog.info("[CommandService] Comando actual: " + traza)

            loggerLog.debug("[CommandService] traza vale: " + traza + " newTraza vale: " + newTraza)

            buffer = ""
            puertoUSB.flushInput()
            puertoUSB.flushOutput()

    except Exception as e:
        loggerLog.error("[CommandService][ERROR] " + str(e))
        puertoUSB.close()
        time.sleep(5)

puertoUSB.close()