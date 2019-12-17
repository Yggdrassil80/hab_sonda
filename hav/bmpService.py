#!/usr/bin/python

# Can enable debug output by uncommenting:
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
inf = logging.FileHandler('/data/lirevenas/logs/bmpService.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.

sensor = BMP280()

# Optionally you can override the bus number:
#sensor = BMP085.BMP085(busnum=2)

# You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER,
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.
#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

act = ConfigHelper.isBMPActivo()
tiempoMuestreoBMP = ConfigHelper.getTiempoMuestreoBMP()

loggerLog.info("[bmpService] tiempoMuestreoBMP: " + str(tiempoMuestreoBMP))

if act == 1:

	while True:

		try:
			loggerLog.info("[bmpService] inicio")
			bmpTemp = sensor.get_temperature()
			#loggerLog.info("[bmpService] temperatura leida")
			bmpPres = sensor.get_pressure()
			#loggerLog.info("[bmpService] presion leida")
			bmpAlti = sensor.get_altitude()
			#loggerLog.info("[bmpService] alturaleida")

			logger.info(str(round(bmpTemp,2)) + "|" + str(round(bmpPres,4)) + "|" + str(int(bmpAlti)))

			time.sleep(tiempoMuestreoBMP)

		except Exception, e:
			loggerLog.error("[bmpService] Exception: " + str(e))
			loggerLog.error("[bmpService] Se ha producido un error, se sigue iterando...")
			time.sleep(5)
else:
	loggerLog.warn("[bmpService] El sensor no ha sido activado!")
