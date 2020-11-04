
#!/usr/bin/python

import logging
import serial
import time
import sys
import os

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger_gps') 
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/GPSlibrary.log')
inf.setLevel(logging.DEBUG) 
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S') 
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#Metodo que devuelve la altura del objeto gpsData
def getAltura(gpsData):
    loggerLog.debug("[GPSHelper][getAltura] Inicio/Fin")
    return int(gpsData[0])

def getGPSDataExtendetDummy(port):
    gpsDataExtendet = [int(0), float(41.2323), float(2.342), "114345", "260619", "6.112", "OK"]
    return gpsDataExtendet 

def getGPSDataDummy(port):
    gpsData = [int(456), float(41.2323), float(2.342), "OK"]
    return gpsData

#Metodo que recupera los datos de GPS del archivo de datos del servicio
def getGPSDataFromFile():
    #[2019-06-26 11:44:20][INFO]|456.232|41.2323,2.342|114345|260619|6.112|
    gpsData = [int(0), float(0), float(0), "", "", float(0), "KO"]
    try:
        loggerLog.debug("[GPSHelper][getGPSDataFromFile] Recuperando datos del servicio de GPS...")
        with open('/data/chuteless/logs/gpsdata.log') as gpsdatafile:
            line = list(gpsdatafile)[-1]
        loggerLog.debug("[GPSHelper][getGPSDataFromFile] ultima linea: " + line)
        gdata = line.split('|')
        gpsData[0] = int(gdata[1])
        coord = gdata[2].split(',')
        gpsData[1] = float(coord[0])
        gpsData[2] = float(coord[1])
        gpsData[3] = str(gdata[3])
        gpsData[4] = str(gdata[4])
        gpsData[5] = str(gdata[5])
        gpsData[6] = "OK"
        return gpsData
    except:
        loggerLog.error("[GPSHelper][getGPSDataFromFile] Error en la recuperacion de la ultima linea")
        return gpsData

#Metodo que recupera los datos basicos de posicion y altura del GPS
def getGPSData(ser):

    gpsData = [int(0), float(0), float(0), "KO"]
    try:
        data = ser.readline()
        loggerLog.debug("[GPSHelper][getGPSData] Lectura bruta del puerto: " + str(data))
        loggerLog.debug("[GPSHelper][getGPSData] Invocando el parser...")
        gpsData = parseGPS_GGA(data)
        loggerLog.debug("[GPSHelper][getGPSData] datos del parser: [0: " + str(gpsData[0]) + "][1: " + str(gpsData[1]) + "][2:" + str(gpsData[2]) + " ][3:" + str(gpsData[3]) + " ]")
        while gpsData[3] != "OK":
            data = ser.readline()
            loggerLog.debug("[GPSHelper][getGPSData] Lectura bruta del puerto: " + str(data))
            loggerLog.debug("[GPSHelper][getGPSData] Invocando el parser...")
            gpsData = parseGPS_GGA(data)
            time.sleep(0.05)
            loggerLog.debug("[GPSHelper][getGPSData] datos del parser: [0: " + str(gpsData[0]) + "][1: " + str(gpsData[1]) + "][2:" + str(gpsData[2]) + " ][3:" + str(gpsData[3]) + " ]")
        return gpsData
    except Exception:
        e = sys.exc_info()[1]
        print("[GPSHelper][getGPSData]" + str(e.args[0]))
        loggerLog.error("[GPSHelper][getGPSData] ERROR se retorna objeto invalido:" + e.args[0])
        return gpsData

#def setGPSFlyMode(port):
#	ser = serial.Serial(port, baudrate = 9600, timeout = 0.5) data = 0xB5, 0x62, 
#	0x06, 0x24, 0x24, 0x00, 0xFF, 0xFF, 0x06, 0x03, 0x00, 0x00, 0x00, 0x00, 0x10, 
#	0x27, 0x00, 0x00, 0x05, 0x00, 0xFA, 0x00, 0xFA, 0x00, 0x64, 0x00, 0x2C, 0x01, 
#	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
#	0x00, 0x16, 0xDC"

#metodo que se encarga de parsear los datos brutos de la mensajeria NMEA entrante por 
#puerto serie
def parseGPS_GGA(data):
    gpsData = [int(0), float(0), float(0), "KO"]
    try:
        loggerLog.debug("[GPSHelper][parseGPS_GGA] Inicio")
        # $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
        #     GGA Global Positioning System Fix Data 123519 Fix taken at 12:35:19 UTC 
        #     4807.038,N Latitude 48 deg 07.038' N 01131.000,E Longitude 11 deg 31.000' 
        #     E 1 Fix quality: 0 = invalid
        #               1 = GPS fix (SPS) 2 = DGPS fix 3 = PPS fix 4 = Real Time 
        #              Kinematic 5 = Float RTK
        #               6 = estimated (dead reckoning) (2.3 feature) 7 = Manual input 
        #              mode 8 = Simulation mode 08 Number of satellites being tracked 
        #              0.9 Horizontal dilution of position 545.4,M Altitude, Meters, 
        #              above mean sea level 46.9,M Height of geoid (mean sea level) 
        #              above WGS84
        #                      ellipsoid (empty field) time in seconds since last DGPS 
        #     update (empty field) DGPS station ID number *47 the checksum data, always 
        #     begins with *
        #loggerLog.debug("[GPSHelper][parseGPS_GGA] data[0:6]: " + str(data[0:6])
        gpgga_msg = b'$GPGGA'
        if (data[0:6] == gpgga_msg):
            loggerLog.debug("[GPSHelper][parseGPS_GGA] Mensaje $GPGGA encontrado")
            dataDecoded = data.decode("utf-8")
            s = dataDecoded.split(",")
            if s[7] == '0':
                loggerLog.debug("[GPSHelper][parseGPS_GGA] No hay satelites disponibles.")
                return
            loggerLog.debug("[GPSHelper][parseGPS_GGA] Satelites disponibles. Detectando campos vacios...")
            loggerLog.debug("[GPSHelper][parseGPS_GGA] s2:" + s[2] + "s4:" + s[4] + "s9:" + s[9])
            if ((s[2] == '') and (s[4] == '') and (s[9] == '')):
                loggerLog.debug("[GPSHelper][parseGPS_GGA] Campos vacios... devolvemos un KO")
                gpsData[0] = int(0)
                gpsData[1] = float(0)
                gpsData[2] = float(0)
                gpsData[3] = "KO"

                return gpsData

            loggerLog.debug("[GPSHelper][parseGPS_GGA] Datos validos.Recuperando...")
            time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
            lat = decode(s[2])
            dirLat = s[3]
            lon = decode(s[4])
            dirLon = s[5]
            if dirLon == 'W':
                lon = lon * -1
            
            alt = s[9]
            sat = s[7]

            loggerLog.debug("[GPSHelper][parseGPS_GGA] lat: " + str(lat) + " lon: " + str(lon))
            gpsData[0] = alt
            gpsData[1] = lat
            gpsData[2] = lon
            gpsData[3] = "OK"
        else:
            loggerLog.debug("[GPSHelper][parseGPS_GGA] Mensaje $GPGGA NO encontrado. Salir con KO")
            gpsData[0] = int(0)
            gpsData[1] = float(0)
            gpsData[2] = float(0)
            gpsData[3] = "KO"
        loggerLog.debug("[GPSHelper][parseGPS_GGA] Fin [0: " + str(gpsData[0]) + "][1: " + str(gpsData[1]) + "][2:" + str(gpsData[2]) + " ][3:" + str(gpsData[3]) + " ]")
        return gpsData
    except Exception as e:
        loggerLog.error("[GPSHelper][parseGPS_GGA] ERROR se retorna objeto invalido: " + str(e))
        return gpsData

#Metodo que transforma el formato de la coordenada
def decode(coord):
    # DDDMM.MMMMM -> XX.XXXXXXXX
	
    try:
        loggerLog.debug("[GPSHelper][decode] Inicio")
        coordenada = float(0)
        if coord != '':
            #print("[decode][cood: " + coord + "]")
            v = coord.split(".")
            head = v[0]
            tail = v[1]
            deg = head[0:-2]
            min = head[-2:]
            resto = float(str(min)+"."+str(tail))
            #print("resto:"+str(resto))
            grados = float(str(deg))
            #print("grados:"+str(grados))
            restoConv = resto / 60
            #print("resto:"+str(restoConv))
            coordenada = grados + restoConv
            loggerLog.debug("[GPSHelper][decode] coordenada:" + str(coordenada) + " Fin")
        else:
            coordenada = float(0)
            loggerLog.debug("[GPSHelper][decode] Coordenada vacia Fin")
        return coordenada
    except Exception as e:
        loggerLog.error("[GPSHelper][decode] ERROR se retorna coordenada a 0: " + str(e))
        return coordenada

#Metodo que recupera los datos basicos de posicion y altura del GPS
def parseGPS_RMC(data):

    gpsDataExtendet = [int(0), float(0), float(0), "", "", "", "KO"]

    try:
                #loggerLog.debug("[GPSHelper][parseGPS_RMC] Inicio")
                #$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
                #     RMC          Recommended Minimum sentence C
                # 1    123519       Fix taken at 12:35:19 UTC
                # 2    A            Status A=active or V=Void.
                # 3,4    4807.038,N   Latitude 48 deg 07.038' N
                # 5,6    01131.000,E  Longitude 11 deg 31.000' E
                # 7    022.4        Speed over the ground in knots
                # 8    084.4        Track angle in degrees True
                # 9    230394       Date - 23rd of March 1994
                # 10,11    003.1,W      Magnetic Variation
                # 12    *6A          The checksum data, always begins with

        time = "No valido"
        date = "No valido"
        speed = "No valido"

        gprmc_msg = b'$GPRMC'
        if  (data[0:6] == gprmc_msg):
            loggerLog.debug("[GPSHelper][parseGPS_RMC] Mensaje $GPRMC encontrado")
            dataDecoded = data.decode("utf-8")
            s = dataDecoded.split(",")
            if ((s[1] == '') or (s[3] == '') or (s[4] == '') or (s[5] == '') or (s[6] == '') or (s[7] == '') or (s[9] == '')):
                loggerLog.debug("[GPSHelper][gpsDataExtendet] Datos insufucientes para componer traza")
                return gpsDataExtendet
            loggerLog.debug("[GPSHelper][parseGPS_RMC] Datos validos. Recuperando...")
            time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
            lat = decode(s[3])
            dirLat = s[4]
            lon = decode(s[5])
            dirLon = s[6]

            if dirLon == 'W':
                lon = lon * -1

            speed = s[7]
            date = s[9][0:2] + "-" + s[9][2:4] + "-" + s[9][4:6]
            gpsDataExtendet[1] = lat
            gpsDataExtendet[2] = lon
            gpsDataExtendet[3] = time
            gpsDataExtendet[4] = date
            #Conversion de nudos a m/s
            gpsDataExtendet[5] = (float(speed)*float(0.514))
            gpsDataExtendet[6] = "OK"

        else:

            loggerLog.debug("[GPSHelper][parseGPS_RMC] Mensaje $GPRMC NO encontrado. Salir con KO")
            gpsDataExtendet[0] = int(0)
            gpsDataExtendet[1] = float(0)
            gpsDataExtendet[2] = float(0)
            gpsDataExtendet[3] = ""
            gpsDataExtendet[4] = ""
            gpsDataExtendet[5] = float(0)
            gpsDataExtendet[6] = "KO"

        loggerLog.debug("[GPSHelper][parseGPS_RMC] Fin [0: " + str(gpsDataExtendet[0]) + "][1: " + str(gpsDataExtendet[1]) + "][2:" + str(gpsDataExtendet[2]) + " ][3:" + str(gpsDataExtendet[3]) + "][4:" + time + "][5:" + date + "][6:" + speed)

        return gpsDataExtendet

    except Exception:
        e = sys.exc_info()[1]
        print("[GPSHelper][parseGPS_RMC]" + str(e.args[0]))
        loggerLog.error("[GPSHelper][parseGPS_RMC] ERROR se retorna objeto invalido: " + e.args[0])
        return gpsDataExtendet


#Metodo que recupera los datos basicos de posicion y altura del GPS
def getGPSDataExtendet(ser):

    gpsData = [float(0), float(0), float(0), "ERR", "ERR", "ERR", "KO"]
    try:
        #loggerLog.debug("[GPSHelper][getGPSDataExtendet] Arrancando comunicacion con GPS por puerto: " + port)
        #loggerLog.debug("[GPSHelper][getGPSDataExtendet] baudrate: 9500 timeout 0.5")
        #ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
        data = ser.readline()
        #loggerLog.debug("[GPSHelper][getGPSDataExtendet] Lectura bruta del puerto: " + data)
        loggerLog.debug("[GPSHelper][getGPSDataExtendet] Invocando el parser...")
        gpsData = parseGPS_RMC(data)
        loggerLog.debug("[GPSHelper][getGPSDataExtendet] datos del parser: [0: " + str(gpsData[0]) + "][1: " + str(gpsData[1]) +"][2:" + str(gpsData[2]) + " ][3:" + str(gpsData[3]) + " ]")
        while gpsData[6] != "OK":
            data = ser.readline()
            #loggerLog.debug("[GPSHelper][getGPSDataExtendet] Lectura bruta del puerto: " + data)
            gpsData = parseGPS_RMC(data)
            loggerLog.debug("[GPSHelper][getGPSDataExtendet] Invocando el parser...")
            time.sleep(0.05)
        loggerLog.debug("[GPSHelper][getGPSDataExtendet] datos del parser: [0: " + str(gpsData[0]) + "][1: " + str(gpsData[1]) +"][2:" + str(gpsData[2]) + " ][3:" + str(gpsData[3]) + " ]")
        return gpsData
    except Exception:
        e = sys.exc_info()[1]
        print("[GPSHelper][getGPSDataExtendet]" + str(e.args[0]))
        loggerLog.error("[GPSHelper][getGPSDataExtendet] ERROR se retorna objeto invalido:" + e.args[0])
        return gpsData
