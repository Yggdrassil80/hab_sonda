#!/usr/bin/python

import time
import serial
#import logging
import sys

#Creacion del loger para los datos cientificos
#loggerLog = logging.getLogger('server_logger-RF')
#loggerLog.setLevel(logging.INFO)
#inf = logging.FileHandler('/data/wsp-virolai/logs/wsp-RF.log')
#inf.setLevel(logging.INFO)
#formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
#inf.setFormatter(formatterInformer)
#loggerLog.addHandler(inf)

#Metodo que recupera la ultima linea de un arhivo y la envia por RF
def putUltimoDatoRF(usbPort, archivoDatos):
	
	try:
		#loggerLog.info("[RFHelper][putUltimoDatoRF] Inicio");
		#loggerLog.debug("[RFHelper][putUltimoDatoRF] usbPort: " + usbPort + " archivoDatos: " + archivoDatos);

		#loggerLog.debug("[RFHelper][putUltimoDatoRF] Apertura puerto serie para leer...");
        	#abrir el puerto para poder enviar datos al chip de RF
        	puertoUSB=serial.Serial(usbPort)
		#loggerLog.debug("[RFHelper][putUltimoDatoRF] Puerto abierto");
        	#abrir el archivo de datos de los sensores y recuperar la ultima linea
		#loggerLog.debug("[RFHelper][putUltimoDatoRF] Apertura archivo de log de datos...");
        	f=file(archivoDatos,"r")
        	lastLine = f.readlines()[-1]
       		#print ('Datos leidos: ' + lastLine)
		#loggerLog.debug("[RFHelper][putUltimoDatoRF] Datos leidos");
		f.close()
		#loggerlog.debug("[RFHelper][putUltimoDatoRF] Archivo cerrado");

		#Enviar byte a byte por RF
		for dato in lastLine:
			#loggerLog.debug("[RFHelper][putUltimoDatoRF] Inicio envio datos...");
			bytesEscritos = puertoUSB.write(dato)
			#loggerLog.debug("[RFHelper][putUltimoDatoRF] Dato enviado!");
			time.sleep(0.05)
			
			#print ('Datos enviados: ' + str(dato))
        	
		#loggerLog.debug("[RFHelper][putUltimoDatoRF] Todos los datos enviados OK");

		#bytesEscritos = puertoUSB.write(lastLine.encode('utf-8'))
		#print ('Datos enviados: ' + str(bytesEscritos))	

		#vaciar el buffer de salida para asegurarse que no se queda nada que pueda mezclarse con el siguiente dato
		#puertoUSB.flushInput()
		#puertoUSB.flushOutput()
        	#Cerrar el puerto USB
        	puertoUSB.close()
		#loggerLog.info("[RFHelper][putUltimoDatoRF] Puerto Serial cerrado. Final");
		return bytesEscritos
	except Exception:
   		e = sys.exc_info()[1]
    		print(e.args[0])
		#loggerLog.error("[RFHelper][putUltimoDatoRF] " + e.args[0]);
		#loggerLog.error("[RFHelper][putUltimoDatoRF] Error");
		return 0

#Metodo que coge una imagen y la envia por RF
def putUltimaImagenRF(usbPort, nombreImagen):

	#print("usbPort: " + usbPort)
        #print("Imagen: " + str(nombreImagen))

	bytesEnviados = int(0)

	#abrir el puerto para poder enviar datos al chip de RF
        puertoUSB=serial.Serial(usbPort)

	#abrir la imagen a enviar
	buffersize = 512
	input = open(str(nombreImagen), 'rb')
	buffer = input.read(buffersize)

	while len(buffer):
		for dato in buffer:
			bytesEscritos = puertoUSB.write(dato)
	               	time.sleep(0.05)
			#print ('Datos enviados: ' + str(bytesEscritos))
			bytesEnviados = bytesEnviados + 1
			#print ('bytes Enviados: ' + str(bytesEnviados))
	
		buffer = input.read(buffersize)
		
	#vaciar el buffer de salida para asegurarse que no se queda nada que pueda mezclarse con el siguiente dato
        puertoUSB.flushInput()
	puertoUSB.flushOutput()

	puertoUSB.close()

	return bytesEnviados

#Metodo que envia el codigo de preambulo de envio de datos o final de envio de datos
def putCodigo(usbPort, codigo):
	#print("usbPort: " + usbPort)
        #print("codigo: " + str(codigo))

	#abrir el puerto para poder enviar datos al chip de RF
        puertoUSB=serial.Serial(usbPort)

	for dato in codigo:
		bytesEscritos = puertoUSB.write(dato)
		time.sleep(0.02)

        #print('codigo: ' + codigo + ' enviado OK')
	
	#vaciar el buffer de salida para asegurarse que no se queda nada que pueda mezclarse con el siguiente dato
        puertoUSB.flushInput()
	puertoUSB.flushOutput()

	puertoUSB.close()

        return codigo



