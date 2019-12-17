#!/usr/bin/python

import time
import math
import logging
import ConfigHelper

import MPUHelper.mpu6050 as mpu6050

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/lirevenas/logs/mpudata.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s|', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/lirevenas/logs/mpuService.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

################################################################################

sensor = mpu6050(0x68)

act = ConfigHelper.isMPUActivo()
tiempoMuestreoMPU = ConfigHelper.getTiempoMuestreoMPU()

loggerLog.info("[mpuService] tiempoMuestreoMPU: " + str(tiempoMuestreoMPU))

if act == 1:

	while True:

		try:
			acel_data = sensor.get_accel_data()
			gyro_data = sensor.get_gyro_data()
			temp_data = sensor.get_temp()

			ax = acel_data["x"]
			ay = acel_data["y"]
			az = acel_data["z"]
			gx = gyro_data["x"]
			gy = gyro_data["y"]
			gz = gyro_data["z"]

			dgx_tmp = math.degrees(gx)
			dgy_tmp = math.degrees(gy)
			dgz_tmp = math.degrees(gz)

			dgx = dgx_tmp % 360
			dgy = dgy_tmp % 360
			dgz = dgz_tmp % 360

			logger.info(str(round(ax,4)) + "|" + str(round(ay,4)) + "|" + str(round(az,4)) + "|" + str(round(dgx,4)) + "|" + str(round(dgy,4)) + "|" + str(round(dgz,4)) + "|" + str(round(temp_data,2)));

			#print "acel_data: " + "x:" + str(ax) + "y:" + str(ay) + "z:" + str(az)
			#print "gyro_data: " + "x:" + str(dgx) + "y:" + str(dgy) + "z:" + str(dgz)

			time.sleep(tiempoMuestreoMPU)

		except Exception, e:
			loggerLog.error("[mpuService] Exception: " + str(e))
			loggerLog.error("[mpuService] Se ha producido un error... se sigue iterando")
			time.sleep(5)

else:
	loggerLog.warn("[mpuService] El modulo no esta activado!")
