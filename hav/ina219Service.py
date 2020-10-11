#################################################################################
#               Proyecto:   ina219Service                                      #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import time
import logging
import INA219Helper.ina219 as ina219
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219


import ConfigHelper

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/lirevenas/logs/ina219data.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s|', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/lirevenas/logs/ina219Service.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

tiempoMuestreoINA219 = ConfigHelper.getTiempoMuestreoINA219()

loggerLog.info("[Ina219Service] tiempoMuestreoIna219: " + str(tiempoMuestreoINA219))

i2c_bus = board.I2C()
ina219 = INA219(i2c_bus)

ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.bus_voltage_range = BusVoltageRange.RANGE_32V

while True:

    try:
        busvoltage1 = -100
        shuntvoltage1 = -100
        current_mA1 = -100

        loggerLog.info("[Ina219Service] inicio")
        busvoltage1 = ina219.bus_voltage
        shuntvoltage1 = ina219.shunt_voltage
        current_mA1 = ina219.current / 1000

        logger.info(str(round(busvoltage1,4)) + "|" + str(round(shuntvoltage1,4)) + "|" + str(round(current_mA1,4)))
        time.sleep(tiempoMuestreoINA219)
    except Exception as e:
        loggerLog.error("[Ina219Service] Exception: " + str(e))
        loggerLog.error("[Ina219Service] Se ha producido un error, se sigue iterando...")
        time.sleep(5)
