#################################################################################
#               Proyecto:   ina3221Service                                      #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import time
import logging
import INA3221Helper.ina3221 as ina3221

import ConfigHelper

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/lirevenas/logs/ina3221data.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s|', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/lirevenas/logs/ina3221Service.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

tiempoMuestreoINA3221 = ConfigHelper.getTiempoMuestreoINA3221()

loggerLog.info("[Ina3221Service] tiempoMuestreoIna3221: " + str(tiempoMuestreoINA3221))

ina = ina3221.SDL_Pi_INA3221(active_channels="111")

CHANNEL1 = 1
CHANNEL2 = 2
CHNANEL3 = 3

while True:
	try:

		busvoltage1 = -100
		shuntvoltage1 = -100
		current_mA1 = -100
		loadvoltage1 = -100

		busvoltage2 = -100
                shuntvoltage2 = -100
                current_mA2 = -100
                loadvoltage2 = -100

		busvoltage3 = -100
                shuntvoltage3 = -100
                current_mA3 = -100
                loadvoltage3 = -100

		loggerLog.info("[Ina3221Service] inicio")
  		busvoltage1 = ina.getBusVoltage_V(CHANNEL1)
		shuntvoltage1 = ina.getShuntVoltage_mV(CHANNEL1)
		current_mA1 = ina.getCurrent_mA(CHANNEL1)
		loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)

		busvoltage2 = ina.getBusVoltage_V(CHANNEL2)
                shuntvoltage2 = ina.getShuntVoltage_mV(CHANNEL2)
                current_mA2 = ina.getCurrent_mA(CHANNEL2)
                loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000)
		#busvoltage3 = ina.getBusVoltage_V(CHANNEL3)
                #shuntvoltage3 = ina.getShuntVoltage_mV(CHANNEL3)
                #current_mA3 = ina.getCurrent_mA(CHANNEL3)
                #loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000)

		logger.info(str(round(busvoltage1,4)) + "|" + str(round(shuntvoltage1,4)) + "|" + str(round(current_mA1,4)) + "|" + str(round(loadvoltage1,4)) 
			+ "|" + str(round(busvoltage2,4)) + "|" + str(round(shuntvoltage2,4)) + "|" + str(round(current_mA2,4)) + "|" + str(round(loadvoltage2,4)) 
			+ "|" + str(round(busvoltage3,4)) + "|" + str(round(shuntvoltage3,4)) + "|" + str(round(current_mA3,4)) + "|" + str(round(loadvoltage3,4)))
		time.sleep(tiempoMuestreoINA3221)
	except Exception, e:
		loggerLog.error("[Ina3221Service] Exception: " + str(e))
		loggerLog.error("[Ina3221Service] Se ha producido un error, se sigue iterando...")
		time.sleep(5)
