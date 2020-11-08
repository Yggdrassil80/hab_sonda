#################################################################################
#               Proyecto:   bmpService                                          #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import time
import logging
import BMPHelper.BMP280 as BMP280

import ConfigHelper

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/hab_sonda/logs/bmpdata.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s|', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/hab_sonda/logs/bmpService.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

sensor = BMP280()

act = ConfigHelper.isBMPActivo()
tiempoMuestreoBMP = ConfigHelper.getTiempoMuestreoBMP()

loggerLog.info("[bmpService] tiempoMuestreoBMP: " + str(tiempoMuestreoBMP))

if act == 1:

	while True:

		try:
                        #INICIO: Espacio para recuperar los datos del sensor a partir de la libreria
			#loggerLog.info("[bmpService] inicio")
			bmpTemp = sensor.get_temperature()
			#loggerLog.info("[bmpService] temperatura leida")
			bmpPres = sensor.get_pressure()
			#loggerLog.info("[bmpService] presion leida")
			bmpAlti = sensor.get_altitude()
			#loggerLog.info("[bmpService] alturaleida")

                        #Escritura de datos en el archivo de datos del sensor. Todo lo que se escriba aqui sera lo que potencialmente se acabe enviando por telemetria.
			logger.info(str(round(bmpTemp,2)) + "|" + str(round(bmpPres,4)) + "|" + str(int(bmpAlti)))

                        #FINAL: Espacio para recuperar los datos del sensor a partir de la libreria
			time.sleep(tiempoMuestreoBMP)

		except Exception as e:
			loggerLog.error("[bmpService] Exception: " + str(e))
			loggerLog.error("[bmpService] Se ha producido un error, se sigue iterando...")
			time.sleep(5)
else:
	loggerLog.warn("[bmpService] El sensor no ha sido activado!")
