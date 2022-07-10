#!/usr/bin/python

import configparser
import logging

#loggerLog = logging.getLogger('server_logger-config')
#loggerLog.setLevel(logging.INFO)
#inf = logging.FileHandler('/data/hab_sonda/logs/wsp-Config.log')
#inf.setLevel(logging.INFO)
#formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
#inf.setFormatter(formatterInformer)
#loggerLog.addHandler(inf)

CONF_PATH = "/data/hab_sonda/conf/hav.conf"

#Metodo que informa sobre la configuracion de la traza de sensores que se quiere enviar
def getConfiguracionTraza():

    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        conf = cfg.get("Sensores", "configuracionTraza")
        return conf
    except:
        return "null"

#Metodo que informa sobre el estado de activacion del INA3221
def isINA219Activo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("INA219", "ina219_activo")
        return int(t)
    except:
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del INA3221
def isINA3221Activo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("INA3221", "ina3221_activo")
        return int(t)
    except:
        return "valor vacio"

def getTiempoMuestreoINA219():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("INA219", "tiempoMuestreoINA219")
        return int(t)
    except:
        return "valor vacio"

#Metodo que recupera el tiempo de muestreo del UV
def getTiempoMuestreoINA3221():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("INA3221", "tiempoMuestreoINA3221")
        return int(t)
    except:
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del UV
def isUVActivo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("UV", "uv_activo")
        return int(t)
    except:
        return "valor vacio"

#Metodo que recupera el tiempo de muestreo del UV
def getTiempoMuestreoUV():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("UV", "tiempoMuestreoUV")
        return int(t)
    except:
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del MPU
def isMPUActivo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("MPU", "mpu_activo")
        return int(t)
    except:
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del BMP
def isBMPActivo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("BMP", "bmp_activo")
        return int(t)
    except:
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del GSM
def isGSMActivo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("GSM", "gsm_activo")
        return int(t)
    except:
        return "valor vacio"

#Metodo que informa sobre el estado de activacion de la camara
def isCamaraActivo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("Camara", "camara_activo")
        return int(t)
    except:
        return "valor vacio"

#Metodo que recupera el tiempo de muestreo del MPU
def getTiempoMuestreoMPU():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("MPU", "tiempoMuestreoMPU")
        return int(t)
    except:
        return "valor vacio"

#metodo que recupera el tiempo de muestreo del GPS
def getTiempoMuestreoGPS():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("GPS", "tiempoMuestreoGPS")
        return int(t)
    except:
        return "valor vacio"

#Metodo que devuelve el tiempo de muestreo del sensor BMP085
def getTiempoMuestreoBMP():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("BMP", "tiempoMuestreoBMP")
        return int(t)
    except:
        return int(-1)

#Metodo que recupera el intervalo en segundos entre toma y toma de datos de los sensores
def getTiempoMuestreoConf():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        h = cfg.get("Sensores", "tiempoMuestreo")
        return int(h)
    except:
        return int(10)

#Metodo que recupera el intervalo en segundos para tomar una imagen
def getTiempoTomaImagen():
    try:
        cfg = configparser.configParser()
        cfg.read([CONF_PATH])
        h = cfg.get("Camara", "tiempoTomaImagen")
        return int(h)
    except:
        return int(10)

#Metodo que recupera la resolucion de la imagen que tomara la camara
def getResolucionImagenRF():

    resolucion = [int(0),int(0)]

    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        resolucion[0] = cfg.get("Camara", "resolucionRFX")
        resolucion[1] = cfg.get("Camara", "resolucionRFY")
        return resolucion
    except:
        #loggerLog.error("[ConfigHelper][getMaxTiempoImagen] ERROR");
        return resolucion

#Devuelve los datos de resolucion maxima con la que se tomaran imagenes
def getResolucionImagenMax():

        resolucion = [int(0),int(0)]

        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        resolucion[0] = cfg.get("Camara", "resolucionMaxX")
        resolucion[1] = cfg.get("Camara", "resolucionMaxY")
        return resolucion

#Metodo que recupera el path base donde se almacenaran las imagenes
def getPathImagenesBase():

    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        pathBase = cfg.get("Camara", "pathImagenesBase")
        return pathBase
    except:
        return "Error path"

#Metodo que recupera el puerto del usb de RF
def getUsbRF():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        puerto = cfg.get("RF", "usbRF")
        return puerto
    except:
        return "Puerto Vacio"

#Metodo que recupera el puerto del usb de GPS
def getUsbGPS():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        puerto = cfg.get("GPS", "usbGPS")
        return puerto
    except:
        return "Puerto Vacio"

#Metodo que recupera el puerto del usb de GSM
def getUsbGSM():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        puerto = cfg.get("GSM", "usbGSM")
        return puerto
    except:
        return "Puerto Vacio"

#Metodo que recupera el tiempo maximo de espera para el envio de una traza de telemetria por SMS
def getMaxTiempoTrazaGSM():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("GSM", "tiempoTrazaGSM")
        return int(t)
    except:
        return int(60)

#Metodo que recupera la lista de moviles a los cuales se enviaran los datos de telemetria
def getListaMoviles():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        listaMoviles = cfg.get("GSM", "listaMoviles")
        return listaMoviles
    except:
        return "000000000"

#Metodo que recupera el pin de la tarjeta que lleva el SIM900A
def getPinGSM():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        pin = cfg.get("GSM", "pin")
        return pin
    except:
        return "0000"

#Metodo que recupera la altura a partir de la cual se desactivara el envio de datos por GSM
def leerAlturaGSMDesactivacion():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        h = cfg.get("GSM", "alturaDesactivacion")
        return float(h)
    except:
        return float(1)

#Metodo que recupera la altura a partir de la cual se activara el envio de datos por GSM
def leerAlturaGSMActivacion():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        h = cfg.get("GSM", "alturaActivacion")
        return float(h)
    except:
        return float(1)

#Metodo que recupera el el identificador de misión del HAB
def getIDMision():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        idmision = cfg.get("RF", "idMision")
        return idmision
    except:
        #loggerLog.error("[ConfigHelper][getIDMision] ERROR");
        return "HABCAT00"

#Metodo que informa sobre el estado de activacion del sensor de temperatura DS18B20(dallas)
def isDallasActivo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("dallas", "dallas_activo")
        return int(t)
    except:
        return "valor vacio"

#Metodo que recupera el tiempo maximo de espera entre tomas de temperatura del sensor DS18B20(dallas)
def getTiempoMuestreoDallas():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("dallas", "tiempoTrazaDallas")
        return int(t)
    except:
        return int(60)

#Metodo que informa si la configuracion para el procesamiento NDVI de las imagenes esta activa o no
def isNDVIConfigurationActivo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("Camara", "ndviProcessingActive")
        return int(t)
    except:
        return "valor vacio"

#Metodo que informa el path base donde se escribiran las imagenes ndvi despues de su procesamiento
def getNDVIBasePath():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        pathBase = cfg.get("Camara", "ndviBasePath")
        return pathBase
    except:
        return "/data/hab_sonda/utilities/ndvi"

#Metodo que devuelve el balance de rojos de la camara para su configuracion compatible con el procesamiento ndvi
def getRedAWB():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        red = cfg.get("Camara", "redAWB")
        return float(red)
    except:
        return float(1)

#Metodo que devuelve el balance de azules de la camara para su configuracion compatible con el procesamieento ndvi
def getBlueAWB():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        blue = cfg.get("Camara", "blueAWB")
        return float(blue)
    except:
        return float(1)

def isRuleActivo():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("rules", "rules_activo")
        return int(t)
    except:
        return "valor vacio"

def getTiempoMuestreoMotorReglas():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("rules", "tiempoMuestreoMotorReglas")
        return int(t)
    except:
        return int(60)

def getListaSensoresOperables():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        conf = cfg.get("rules", "listaSensoresOperables")
        return conf
    except:
        return "null"

def getRuleList():
    try:
        cfg = configparser.ConfigParser()
        cfg.read([CONF_PATH])
        conf = cfg.get("rules", "listaReglas")
        return conf
    except:
        return "null"