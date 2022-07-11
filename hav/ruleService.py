#################################################################################
#               Proyecto:   ruleService                                         #
#               Autor: Oscar Loras Delgado                                      #
#                                                                               #
#################################################################################

import os
import time
import logging

import RuleHelper
from hav import ConfigHelper

BASE_PATH_LOG = "/data/hab_sonda/logs/"

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/hab_sonda/logs/ruledata.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s|', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/hab_sonda/logs/ruleService.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#Este servicio se encarga de recuperar los datos de todos los sensores que se le configuren que la sonda
#lleva a bordo. Carga una serie de reglas definidas en el archivo de configuración hav.conf y aplica dichas 
#reglas a los datos recuperados. La salida es un archivo ruledata.log donde figuran las acciones que otros componentes
#pueden hacer en función de estas reglas (aumentar frecuencias de envio, encender y apagar sistemas, etc.)

#Informa si el modulo esta o no activo
act = ConfigHelper.isRuleActivo()
#Tiempo de muestreo de los datos de los sensores
tiempoMuestreoMotorReglas = ConfigHelper.getTiempoMuestreoMotorReglas()
#Lista de sensores de los cuales el modulo de reglas leera datos para mirar de aplicar las reglas
listaSensoresOperables = ConfigHelper.getListaSensoresOperables()
#Lista de reglas definidas
listaReglas = ConfigHelper.getRuleList() 
#thresholdOp:{idOriginService}.{dataServicePosition}.{operator[lt/gt]}.{valueToEvaluate}:{idtargetService}.{{inputDataId}.{operator[eq]}.{valueInputDataToChange}/[activator]}
#
#Las reglas se separan unas de otras en la configuración por comas (,) simples
#Las reglas tienen 3 partes [tipo:reglaAEvaluar:AccionAEfectuar]
#Los campos reglaAEvaluar y AccionAEfectuar tienen mas campos que se separan entre ellos por puntos (.)
#
#thresholdOp: Informa que se trata de una regla de evaluacion de umbral
#idOriginService: Servicio origen del dato a evaluar
#dataServicePosition: Cada servcio ofrece X datos, este valor es un ordinal que informa sobre la posicion del dato del servicio que se quiere evaluara a comparar
#operator[lt/gt]: Operador logico, se admiten 2, "lt: less than" y "gt: greater than"
#valueToEvaluate: valor umbral con el que se comparara el dato del sensor
#idtargetService: Identificador del actuador/componente destino sobre el que se realizara la accion
#inputDataId: identificador del dato de entrada del servicio que se alterara
#operator[eq]: operador asignacion "eq: equal"
#valueInputDataToChange: valor del dato que se cambiara
#activator[on/off]: valor que activa o desactiva un servicio
#
#Ejemplo1:
#Regla que informa que si el campo 0 de los datos del gps (altura) es mas pequeña de 10000 metros se informara
#al servicio lora1 el campo freqEnvio que pase a ser de 10 segundos
#thresholdOp:gps.0.lt.10000:lora1.freqEnvio.eq.10
#
#Ejemplo2:
# Regla que informa que si el campo 0 del gps (altura) esta por debajo de 10000 metros, se active (on) ek servicio del buzzer
#thresholdOp:GPS.0.lt.10000:buzzer.on

def sensorLogFile(idSensor):
    path = BASE_PATH_LOG + idSensor + "data.log"
    loggerLog.debug("[RuleService][sensorLogFile] Archivo de sensores recuperado: " + str(path))
    return path

#Metodo que devuelve el nombre del sensor sobre el que aplica una regla
def getRuleSensor(rule):
	#thresholdOp:{idOriginService}.{dataServicePosition}.{operator[lt/gt]}.{valueToEvaluate}:{idtargetService}.{{inputDataId}.{operator[eq]}.{valueInputDataToChange}/[activator]}
	try:
		ruleComponent = rule.split(":")
		#Se retorna el {idOriginService}
		return ruleComponent[1]
	except:
		loggerLog.error("[RuleService][getRuleSensor] Exception: " + str(e))
		loggerLog.error("[RuleService][getRuleSensor] Se ha producido un error parseando la regla")
		return "NORULE"

#Metodo que ejecuta una regla.
#La ejecucion de una regla implica que se escribira un archivo de tipo token en FS que sera leido por el sensor en cuestion
#Este token informara sobre un aspecto de la configuracion que se debera alterar en el inicio de la accion que el sensor tenga
#que hacer, por ejemplo, alterar la frecuencia de toma de datos, apagarse, encenderse, etc.
#Esto implica necesariamente que todos los sensores que su configuracion pueda alterarse en tiempo de ejecucion soporten esto.
def executeRule(ruleComponent):
	#thresholdOp:{idOriginService}.{dataServicePosition}.{operator[lt/gt]}.{valueToEvaluate}:{idtargetService}.{{inputDataId}.{operator[eq]}.{valueInputDataToChange}/[activator]}
	try:
		lenRuleFields = len(ruleComponent)
		if lenRuleFields == 9:
			createTokenContent = ruleComponent[5] + ":" + ruleComponent[6] + ":" + ruleComponent[8] + ":"
		else:
			if lenRuleFields == 7:
				createTokenContent = ruleComponent[5] + ":" + ruleComponent[6] + ":"
			else:
				loggerLog.error("[RuleService][executeRule] Regla no reconocida!")
		f=open(ruleComponent[1],"w")
		f.write(createTokenContent)
		f.close()
	except:
		loggerLog.error("[RuleService][executeRule] Exception: " + str(e))
		loggerLog.error("[RuleService][executeRule] Se ha producido un error ejecutando la regla")


#Metodo que evalua una regla {rule} contra los datos de un sensor {sensorData} asumiendo que esta regla aplica a este sensor
def evaluateRule(rule, sensorData):
	#thresholdOp:{idOriginService}.{dataServicePosition}.{operator[lt/gt]}.{valueToEvaluate}:{idtargetService}.{{inputDataId}.{operator[eq]}.{valueInputDataToChange}/[activator]}
	try:
		ruleComponent = rule.split(":")
		#El dato a evaluar siempre esta en la posicion indicada en la regla+1 porque hay que saltar el nombre del sensor almacenado en el array
		dataToEvaluate = sensorData[ruleComponent[2]+1]
		operationToEvaluate = ruleComponent[3]
		thresholdToEvaluate = ruleComponent[4]
		if operationToEvaluate == "lt":
			if dataToEvaluate < thresholdToEvaluate:
				loggerLog.warn("[RuleService][evaluateRule] Aplicando regla [" + str(rule) + "]")
				#Se aplica la regla
				executeRule(ruleComponent)
			else:
				#No se aplica la regla
		else:
			if operationToEvaluate == "gt":
				if dataToEvaluate > thresholdToEvaluate:
					loggerLog.warn("[RuleService][evaluateRule] Aplicando regla [" + str(rule) + "]")
					#Se aplica la regla
					executeRule(ruleComponent)
				else:
					#No se aplica la regla
			else:
				loggerLog.warn("[RuleService][evaluateRule] OJO, no se puede evaluar la comparacion!")

	except:
		loggerLog.error("[RuleService][getRuleSensor] Exception: " + str(e))
		loggerLog.error("[RuleService][getRuleSensor] Se ha producido un error evaluando la regla [" + str(rule) + "]")

if act == 1:
	loggerLog.info("[RuleService] Motor de Reglas Activo: ")
	while True:

		try:
            #0.Leer los datos de los archivos *data.log de todos los sensores configurados con los que trabajara el motor de reglas
			trazaDatos = ""
			trazaDatosList = []
			for sensorType in listaSensoresOperables:
				loggerLog.debug("[HABMain][sensor: " + sensorType + "]")
				pathSensor = sensorLogFile(sensorType)
				if (os.path.exists(pathSensor)):
					f=open(pathSensor,"r")
					isSensorFileFull = os.stat(pathSensor).st_size>0
					if (isSensorFileFull):
						lastLine = f.readlines()[-1]
						loggerLog.debug("[RuleService] Ultima linea leida [" + lastLine + "]")
						#2.3.1 Para evitar el procesamiento del ultimo "|" se elimina.
						ll = lastLine[:-2]
						loggerLog.debug("[RuleService] Linea leida: [" + ll + "]")
						dataSensorArray = ll.split('|')
						i = 0
						datosProcesados = ""
						datosProcesadosList = []
						datosProcesadosList.append(sensorType)
						for data in dataSensorArray:
							if (i > 0):
								datosProcesados = datosProcesados + "|" + data
								datosProcesadosList.append(data)
							i = i + 1
							loggerLog.debug("[RuleService][datosProcesados: " + datosProcesados + "]")
						f.close()
						trazaDatos = trazaDatos + datosProcesados
						trazaDatosList.append(datosProcesadosList)
					else:
                    loggerLog.warn("[RuleService] OJO, si el sensor era el gps probablemente su archivo de datos este aun vacio...")
				else:
					loggerLog.warn("[RuleService] OJO, no se ha encontrado archivo de datos del sensor [" + sensorType + "]")
			loggerLog.debug("[RuleService][trazaDatos: " + trazaDatos + "]")
			#1.Para cada una de las reglas, ver si puede aplicarse sobre alguno de los datos disponibles
			for rule in listaReglas:
				for sensorData in trazaDatosList:
					if getRuleSensor(rule) == sensorData[0]:
						#1.1. Si encuentra una regla que se puede ejecutar, se ejecuta y genera un resultado temporal
						#2.Se almacenan todos los resultados temporales en una entrada en el archivo ruledata.log
						evaluateRule(rule, sensorData) 
					
			time.sleep(tiempoMuestreoMotorReglas)

		except Exception as e:
			loggerLog.error("[RuleService] Exception: " + str(e))
			loggerLog.error("[RuleService] Se ha producido un error, se sigue iterando...")
			time.sleep(5)
else:
	loggerLog.warn("[RuleService] El modulo de Motor de Reglas no ha sido activado! Consultar su activacion en el archivo hav.conf")
