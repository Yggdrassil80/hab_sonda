#################################################################################
#               Proyecto:   GSMService                                          #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import os
import glob
import time
import logging

import random

import GSMHelper
import ConfigHelper

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/GSMService.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%$')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#pseudocodigo

#1.   Inicializar el GSM
#2.   Comprobar que el archivo sensores.log existe
#2.1. si existe
#2.2.   coger la ultima linea y enviar. Esperar tiempodeenvioGSM y volver a comprobar si el archivo sensores.log$
#2.3. si no existe
#2.4.   Esto seria un estado de emergencia en el cual se asume que no hay datos de sensores.
# Se pasaria a intentar enviar la ultima linea del archivo de log del servicio de GPS

