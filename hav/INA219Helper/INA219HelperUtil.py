#!/usr/bin/python

import logging
import time
import sys
import os

#Metodo que recupera solo los datos de voltage del bus del INA219 del archivo de datos del servicio
def getINA219DataFromFile():
    ina219Data = ["ERROR"]
    try:
        with open('/data/lirevenas/logs/ina219data.log') as ina219datafile:
            line = list(ina219datafile)[-1]
        bdata = line.split('|')
        ina219Data[0] = str(bdata[1])
        return ina219Data
    except:
        return ina219Data

