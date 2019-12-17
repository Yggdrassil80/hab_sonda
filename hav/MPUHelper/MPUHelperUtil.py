#!/usr/bin/python

import ConfigParser
import logging
import time
import sys
import os

#Metodo que recupera los datos del MPU del archivo de datos del servicio
def getMPUDataFromFile():
        #logger.info(str(round(ax,4)) + "|" + str(round(ay,4)) + "|" + str(round(az,4)) + "|" + str(round(dgx,4)) + "|" + str(round(dgx,4)) + "|" + str(rou
	#nd(dgy,4)) + "|" + str(round(dgz,4)) + "|" + str(round(temp_data,4)));

	mpuData = [float(0), float(0), float(0), float(0), float(0), float(0), float(0)]
        try:
                with open('/data/chuteless/logs/mpudata.log') as mpudatafile:
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


