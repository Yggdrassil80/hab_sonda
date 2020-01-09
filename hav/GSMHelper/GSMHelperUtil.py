#!/usr/bin/python
import serial
import os, time
import logging

loggerLog = logging.getLogger('server_logger-GSM')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/lirevenas/logs/wsp-GSM.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#Metodo que envia una traza por SMS a una lista de telefonos
def putDatosGSM(usbPort, archivoDatos, listaMoviles, pin):
	
	try:
		loggerLog.info("[GSMHelper][putDatosGSM] Inicio");
		loggerLog.debug("[GSMHelper][putDatosGSM] usbPort: " + usbPort + " archivoDatos: " + archivoDatos);

        	#abrir el archivo de datos de los sensores y recuperar la ultima linea
        	loggerLog.debug("[GSMHelper][putDatosGSM] Apertura del archivo de datos...");
		f=file(archivoDatos,"r")
		loggerLog.debug("[GSMHelper][putDatosGSM] Archivo abierto OK!");
        	lastLine = f.readlines()[-1]
		loggerLog.debug("[GSMHelper][putDatosGSM] lectura de la ultima linea de datos: " + lastLine);
        	#print ('Datos leidos: ' + lastLine)
        	f.close()
		enviarSMS(usbPort, lastLine, listaMoviles, pin)
		loggerLog.debug("[GSMHelper][putDatosGSM] Fin");
        	return bool("true")
	except:
		loggerLog.error("[GSMHelper][putDatosGSM] ERROR");
		return bool("false")

#Metodo que envia un sms al SIM900A para que lo envie a una lista de moviles
def enviarSMS(usbPort, lastLine, listaMoviles, pin):
	
	try:
		loggerLog.info("[GSMHelper][enviarSMS] Inicio");
		loggerLog.debug("[GSMHelper][enviarSMS] usbPort: " + usbPort + " lastLine: " + lastLine + " listaMoviles: " + listaMoviles + " pin: " + pin);

		lm = listaMoviles.split(',')

		loggerLog.debug("[GSMHelper][enviarSMS] Abriendo puerto...");
		port = serial.Serial(usbPort, baudrate=9600, timeout=1)
		loggerLog.debug("[GSMHelper][enviarSMS] Puerto abierto");

		for tel in lm:
			loggerLog.debug("[GSMHelper][enviarSMS] Enviando SMS para telefono: " + tel);

			#6207
        		#Se informa el pin de la tarjeta
			loggerLog.info("[GSMHelper][enviarSMS] Informar el PIN de la tarjeta...");
        		port.write('AT+CPIN=' + pin + '\r\n')
        		rcv = port.read(64)
       			print rcv
			loggerLog.info("[GSMHelper][enviarSMS] Pin puesto: " + rcv);
        		time.sleep(1)

        		#Seleccion del modo de SMS en texto
        		loggerLog.info("[GSMHelper][enviarSMS] Seleccion del modo SMS en Texto...");
			port.write('AT+CMGF=1'+'\r\n')
        		rcv = port.read(64)
        		print rcv
			loggerLog.info("[GSMHelper][enviarSMS] Modo seleccionado: " + rcv);
        		time.sleep(1)

			loggerLog.info("[GSMHelper][enviarSMS] Configuracion del telefono al que se enviara el SMS...");
			#Configuracion de numero de telefono al que enviar el sms
			port.write('AT+CMGS=\"' + tel  + '\"\r\n')
			rcv = port.read(64)
			print rcv
			loggerLog.info("[GSMHelper][enviarSMS] Telefono configurado: " + rcv);
			time.sleep(1)

			#Escritura del mensaje
			loggerLog.info("[GSMHelper][enviarSMS] Escritura del mensaje...");
			port.write(lastLine)
			rcv = port.read(160)
			print rcv
			loggerLog.info("[GSMHelper][enviarSMS] Mensaje escrito: " + rcv);
			time.sleep(1)
	
			#Escritura del caracter ctrl-Z que hace de final de cadena y envio
			loggerLog.info("[GSMHelper][enviarSMS] Escritura del ctrl-Z que envia el SMS");
			port.write(chr(26))
			rcv = port.read(10)
			print rcv
			loggerLog.info("[GSMHelper][enviarSMS] Mensaje enviado: " + rcv);
			time.sleep(1)

			#Reset de parametros de configuracion a estado inicial
                	loggerLog.info("[GSMHelper][enviarSMS] Restitucion configuracion inicial...");
			port.write('AT+ATZ\r\n')
                	rcv = port.read(64)
                	print rcv
			loggerLog.info("[GSMHelper][enviarSMS] Configuracion restituida: " + rcv);
                	time.sleep(1)

		loggerLog.info("[GSMHelper][enviarSMS] Fin de la lista de telefonos. Cerrando puerto...");
		port.close()
		loggerLog.info("[GSMHelper][enviarSMS] Puerto cerrado");
		loggerLog.info("[GSMHelper][enviarSMS] Fin");
		return bool("true")
	except:
		loggerLog.info("[GSMHelper][enviarSMS] Error");
		return bool("false")
