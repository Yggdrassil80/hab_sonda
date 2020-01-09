#################################################################################
#               Proyecto:   uvService                                           #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import time
import logging
import UVHelper.veml6070 as veml6070

import ConfigHelper

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/lirevenas/logs/uvdata.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s|', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/lirevenas/logs/uvService.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

tiempoMuestreoUV = ConfigHelper.getTiempoMuestreoUV()
act = ConfigHelper.isUVActivo()

loggerLog.info("[uvService] tiempoMuestreoUV: " + str(tiempoMuestreoUV))

veml = veml6070.Veml6070()

if act == 1:

	while True:
		try:
  			veml.set_integration_time(veml6070.INTEGRATIONTIME_4T)
  			uv_raw = veml.get_uva_light_intensity_raw()
			uv = veml.get_uva_light_intensity()
			logger.info(str(round(uv,2)))
			time.sleep(tiempoMuestreoUV)
		except Exception, e:
			loggerLog.error("[uvService] Exception: " + str(e))
			loggerLog.error("[uvService] Se ha producido un error, se sigue iterando...")
			time.sleep(5)

else:
	loggerLog.warn("[uvService] El modulo no esta activado!")

