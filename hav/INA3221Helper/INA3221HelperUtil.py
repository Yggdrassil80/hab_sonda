#!/usr/bin/python

import logging
import time
import sys
import os

#Metodo que recupera los datos del UV del archivo de datos del servicio
def getINA3221DataFromFile():
    ina3221Data = ["ERROR", "ERROR", "ERROR"]
    try:
        with open('/data/hab_sonda/logs/ina3221data.log') as ina3221datafile:
            line = list(ina3221datafile)[-1]
        bdata = line.split('|')
        ina3221Data[0] = str(bdata[1])
        ina3221Data[1] = str(bdata[2])
        ina3221Data[2] = str(bdata[3])
        return ina3221Data
    except:
        return ina3221Data

