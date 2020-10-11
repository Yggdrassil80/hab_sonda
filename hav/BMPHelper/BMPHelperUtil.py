#!/usr/bin/python

#import ConfigParser
import logging
import time
import sys
import os

#Metodo que recupera los datos del BMP del archivo de datos del servicio
def getBMPDataFromFile():
        #logger.info(str(bmpTemp) + "|" + str(bmpPres) + "|" + str(bmpAlti))
        bmpData = [float(0), int(0), float(0)]
        try:
                with open('/data/hab_sonda/logs/bmpdata.log') as bmpdatafile:
                        line = list(bmpdatafile)[-1]
                bdata = line.split('|')
                bmpData[0] = float(bdata[1])
                bmpData[1] = int(bdata[2])
                bmpData[2] = int(bdata[3])
                return bmpData
        except:
                return bmpData

