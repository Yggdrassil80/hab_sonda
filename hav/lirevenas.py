#################################################################################
#		Proyecto:   ChuteLess						#
#		Autor: Oscar Loras Delgado					#
#										#
#################################################################################

import os
import glob
import time
import logging

import random

import RFHelper
import GPSHelper
import GSMHelper
import BMPHelper
import MPUHelper
#import Camara
import ConfigHelper

#import Adafruit_BMP.BMP085 as BMP085

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/chuteless/logs/sensores.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(message)s', datefmt='%H%M%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/chuteless/logs/chuteless.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

################################################################################

#Metodo que recupera la lista de sensores que se utilizaran
def getSensorsArray():
	#return ["temperatura1","temperatura2","presion","camara"]
	loggerLog.info("[getSensorsArray] Inicio/Fin");
	return ["tExt1","tInt1","press","altbar","velvert","velterr"]

#################################################################################

#Metodo que se encarga esperar un cierto tiempo antes de volver a tomar datos con los sensores
def esperarTiempoMuestreoDatos():
	t = ConfigHelper.getTiempoMuestreoConf()
	time.sleep(t)

#Metodo que se encarga de esperar un cierto tiempo antes de tomar una foto con la picam
def esperarTiempoTomaImagenes():
	t = ConfigHelper.getTiempoMuestreoImg()
	time.sleep(t)

#Metodo que dado un sensor y la informacion GPS basica, genera un dato y lo registra en FS
def getDatoSensor(sensor, vel):

	if sensor == "tExt1":
		t = getDataTempExt1()
	if sensor == "tInt1":
		t = getDataTempInt1()
	if sensor == "press":
		t = getDataPresion1()
	if sensor == "altbar":
		t = getBarometricAltitude()
	if sensor == "velvert":
		t = vel
	if sensor == "velterr":
                t = getVelTerreno()

	return str(t)

#Metodo que recupera la temperatura externa (esta en el BMP)
def getDataTempExt1():
	try:
		bmpData = BMPHelper.getBMPDataFromFile()
		return bmpData[0]
	except:
		return float(0)

#metodo que recupera la presion externa (esta en el BMP)
def getDataPresion1():
	try:
		bmpData = BMPHelper.getBMPDataFromFile()
		return bmpData[1]
	except:
		return str("0")

#Metodo que recupera la altura barometrica (esta en el BMP)
def getBarometricAltitude():
        try:
                bmpData = BMPHelper.getBMPDataFromFile()
                return bmpData[2]
        except:
                return int(0)

#Metodo que recupera la temperatura interna (esta en el MPU)
def getDataTempInt1():
	try:
		mpudata = MPUHelper.getMPUDataFromFile()
		return mpudata[6]
	except:
		return float(0)


#Metodo que recupera la velocidad respecto al suelo (esta en el GPS)
def getVelTerreno():
	try:
		gpsdata = GPSHelper.getGPSDataFromFile()
		return gpsdata[5]
	except:
		return float(0)

#################################################################################
#	Sensor Temperatura Externa1						#
#################################################################################

#Metodo que crea la traza base que se escribira en FS
def creacionTraza(gpsData):
	loggerLog.info("[chuteless][creacionTraza] Inicio/fin")
        return str(gpsData[1]) + ";" + str(gpsData[2]) + ";" + str(gpsData[0]) + ";"

#Metodo que anade un dato a la traza que se escribira en FS
def addDatoTraza(nombreSensor, datoSensor):
	loggerLog.info("[chuteless][addDatoTraza] Inicio/fin [" + nombreSensor + "][" + str(datoSensor) + "]")
        return datoSensor + ":"

#################################################################################
#	Inicio Aplicacion							#
#################################################################################

loggerLog.info("[chuteless][Main] Inicio");
usbGPS = ConfigHelper.getUsbGPS()
loggerLog.info("[chuteless][Main][Conf] Puerto USB GPS: " + usbGPS);
usbRF = ConfigHelper.getUsbRF()
loggerLog.info("[chuteless][Main][Conf] Puerto USB RF: " + usbRF);
usbGSM = ConfigHelper.getUsbGSM()
loggerLog.info("[chuteless][Main][Conf] Puerto USB SMS: " + usbGSM);

maxAlturaGSM = ConfigHelper.leerAlturaGSMActivacion();
loggerLog.info("[chuteless][Main][Conf] Altura de activacion del GSM: "+ str(maxAlturaGSM))

#GPSHelper.activacionGPS(modo)
loggerLog.info("[chuteless][Main] Lectura primera posicion GPS...")
#gpsData = GPSHelper.getGPSData(usbGPS)
gpsData = GPSHelper.getGPSDataFromFile()
loggerLog.info("[chuteless][Main] Primera posicion GPS leida OK")

trazaBase = ''
trazaAcc = ''

#maxTiempoImagen = ConfigHelper.getMaxTiempoImagen()
#loggerLog.info("[chuteless][Main][Conf] MaxTiempoImagen: " + str(maxTiempoImagen))
maxTiempoTrazaGSM = ConfigHelper.getMaxTiempoTrazaGSM()
loggerLog.info("[chuteless][Main][Conf] MaxTiempoTrazaGSM: " + str(maxTiempoTrazaGSM))
#resolucionRF = ConfigHelper.getResolucionImagenRF()
#loggerLog.info("[chuteless][Main][Conf] ResolucionRF: " + str(resolucionRF))
#resolucionMax = ConfigHelper.getResolucionImagenMax()
#loggerLog.info("[chuteless][Main][Conf] resolucionMax: " + str(resolucionMax))
#basePathImage = ConfigHelper.getPathImagenesBase()
#loggerLog.info("[chuteless][Main][Conf] basePathImage: " + str(basePathImage))
listaMoviles = ConfigHelper.getListaMoviles()
loggerLog.info("[chuteless][Main][Conf] listaMoviles: " + str(listaMoviles))
pinGSM = ConfigHelper.getPinGSM()
loggerLog.info("[chuteless][Main][Conf] pin tarjeta GSM: " + str(pinGSM))

#Constante inicial para iniciar los calculos de velocidad
tAntVel = 1500000000
hAntVel = GPSHelper.getAltura(gpsData)

loggerLog.info("[chuteless][Main][vel] tAntVel: " + str(tAntVel) + " hAntVel: " + str(hAntVel))

loggerLog.info("[chuteless][Main] Inicializacion de contadores de envio de traza por RF y GSM")
t = 0
tgsm = 0

sensors = getSensorsArray()

while True:

	try:

		tActVel = int(round(time.time()))
		hActVel = GPSHelper.getAltura(gpsData)

		loggerLog.debug("[chuteless][Main][vel] tAntVel: " + str(tAntVel) + " hAntVel: " + str(hAntVel))
		loggerLog.debug("[chuteless][Main][vel] tActVel: " + str(tAntVel) + " hActVel: " + str(hAntVel))

		vel = (hActVel - hAntVel) / (tActVel - tAntVel)

		loggerLog.info("[chuteless][Main][vel] Velocidad calculada: " + str(vel))

		hAntVel = hActVel
		tAntVel = tActVel

		trazaBase = creacionTraza(gpsData)

		loggerLog.info("[chuteless][Main] Inicio bucle sensores...")
		for nombreSensor in sensors:
			#Tomar datos del sensor $sensor
			datoSensor = getDatoSensor(nombreSensor, round(vel,4))
			trazaAcc += addDatoTraza(nombreSensor, datoSensor)
		loggerLog.info("[chuteless][Main] Fin bucle sensores")

		logger.info(trazaBase + trazaAcc)
		trazaGSM = trazaBase + trazaAcc

		loggerLog.debug("[chuteless][Main] Traza de sensores creada con info: " + str(trazaBase) + str(trazaAcc))

		trazaAcc = ''
		esperarTiempoMuestreoDatos()

		loggerLog.debug("[chuteless][Main] Envio de traza almacenada en log por RF...")
		RFHelper.putUltimoDatoRF(usbRF, '/data/chuteless/logs/sensores.log')
		loggerLog.debug("[chuteless][Main] Traza enviada OK")

#		if t > maxTiempoImagen:
#			loggerLog.info("[chuteless][Main] Inicio de toma de imagen de camara interna...")
#			#Toma imagen de alta resolucion para despues
#			nombreImagen = Camara.tomarImagen(gpsData, resolucionMax, basePathImage, int(5), "HD", "png")
#			loggerLog.info("[chuteless][Main] Imagen tomada OK")
#			#Toma Image de baja resolucion para su envio
#			#nombreImagen = Camara.tomarImagen(gpsData, resolucionRF, basePathImage, int(3), "RF", "jpeg")
#			#nombreImagenRaw = Camara.convertirImagenToRaw(nombreImagen, basePathImage)
#
#			#RFHelper.putUltimaImagenRF(usbRF, nombreImagen)
#			t = 0
#		else:
#			time.sleep(1)
#			t = t + 1

		#Se recupera la altura GPS a la que se encuentra el globo.
		h = GPSHelper.getAltura(gpsData)

#		#Si la altura real esta por debajo de la altura de activacion del GSM,
#		#se abilita para que este intente enviar la telemetria por SMS
		loggerLog.debug("[chuteless][Main] Si h: " + str(h) + " mas pequeno que maxalturaGSM: " + str(maxAlturaGSM) + " se activara la telemetria por SMS")
#		#print("h: " + str(h) + " maxalturaGSM: " + str(maxAlturaGSM))
		if h < maxAlturaGSM:
			#Para evitar enviar muchos SMS, se pone un contador configurable.
			#No se tendra RT pero servira para la localizacion una vez aterrizado.
			#print("tgsm: " + str(tgsm) + " maxTiempoTrazaGSM: " + str(maxTiempoTrazaGSM))
			loggerLog.debug("[chuteless][Main] Si tiempo de activacion de GSM ha llegado al maxTiempoTrazaGSm entonces se envia SMS: tgsm " + str(tgsm) + " maxTiempoTrazaGSM: " + str(maxTiempoTrazaGSM))
			if tgsm > maxTiempoTrazaGSM:
				loggerLog.debug("[chuteless][Main] Inicio de envio de SMS...")
				GSMHelper.putDatosGSM(usbGSM, '/data/chuteless/logs/sensores.log',listaMoviles, pinGSM)
				loggerLog.debug("[chuteless][Main] SMS enviado OK")
				tgsm = 0
			else:
				time.sleep(1)
				tgsm = tgsm + 1

		loggerLog.debug("[chuteless][Main] Toma de datos de GPS nuevos para la nueva traza...")
		gpsData = GPSHelper.getGPSDataFromFile()
		loggerLog.debug("[chuteless][Main] Datos GPS obtenidos OK")
	except:
		loggerLog.error("[chuteless][Main] Se ha producido un error inesperado, se continua iterando...")
		time.sleep(5)
