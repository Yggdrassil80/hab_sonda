#!/usr/bin/python

import ConfigParser
import logging

#loggerLog = logging.getLogger('server_logger-config')
#loggerLog.setLevel(logging.INFO)
#inf = logging.FileHandler('/data/lirevenas/logs/wsp-Config.log')
#inf.setLevel(logging.INFO)
#formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
#inf.setFormatter(formatterInformer)
#loggerLog.addHandler(inf)

CONF_PATH = "/data/lirevenas/conf/hav.conf"

#Metodo que informa sobre la configuracion de la traza de sensores que se quiere enviar
def getConfiguracionTraza():

    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        conf = cfg.get("Sensores", "configuracionTraza")
        return conf
    except:
        return "null"


#Metodo que informa sobre el estado de activacion del INA3221
def isINA3221Activo():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("INA3221", "ina3221_activo")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][isINA3221Activo] ERROR");
        return "valor vacio"

#Metodo que recupera el tiempo de muestreo del UV
def getTiempoMuestreoINA3221():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("INA3221", "tiempoMuestreoINA3221")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][getTiempoMuestreoINA3221] ERROR");
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del UV
def isUVActivo():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("UV", "uv_activo")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][isUVActivo] ERROR");
        return "valor vacio"

#Metodo que recupera el tiempo de muestreo del UV
def getTiempoMuestreoUV():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("UV", "tiempoMuestreoUV")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][getTiempoMuestreoUV] ERROR");
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del MPU
def isMPUActivo():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("MPU", "mpu_activo")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][isMPUActivo] ERROR");
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del BMP
def isBMPActivo():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("BMP", "bmp_activo")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][isBMPActivo] ERROR");
        return "valor vacio"

#Metodo que informa sobre el estado de activacion del GSM
def isGSMActivo():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("GSM", "gsm_activo")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][isGSMActivo] ERROR");
        return "valor vacio"

#Metodo que informa sobre el estado de activacion de la camara
def isCamaraActivo():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("Camara", "camara_activo")
        return int(t)
     except:
        #loggerLog.error("[ConfigHelper][isCamaraActivo] ERROR");
        return "valor vacio"

#Metodo que recupera el tiempo de muestreo del MPU
def getTiempoMuestreoMPU():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("MPU", "tiempoMuestreoMPU")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][getTiempoMuestreoGPS] ERROR");
        return "valor vacio"


#metodo que recupera el tiempo de muestreo del GPS
def getTiempoMuestreoGPS():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("GPS", "tiempoMuestreoGPS")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][getTiempoMuestreoGPS] ERROR");
        return "valor vacio"

#Metodo que devuelve el tiempo de muestreo del sensor BMP085
def getTiempoMuestreoBMP():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("BMP", "tiempoMuestreoBMP")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][getTiempoMuestreoBMP] ERROR");
        return int(-1)

#Metodo que recupera el modo de vuelo del Hav (pre-vuelo o vuelo)
def leerModoVueloConf():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        modo = cfg.get("modo_vuelo", "modo")
        return modo
    except:
        #loggerLog.error("[ConfigHelper][leerModoVueloConf] ERROR");
        return "null"

#Metodo que recupera la altura a partir de la cual se desactivara el envio de datos por GSM
def leerAlturaGSMActivacion():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        h = cfg.get("GSM", "alturaActivacion")
        return float(h)
    except:
        #loggerLog.error("[ConfigHelper][leerAlturaGSMActivacion] ERROR");
        return float(1)

#Metodo que recupera el intervalo en segundos entre toma y toma de datos de los sensores
def getTiempoMuestreoConf():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        h = cfg.get("Sensores", "tiempoMuestreo")
        return int(h)
    except:
        #loggerLog.error("[ConfigHelper][getTiempoMuestreoConf] ERROR");
        return int(10)

#Metodo que recupera el intervalo en segundos para tomar una imagen
def getMaxTiempoImagen():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        h = cfg.get("Camara", "tiempoTomaImagen")
        return int(h)
    except:
        #loggerLog.error("[ConfigHelper][getMaxTiempoImagen] ERROR");
        return int(10)

#Metodo que recupera la resolucion de la imagen que tomara la camara
def getResolucionImagenRF():

    resolucion = [int(0),int(0)]

    try:
        cfg = ConfigParser.ConfigParser()
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

        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        resolucion[0] = cfg.get("Camara", "resolucionMaxX")
        resolucion[1] = cfg.get("Camara", "resolucionMaxY")
        return resolucion

#Metodo que recupera el path base donde se almacenaran las imagenes
def getPathImagenesBase():

    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        pathBase = cfg.get("Camara", "pathImagenesBase")
        return pathBase
    except:
        #loggerLog.error("[ConfigHelper][getPathImagenesBase] ERROR");
        return "Error path"

#Metodo que recupera el puerto del usb de RF
def getUsbRF():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        puerto = cfg.get("RF", "usbRF")
        return puerto
    except:
        #loggerLog.error("[ConfigHelper][getUsbRF] ERROR");
        return "Puerto Vacio"

#Metodo que recupera el puerto del usb de GPS
def getUsbGPS():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        puerto = cfg.get("GPS", "usbGPS")
        return puerto
    except:
        #loggerLog.error("[ConfigHelper][getUsbGPS] ERROR");
        return "Puerto Vacio"

#Metodo que recupera el puerto del usb de GSM
def getUsbGSM():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        puerto = cfg.get("GSM", "usbGSM")
        return puerto
    except:
        #loggerLog.error("[ConfigHelper][getUsbGSM] ERROR");
        return "Puerto Vacio"


#Metodo que recupera el tiempo maximo de espera para el envio de una traza de telemetria por SMS
def getMaxTiempoTrazaGSM():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        t = cfg.get("GSM", "tiempoTrazaGSM")
        return int(t)
    except:
        #loggerLog.error("[ConfigHelper][getMaxTiempoTrazaGSM] ERROR");
        return int(60)

#Metodo que recupera la lista de moviles a los cuales se enviaran los datos de telemetria
def getListaMoviles():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        listaMoviles = cfg.get("GSM", "listaMoviles")
        return listaMoviles
    except:
        #loggerLog.error("[ConfigHelper][getListaMoviles] ERROR");
        return "000000000"

#Metodo que recupera el pin de la tarjeta que lleva el SIM900A
def getPinGSM():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read([CONF_PATH])
        pin = cfg.get("GSM", "pin")
        return pin
    except:
        #loggerLog.error("[ConfigHelper][getPinGSM] ERROR");
        return "0000"
