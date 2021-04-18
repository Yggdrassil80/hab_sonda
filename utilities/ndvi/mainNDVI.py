#!/usr/bin/env python

#PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/sbin:/bin:/data/ndviMachine/src/

from imgPreProcess import PreProcess
import matplotlib
import imgNDVIProcess 
import os
import time
import signal

print("[ndviProcess] Arrancando Procesamiento de imagenes por NDVI...: ")
matplotlib.use('Agg')

NDVIWorkspacePath = "/data/hab_sonda/utilities/ndvi"
print("[ndviProcess] NDVIWorkspacePath: " + str(NDVIWorkspacePath))
imageBasePath = "/data/hab_sonda/images"
print("[ndviProcess] imageBasePath: " + str(imageBasePath))

#para cada foto que haya en imageBasePath hacer
for rawCapture in os.listdir(imageBasePath):
    if rawCapture.endswith(".png"):
        print("[ndviProcess] Procesando imagen: " + rawCapture + " ...")
        processedFile=imgNDVIProcess.ndvi(rawCapture, imageBasePath + "/" + rawCapture, imageBasePath, NDVIWorkspacePath+'/ndvi/' + 'ndvi_' + rawCapture)
        while not os.path.exists(NDVIWorkspacePath+'/ndvi/' + 'ndvi_' + rawCapture):
            print("[ndviProcess] Imagen: "+ "ndvi_" + rawCapture + " procesda OK!")
            time.sleep(5)

print("[ndviProcess] Todas las imagenes procesadas OK!")



