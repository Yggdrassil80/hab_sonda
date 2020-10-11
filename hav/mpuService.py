#################################################################################
#               Proyecto:   mpuService                                          #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import time
import math
import logging
import ConfigHelper

import MPUHelper.mpu9250 as mpu9250

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/hab_sonda/logs/mpudata.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s|', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/hab_sonda/logs/mpuService.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

################################################################################

sensor = mpu9250.MPU9250()

act = ConfigHelper.isMPUActivo()
tiempoMuestreoMPU = ConfigHelper.getTiempoMuestreoMPU()

loggerLog.info("[mpuService] tiempoMuestreoMPU: " + str(tiempoMuestreoMPU))

if act == 1:

    while True:

        try:
            acel_data = sensor.readAccel()
            gyro_data = sensor.readGyro()
            magt_data = sensor.readMagnet()
            temp_data = sensor.readTemperature()

            ax = acel_data["x"]
            ay = acel_data["y"]
            az = acel_data["z"]
            gx = gyro_data["x"]
            gy = gyro_data["y"]
            gz = gyro_data["z"]
            mx = magt_data["x"]
            my = magt_data["y"]
            mz = magt_data["z"]

            dgx_tmp = math.degrees(gx)
            dgy_tmp = math.degrees(gy)
            dgz_tmp = math.degrees(gz)

            dgx = dgx_tmp % 360
            dgy = dgy_tmp % 360
            dgz = dgz_tmp % 360

            logger.info(str(round(ax,4)) + "|" + str(round(ay,4)) + "|" + str(round(az,4)) + "|" + str(round(dgx,4)) + "|" + str(round(dgy,4)) + "|" + str(round(dgz,4)) + "|" + str(round(mx,4)) + "|" + str(round(my,4)) + "|" + str(round(mz,4)) + "|" + str(round(temp_data,2)));

	    #print "acel_data: " + "x:" + str(ax) + "y:" + str(ay) + "z:" + str(az)
	    #print "gyro_data: " + "x:" + str(gx) + "y:" + str(gy) + "z:" + str(gz)
            #print "magt_data: " + "x:" + str(mx) + "y:" + str(my) + "z:" + str(mz)
            #print "temp: " + str(temp_data)

            time.sleep(tiempoMuestreoMPU)

        except Exception as e:
            #print("[mpuService] Exception: " + str(e))
            loggerLog.error("[mpuService] Exception: " + str(e))
            loggerLog.error("[mpuService] Se ha producido un error... se sigue iterando")
            time.sleep(5)
else:
    loggerLog.warn("[mpuService] El modulo no esta activado!")
