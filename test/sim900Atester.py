#!/usr/bin/python
import serial      
import os, time
  

# Enable Serial Communication
port = serial.Serial("/dev/ttyUSB1", baudrate=9600, timeout=1)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

#port.write('AT&V'+'\r\n')
#rcv = port.read(10)
#print rcv
#time.sleep(1)

#port.write('AT'+'\r\n')
#rcv = port.read(10)
#print rcv
#time.sleep(1)

#port.write('ATE0'+'\r\n')      # Disable the Echo
#rcv = port.read(10)
#print rcv
#time.sleep(1)

#Envio de un sms

#Reinicio a la configuracion por defecto
#port.write('ATZ'+'\r\n')  
#rcv = port.read(64)
#print rcv
#time.sleep(1)

#Se informa el pin de la tarjeta
port.write('AT+CPIN=6207'+'\r\n')  
rcv = port.read(64)
print rcv
time.sleep(1)

#Seleccion del modo de SMS en texto
port.write('AT+CMGF=1'+'\r\n')  
rcv = port.read(64)
print rcv
time.sleep(1)

#Configuracion de numero de telefono al que enviar el sms
port.write('AT+CMGS=\"+34666269163\"\r\n')      
rcv = port.read(64)
print rcv
time.sleep(1)

#Escritura del mensaje
port.write('SMS-prueba-sim900a')
rcv = port.read(160)
print rcv
time.sleep(1) 

#Escritura del caracter ctrl-Z que hace de final de cadena y envio
port.write(chr(26))
rcv = port.read(10)
print rcv
time.sleep(1)








#port.write('AT+CMGF=0'+'\r\n')  # Select Message format as Text mode 
#rcv = port.read(10)
#print rcv
#time.sleep(1)

#port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
#rcv = port.read(10)
#print rcv
#time.sleep(1)
#
#port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
#rcv = port.read(10)
#print rcv
#time.sleep(1)
#
## Sending a message to a particular Number
#
#port.write('AT+CMGS="9495353464"'+'\r\n')
#rcv = port.read(10)
#print rcv
#time.sleep(1)
#
#port.write('Hello User'+'\r\n')  # Message
#rcv = port.read(10)
#print rcv
#
#port.write("\x1A") # Enable to send SMS
#for i in range(10):
#    rcv = port.read(10)
#    print rcv
#
