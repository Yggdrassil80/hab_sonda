#!/usr/bin/python

import ConfigParser
import logging
import time
import sys
import os

#Metodo que recupera los datos del UV del archivo de datos del servicio
def getUVDataFromFile():
        uvData = ["ERROR"]
        try:
                with open('/data/chuteless/logs/uvdata.log') as uvdatafile:
                        line = list(uvdatafile)[-1]
                bdata = line.split('|')
                bmpData[0] = str(bdata[1])
                return uvData
        except:
                return uvData

