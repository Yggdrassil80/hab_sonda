#################################################################################
#		Proyecto: Liverenas						#
# 		Autor: Oscar Loras Delgado					#
#										#
#################################################################################
import os
import glob
import time
import logging
import subprocess
import random
import GPSHelper
import serial
import ConfigHelper

#Creacion del logger para los logs del servicio de GPS
loggerLog2 = logging.getLogger('server_logger2')
loggerLog2.setLevel(logging.INFO)
inf2 = logging.FileHandler('/data/lirevenas/logs/gpsdata.log')
inf2.setLevel(logging.INFO)
formatterInformer2 = logging.Formatter('[%(asctime)s][%(levelname)s]%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
inf2.setFormatter(formatterInformer2)
loggerLog2.addHandler(inf2)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/lirevenas/logs/gpsService.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#Metodo que crea la traza base que se escribira en FS
def creacionTraza(gpsData):
        return "|" + str(gpsData[0].split(".")[0]) + "|" + str(gpsData[1]) + "," + str(gpsData[2]) + "|" + str(gpsData[3]) + "|" + str(gpsData[4]) + "|" + str(gpsData[5]) + "|"

#################################################################################
#	Inicio Aplicacion #
#################################################################################

loggerLog.info("[GPSService][Main] Inicio");
usbGPS = ConfigHelper.getUsbGPS()
loggerLog.info("[GPSService][Main][Conf] Puerto USB GPS: " + usbGPS);

loggerLog.info("[GPSService][Main][Conf] Inicio configuracion puerto serie...")
puertoUSB=serial.Serial(usbGPS, timeout = 5.0, baudrate=9600)
loggerLog.info("[GPSService][Main][Conf] Puerto serie configurado!")

loggerLog.info("[GPSService][Main][Conf] Inicio Configuracion GPS...")
x = GPSHelper.UbxStream(puertoUSB)
loggerLog.info("[GPSService][Main][Conf] Reset Configuracion inicial...")
x.reset_config()
loggerLog.info("[GPSService][Main][Conf] Reset OK!")
loggerLog.info("[GPSService][Main][Conf] Recuperacion configuracion inicial GPS...")
x.load_config()
loggerLog.info("[GPSService][Main][Conf] Configuracion inicial recuperada OK")
loggerLog.info("[GPSService][Main][Conf] Desabilitar mensajes NMEA...")
x.disable_NMEA()
loggerLog.info("[GPSService][Main][Conf] Mensajes desabilitados OK")
#x.disable_message(240,1)
#x.disable_message(240,2)
#x.disable_message(240,3)
#x.disable_message(240,5)

loggerLog.info("[GPSService][Main][Conf] Activacion de mensajes NMEA utiles...")
#Activacicion del NMEA GGA
x.enable_message(240,0)
loggerLog.info("[GPSService][Main][Conf] Activacion de GGA")
#Activacicion del NMEA RMC
x.enable_message(240,4)
loggerLog.info("[GPSService][Main][Conf] Activacion de RMC")
#Configuracion del modo airbone<1g
x.nav_config(6)
loggerLog.info("[GPSService][Main][Conf] Activacion del modo Airbone 1g")
#Guardado de la configuracion
x.save_config()
loggerLog.info("[GPSService][Main][Conf] Guardado de la configuracion OK")

loggerLog.info("[GPSService][Main] Lectura primera posicion GPS...")
gpsData = GPSHelper.getGPSData(usbGPS)
loggerLog.info("[GPSService][Main] Primera posicion GPS leida OK")
tiempoMuestreoGPS = ConfigHelper.getTiempoMuestreoGPS()
loggerLog.info("[GPSService][Main] Tiempo de muestreo: " + str(tiempoMuestreoGPS))
loggerLog.info("[GPSService][Main] Recuperacion fecha y hora exacta...")
gpsDataExtendet = GPSHelper.getGPSDataExtendet(usbGPS)
loggerLog.info("[GPSService][Main] Fecha y hora recuperadas: " + str(gpsDataExtendet[3]) + " " + str(gpsDataExtendet[4]))
loggerLog.info("[GPSService][Main] Seteando la fecha y hora nuevas en el SO...")
command = "sudo date " + str(gpsDataExtendet[4][2:4]) + str(gpsDataExtendet[4][0:2]) + str(gpsDataExtendet[3][0:2]) + str(gpsDataExtendet[3][2:4]) + "20" + str(gpsDataExtendet[4][4:6]) + "." + str(gpsDataExtendet[3][4:6])
os.system(command)
loggerLog.info("[GPSService][Main] Fecha seteada OK!")

while True:

	try:
		#loggerLog.info("[GPSService][Main] Pasa1")
		gpsData = GPSHelper.getGPSData(puertoUSB)
		#loggerLog.info("[GPSService][Main] Pasa2")
		gpsDataExtendet = GPSHelper.getGPSDataExtendet(puertoUSB)
		#loggerLog.info("[GPSService][Main] Pasa3")
		gpsDataExtendet[0] = gpsData[0]
		#loggerLog.info("[GPSService][Main] Pasa4")
		loggerLog2.info(creacionTraza(gpsDataExtendet))
		#loggerLog.info("[GPSService][Main] Pasa5")
		time.sleep(tiempoMuestreoGPS)
	except:
		loggerLog.error("[GPSService][Main] Se ha producido un error inesperado, se continua iterando...")
		time.sleep(5)

