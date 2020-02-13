#!/usr/bin/python

import time
import sys
import os

#Metodo que recupera los datos del MPU del archivo de datos del servicio
def getMPU6050DataFromFile():

    mpuData = [float(0), float(0), float(0), float(0), float(0), float(0), float(0)]
    try:
        with open('/data/lirevenas/logs/mpudata.log') as mpudatafile:
            line = list(mpudatafile)[-1]
        mdata = line.split('|')
        mpuData[0] = float(mdata[1])
        mpuData[1] = float(mdata[2])
        mpuData[2] = float(mdata[3])
        mpuData[3] = float(mdata[4])
        mpuData[4] = float(mdata[5])
        mpuData[5] = float(mdata[6])
        mpuData[6] = float(mdata[7])
        return mpuData
    except:
        return mpuData

#Metodo que recupera los datos del MPU del archivo de datos del servicio
def getMPU9250DataFromFile():

    mpuData = [float(0), float(0), float(0), float(0), float(0), float(0), float(0), float(0), float(0), float(0)]
    try:
        with open('/data/lirevenas/logs/mpudata.log') as mpudatafile:
            line = list(mpudatafile)[-1]
        mdata = line.split('|')
        mpuData[0] = float(mdata[1])
        mpuData[1] = float(mdata[2])
        mpuData[2] = float(mdata[3])
        mpuData[3] = float(mdata[4])
        mpuData[4] = float(mdata[5])
        mpuData[5] = float(mdata[6])
        mpuData[6] = float(mdata[7])
        mpuData[7] = float(mdata[8])
        mpuData[8] = float(mdata[9])
        mpuData[9] = float(mdata[10])

        return mpuData
    except:
        return mpuData



