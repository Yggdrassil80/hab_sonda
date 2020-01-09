- [HAB_sonda](#hab-sonda)
  * [Introducción](#introducci-n)
  * [Diseño](#dise-o)
    + [Introducción](#introducci-n-1)
    + [Diagrama del Hardware](#diagrama-del-hardware)
    + [Diagrama del Software](#diagrama-del-software)
  * [Modulos](#modulos)
    + [Introducción](#introducci-n-2)
    + [BMP](#bmp-1)
    + [MPU](#mpu)
    + [GPS](#gps)
    + [RF](#rf)
    + [UV](#uv)
    + [INA3221](#ina3221)
    + [GSM](#gsm)
    + [Camara](#camara)
    + [Proceso Principal](#proceso-principal)
    + [Servicio de Configuración](#servicio-de-configuraci-n)
  * [Configuraciones Genéricas](#configuraciones-gen-ricas)
    + [Activación I2C en Raspbian](#activaci-n-i2c-en-raspbian)
  * [Logging](#logging)
    + [Introducción](#introducci-n-13)
    + [Tipos de log](#tipos-de-log)

# HAB_sonda

## Introducción

Proyecto1 que recoge el código fuente base de una sonda de tipo HAB basada en Raspbian (Raspberry Pi ,3B o Zero W) y la gestión de la operación de sistemas diversos (Temperatura, Presión, Camara, Barometros, GPS, Radio Lora, Telemetria por SM, otros)

El proyecto se divide en varios directorios

- <b>hav</b>: Acronimo de High Altitude Vehicle, donde se almacena todo el código de los diferentes componentes que integran la sonda.
- <b>conf</b>: Directorio donde se almacena la configuración de los módulos que hay definidos en "hav"
- <b>services</b>: La definición de los daemons de los procesos que corren sobre cada sensor/componente que integra la sonda
- <b>test</b>: Directorio de pruebas donde se valida parte del software que hay en hav.

## Diseño

### Introducción

El software para la sonda esta pensado de forma que todos los procesos de generación de datos y de envio de datos se ejecuten como un proceso aislado. Luego, un proceso principal, que es el encargado de leer los archivos de datos que los procesos de los modulos de sensores van dejando y enviarlos por alguno de los mecanismos implementados (RF-Lora o SMS-GSM)

Este sistema permite que, en caso de fallo de alguno de estos sensores, buses u otros componentes, el resto de procesos sigan funcionando correctamente, aumentando la robustez del sistema. Esta arquitectura además permite una gran escalabilidad, pudiendo añadir sistemas nuevos o sistemas resilientes llegado al caso, con suma facilidad.

### Diagrama del Hardware

![alt Diagrama del hardware](/doc/img/Lirevenas_Diagrama_hardware.PNG)

### Diagrama del Software

![alt Diagrama del software](doc/img/Lirevenas_Diagrama_software_inicial.PNG)

## Modulos

### Introducción

Como se ha indicado, la idea es que cada componente nuevo que se agrege, se conciba como un servicio que se ejecute en el arranque de la pi en un orden preestablecido y con las dependencias que se desee.

Para poder arrancar el servicio de un componente:

1. Se debe disponer del archivo [Nombre_modulo.service] donde se ha de describir, genericamente, lo siguiente:

```
[Unit]
Description=[nombre_en_systemctl_del_servicio]
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /[path_hubicación_proceso_python_arranque_servicio]/[nombre_servicio].py
Restart=always
RestartSec=0

[Install]
WantedBy=multi-user.target
```

2. Copiar el archivo del servico al directorio de systemd
```
sudo cp [nombre_servicio].service /etc/systemd/system/[nombre_servicio].service
```

3. Refrescar la lista de servicios y activar el nuevo que se desea dar de alta.
```
sudo systemctl daemon-reload
sudo systemctl enable [nombre_servicio].service
```

<b>IMPORTANTE</b>: Asegurarse que el script de python definido en el [Nombre_modulo.service] tiene permisos de ejecución (chmod 755)
### BMP

4. Finalmente, para arrancar o parar el servicio una vez la el SO haya arrancado, utilizar.
```
sudo systemctl start [nombre_servicio].service

o

sudo systemctl stop [nombre_servicio].service
```

### BMP

#### Introducción

El módulo BMP testado es el BMP280. Básicamente se trata de un sensor de presión y temperatura all-in.

#### Descripción

Las funcionalidades de este sensor lo hacen especialmente interesante:
- Presión: Ofrece datos de presión atmosferica a nivel del mar en Pa (Pascales).
- Temperatura: Temperaturas en ºC
- Altura Barométrica: En base a la presión y la temperatura, dispone de modelos atmosféricos primitivos pero relativamente precesios de la altura a la que se encuentra el sensor. La altura es en metros.

Puede utilizarse para medir temperaturas externas o internas de la sonda, depende donde se ubique.

#### Conexión

Este componente se conecta a la Pi a través del bus I2C, luego no tiene requerimientos de conexión especiales.

Para la activación del bus I2C, revisar la sección de configuración "Activación I2C en Raspbian".

#### Calibración

Para conseguir unas medidas de temperatura y presión lo mas correctas posibles, es necesario calibrar adecuadamente dichos sensores. 

Existen dentro del código del módulo del BMP280 que se puede encontrar en hav/BMP280/BMP280.py hay un par de métodos que se pueden utilizar para este menester, el compensate_temperature y el compensate_pressure.

#### Configuracíón

El módulo dispone de confguración específica en el archivo conf/hav.conf

bmp_activo=1
tiempoMuestreoBMP=10

donde,

- bmp_activo: informa sobre el estado de activación del modulo, 0 o 1 en función de si se desea que este activo o no.
- tiempoMuestreoBMP: informa sobre el tiempo de toma de datos del sensor.


### MPU

#### Introducción

El sensor de MPU permite conocer la orientacion espacial de la sonda mediante el calculo de la acceleración (3 ejes), inclinación (3 ejes) y orientación magnetica (3 ejes).

El sensor con el que se trabajará es el MPU9250, que integra un giroscopio convencional para aceleración e inclinación y un magnetómetro para la orientación magnetica.

#### Descripción

Este sensor recupera los valores siguientes:
- ax: aceleración en el eje X
- ay: aceleración en el eje Y
- az: aceleración en el eje Z
- gx: inclinación en el eje X
- gy: inclinación en el eje Y
- gz: inclinación en el eje Z
- ox: orientación magnética en el eje X
- oy: orientación magnética en el eje Y
- oz: orientación magnética en el eje Z
- temp: temperatura del sensor embebido que lleva el circuito

En el caso de los sensores con magnetometros y giroscopios, para poder obtener medidas correctas y precisas, es necesario calibrar estos sistemas.

La calibración es un proceso algo mas complejo pero que se puede abordar perfectamente a través de una série de utilidades que se han desarrollado.

Se puede encontrar información de la calibración en el apartado siguiente.

#### Conexión

Este componente se conecta a la Pi a través de un bus I2C, con lo que no tiene ninguna complicación.

Para la activación del bus I2C, revisar la sección de configuración "Activación I2C en Raspbian".

#### Calibración

[TODO]

#### Configuracíón

El módulo dispone de confguración específica en el archivo conf/hav.conf

mpu_activo=1
tiempoMuestreoMPU=11

donde,

- mpu_activo: informa sobre el estado de activación del modulo, 0 o 1 en función de si se desea que este activo o no.
- tiempoMuestreoMPU: informa sobre el tiempo de toma de datos del sensor.

### GPS

#### Introducción

El GPS, permite determinar la ubicación exacta de la sonda. Su presencia y buen funcionamiento es capital para la recuperación de la misma.

#### Descripción

El GPS sobre el cual se basado este desarrollo es el UBLOX NEO 6M que también se ha demostrado compatible con el UBLOX NEO 7.

Lo que se desea del GPS es que retorne constantemente la altura, la latitud y la longitud de la sonda. Estos datos son solo unos de los pocos que se pueden extraer del GPS.

Actualmente, los chips de UBLOX operan con protocolo NMEA2.0 que se basa en la generación de una série de mensajes con datos de tiempos, velocidades, posiciones, etc.

Se puede encontrar mas información aqui: https://www.gpsinformation.org/dale/nmea.htm

Se ha desarrollado un módulo propio que interpreta los mensajes NMEA que se consideran interesantes para conocer los datos de altura, longitud y latitud de la sonda (GCRMC y el GCACC).

#### Conexión 

Los chips de ublox estan configurados para empezar a volcar sus datos directamente por el puerto serie. Con un simple adaptador a USB (CP2102) se puede utilizar practicamente desde cualquier sistema operativo o plataforma que soporte USB.

#### Calibrado

Este componente no requiere ninguna acción de calibrado especial, ya que tras el encendido empieza a calcular su posición el solo. Para ganar una precisión adecuada de pocos metros, si hace mucho que no se usa, puede requerir unos minutos (5 o 10 min).

#### Configuración

A diferencia de otros componentes, los chips de UBLOX de GPS requieren de configuración inicial dependiendo de lo que se desee hacer con ellos.

En nuestro caso, nuestra aplicación implica que se alcanzaran alturas de entre 30 a 40km en el mejor de los casos, y practicamente ningun GPS convencional mide tales alturas de fabrica.

Además, existe un organismo internacional, COCOM que limita la altura a la cual estos sistemas civiles pueden operar. Nominalmente esta en 18km como maximo, pero dependendiendo del fabricante hay limites en 9 o 12km.

Superado este limite, el comportamiento del componente es diverso, en función del fabricante. En el caso de UBLOX, los datos de lat, lon y altura se quedan "congelados" hasta que se recupera una altura inferior a la del límite de configuración.

Para solventar esto, el componente de GPS desarrollado implementa una libreria especial que permite la configuración de GPS de UBLOX mediante su protocolo de comunicaciones de fabricante (UBX). Luego, cada vez que se arranca el módulo de GPS, se lanza una configuración que activa el modo "airbone<1g" que permite la operación del chip hasta alturas de 50km.

Otras configuraciones adicionales son aplicadas también, como el filtrado de paquetes de NMEA, para solo capturar los GCRMC y GCACC.

Adicionalmente, también existen configuraciones estáticas en el archivo conf/hav.conf

usbGPS=/dev/ttyUSB0
tiempoMuestreoGPS=10

donde,

- usbGPS: corresponde al puerto USB al que esta conectado el adaptador cp2102 del GPS. Es importante destacar que este puerto puede cambiar en función de los dispositivos conectados a la raspberry y el slot USB donde se conecten, con lo que se deberá comprobar manualmente que esta configuración es correcta.
- tiempoMuestreoGPS: que informa sobre el tiempo entre muestras de datos de GPS. Es importante destacar que el GPS no empieza a dar datos de posición de forma inmediata cuando arranca, sino que requeriere unos minutos de "autocalibrado" antes de empezar a recibir paquetes NMEA con datos (GCRMC y GCACC). Luego, suponiendo la configuración correcta de USB, se puede entender como normal que no haya datos de posición nada mas arrancar.

[TODO]

### RF

#### Introducción

El modulo de RF que se utilizará es un ebyte E32-TTL-100 que esta basado en la tecnologia LoRa (Long Range) del chip SX1278 de Semtech.

Esta tecnología permite el envio de mensajes con muy poca energia a grandes distancias a coste eso si de un ancho de banda muy bajo.

Se utiliza para el envio de datos tomados por los sensores exceptuando las imagenes o videos de la cámara, ya que el ancho de banda no lo permite.

#### Descripción

El módulo seleccionado permite de ebyte viene ya preconfigurado. Se conecta a la raspberry a través del puerto serie y, mediante un adaptador CP2102, a un slot USB.

Dispone además de dos pines de configuración, M0 y M1 que, para que pueda funcionar en modo recepción y emisión han de estar a 0V (ojo, no en Z).

Para poder configurar los parametros internos del chip M0 y M1 han de configurarse ambos a 1 lógico (3.3 o 5 V).

Toda la configuración los parametros de LoRa del chip se basa en el parametro de airrate que viene a ser el ancho de banda con el que transmite el chip.

Los siguientes parámetros de configuración de LoRa son los que corresponden a cada airRate.

 - 0.3 Kbps, BW:125Mhz, SF: 12, CR: 4/5
 - 1.2 Kbps, BW:250Mhz, SF: 11, CR: 4/5
 - 2.4 Kbps, BW:500Mhz, SF: 12, CR: 4/5
 - 4.8 Kbps, BW:250Mhz, SF: 8, CR: 4/6
 - 9.6 Kbps, BW:500Mhz, SF: 8, CR: 4/6
 - 19.2 Kbps, BW:500Mhz, SF: 7, CR: 4/6

 donde,

 - BW: Significa BandWith
 - SF: Spread Factor
 - CR: Coding Rate

La frecuencia central se encuentra en los 433 Mhz.

No se tiene información sobre que sync_word o que longitud de preambulo se esta usando.

El airRate por defecto es de 2.4 Kbps.

El modulo de software desarrollado para este chip aisla todos estos elementos de configuración del desarrollador. 

Se ha de dejado un único método al cual se le pasa una cadena de texto (que representa, por ejemplo una linea del sensores.log) y la envia sin mas.

#### Configuración

Existe configuración estática para este modulo en el archivo de configuración conf/hav.conf

usbRF=/dev/ttyUSB2

donde,

- usbRF: corresponde al puerto USB al que esta conectado el adaptador cp2102 del componente de RF (Lora ebyte). Es importante destacar que este puerto puede cambiar en función de los dispositivos conectados a la raspberry y el slot USB donde se conecten, con lo que se deberá comprobar manualmente que esta configuración es correcta.


### UV

#### Introducción

El sensor UV es el encargado de registrar la radiación ultravioleta. Para ello se utilizará el sensor VEML6070.

#### Descripción

Actualmente el componente de UV solo mide los watts/m2 de radiación UV que le llegan al sensor. Es posible configurar este nivel de radiación con el estandar de peligrosidad que esta reconocido internacionalmente.

Los valores serian del 1 al 7 y a cada uno de ellos le corresponde tantos watts/m2.

Este indice no esta aun implementado.

#### Configuracíón

El módulo dispone de confguración específica en el archivo conf/hav.conf

uv_activo=1
tiempoMuestreoUV=10

donde,

- uv_activo: informa sobre el estado de activación del modulo, 0 o 1 en función de si se desea que este activo o no.
- tiempoMuestreoUV: informa sobre el tiempo de toma de datos del sensor.

### INA3221

#### Introducción

Los módulos INA permiten conocer el voltaje e intensidad que circulan por alguna de sus entradas.

Este módulo es muy util para conocer cual es el estado de la bateria o voltajes y corrientes generadas por potenciales paneles solares.

#### Conexión

El módulo ina3221 se conecta a través del bus I2C, con lo que no es precisa ninguna conexión especial salvo la alimentación, que se recomienda que se externa a 5V.

Para la activación del bus I2C, revisar la sección de configuración "Activación I2C en Raspbian".

#### Descripción

Esta versión de INA es la 3221 que permite, en un solo chip, hasta 3 canales de medida de voltajes e intensidades. Ahora bien, en las pruebas se ha constatado que se los canales estan comunicados, y que sin adaptaciones importantes en el módulo, no se pueden utilizar de forma aislada.

Si se usa solo para medir un canal, las medidas son correctas.

Los datos que permite recuperar son voltaje e intensidad.

* NOTA *: Es conveniente recordar que para que las medidas sean las correctas, para medir intensidad, el canal utilizado ha de estar en serie con el circuito y para medir voltaje, en paralelo.

#### Configuracíón

El módulo dispone de confguración específica en el archivo conf/hav.conf

ina3221_activo=1
tiempoMuestreoINA3221=10

donde,

- ina3221_activo: informa sobre el estado de activación del modulo, 0 o 1 en función de si se desea que este activo o no.
- tiempoMuestreoINA3221: informa sobre el tiempo de toma de datos del sensor.

### GSM

#### Introducción

Este módulo se basa en el chip sim900A. Este módulo permite el envio de mensajes SMS vía protocolo AT. Se utiliza como sistema de envio de datos redundante en caso de fallo del sistema primario basado en RF.

#### Descripción

El software que controla este modulo se ha simplificado al máximo para que simplemente se le pase a los métodos de envio un string con el SMS que se desea que se envien.

La interacción con el chip es mediante protocolo AT. El detalle de este protocolo y de todas las funcionalidades con este chip se puede encontrar aqui.

https://components101.com/wireless/sim900a-gsm-module

#### Conexión

El modulo se conecta a la raspberry por puerto série y se utiliza un adaptador CP2102 para adaptar el puerto serie a USB y poder conectarlo asi a uno de los slots USB de la raspberry.

#### Configuracíón

El módulo dispone de confguración específica en el archivo conf/hav.conf

gsm_activo=1
alturaActivacion=1
usbGSM=/dev/ttyUSB1
listaMoviles=+34666666666,+34699999999
pin=6666
tiempoTrazaGSM=45

donde,

- gsm_activo: informa sobre el estado de activación del modulo, 0 o 1 en función de si se desea que este activo o no.
- tiempoTrazaGSM: informa sobre el tiempo que transcurre entre el envio de datos por SMS
- alturaActivacion: Altura por debajo de la cual el modulo de GSM funciona. Este parametro tiene sentido porque por encima de 2 o 3 mil metros, la cobertura de GSM suele ser inexistente. De esta forma se ahorra bateria. Con el valor por defecto, 1, se consigue un efecto de deativación del modulo. Este parametro se ha de configurar adecuadamente antes del lanzamiento.
- usbGSM: corresponde al puerto USB al que esta conectado el adaptador cp2102 del componente de GSM. Es importante destacar que este puerto puede cambiar en función de los dispositivos conectados a la raspberry y el slot USB donde se conecten, con lo que se deberá comprobar manualmente que esta configuración es correcta.
- listaMoviles: lista de numeros de telefono movil a los cuales se enviará el SMS con la traza. Es importante que el numero tengo +34 (código pais españa) y sin ningún espacio.
- pin: código pin de la tarjeta SIM que utiliza el componente.

### Camara

#### Introducción

Este punto hace referencia explicitamente a la Pi cam, o la camara que puede conectarse directamente a la PI por CSI.

#### Descripción

El módulo de control de la camara requiere de una série de librerias de python para su operación denominadas **PIL** y **picamera**. Previamente hay que haber instalado estos módulos en pyton con PIP.

Ejecutar:

```
sudo pip install picamera
```

#### Configuración

El módulo dispone de confguración específica en el archivo conf/hav.conf

camara_activo=1
tiempoTomaImagen=30
tiempoExposicion=3
resolucionRFX=320
resolucionRFY=240
resolucionMaxX=1920
resolucionMaxY=1080
pathImagenesBase=/data/lirevenas/images/

donde,

- camara_activo: informa sobre si el módulo esta activo o no.
- tiempoTomaImagen: tiempo entre foto y foto.
- tiempoExposicion: tiempo de exposición del sensor cmos de la camara(equivalente al tiempo de apertura del diafragma de la camara)
- resolucionRFX: resolución mínima en el ejeX (anchura) de la foto que tomará la camara.
- resolucionRFY: resolución mínima en el ejeY (altura) de la foto que tomará la camara.
- resolucionMaxX: resolución máxima en el ejeX (anchura) de la foto que tomará la camara.
- resolucionMaxY: resolución máxima en el ejeY (altura) de la foto que tomará la camara.
- pathImagenesBase: path base en el filesystem del SO donde se ubicaran las fotos.

### Proceso Principal

#### Introducción

Como se ha comentado, todos los componentes vuelcan los datos que generan directamente a archivos de log para evitar interferir en los procesos de envio o de toma de datos de otros sensores.

Este módulo se encarga de, mediante una configuración previa, recuperar los archivos de log de los sensores que se deseen, procesarlos y dejarlos fusionados en una única traza de log que será la que utilicen los componentes de RF y GSM para enviarla.

#### Descripción

Todos los archivos de datos de los sensores tienen la forma siguiente:

timestamp|dato1|...|datoN|

el proceso recupera, en función de la lista de módulos sobre los que ha de iterar, la ultima traza de datos disponible.

Para cada una de esas trazas, coge todos los campos menos el primero, que es el timestamp, y lo concatena sobre una nueva traza que se acabará escribiendo en un archivo llamado sensores.log.

Es sobre este archivo sobre el que trabajaran los modulos de RF y GSM para poder enviar los datos que aqui hayan mediante sus respectivos protocolos.

#### Configuración

El módulo dispone de confguración específica en el archivo conf/hav.conf

tiempoMuestreo=15
configuracionTraza=gps,bmp,uv,ina3221

donde,

- tiempoMuestreo: corresponde al intervalo de tiempo en el que se realizará la acción se sintesis de archivos de datos para construir una linea del archivo de datos sensores.log
- configuracionTraza: corresponde a la lista de modulos de los cuales se intentará recuperar archivos de datos. El orden de los datos en el archivo sensores.log lo determina el orden de los módulos de esta lista.

### Servicio de Configuración

#### Introducción

El sistema de configuración es un módulo de soporte que se encarga de recuperar los datos de configuración del archivo de configuración que se le configure.

Ayuda a hacer mas mantenible el código y a una mejor parametrización del software.

#### Descripción

Se basa en una libreria interna de python denominada "configparser" que es capaz de leer configuraciones del tipo:

```
[nombre_seccion1]
param11=valor11
...
param1N=valor1N
....
[nombre_seccionM]
paramM1=valorM1
paramMZ=valorMX
```

Para cada nuevo parámetro que se dese añadir al archivo de configuración se ha de crear un método de lectura en este módulo.

## Configuraciones Genéricas

### Activación I2C en Raspbian

El bus I2C permite el mapeo de los componentes que estan conectados al mismo a través de una serie de registros de datos y control. Estos registros son específicos por cada componente, leyendo y escribiendo en estos registros de la forma indicada por cada fabricante es como se controlan.

Para poder activar el bus I2C en la Pi. Se han de seguir los pasos siguientes:

1. Ejecutar: 

```
sudo raspi-config
```

2. Navegar por las opciones siguientes [Interfacing Options -> I2C -> Activate]. Pasados unos segundos el I2C queda activado.

A modo de comprobación, se puede utilizar la herramienta i2c-detect, simplemente ejecutando "i2cdetect -y 1" en linea de comandos y donde se muestra los dispositivos que estan usando el mapa de registros del I2C

```
pi@raspberrypi:/data/lirevenas/hav $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- 38 39 -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

## Logging

### Introducción

El software desarrollado deja gran cantidad de logs en el filesystem. Es vital entender donde estan, de que tipo son y que información se puede recuperar de ellos.

El uso de logs es una ventaja ostensible para los procesos de desarrollo y mantenimiento ya que agilizan mucho la depuración de errores y permiten el "analisis forense" de lo que puede haber ocurrido en caso de fallo.

Todos los tipos de logs, exceptuando los del propio SO raspbian, estan basados en una libreria de python denominada "logging"

Esta libreria permite declarar "appenders" o configuraciones de escritura de logs sobre un archivo concreto y con una forma concreta.

Esto homogenealiza la escritura de los logs y permite una lectura mucho mas clara. 

Otro aspecto fundamental es la adción de un timestamp, que permite darle una relación temporal a todos los eventos que se suceden durante la ejecución del código.

Finalmente, la libreria permite configurar la severidad de las trazas. Esto es, configurar el momento en el que se desea que aparezcan las trazas de log en los archivos en función de la configuración.

La severidad esta predefinida en niveles:

- debug
- info
- warn
- error

### Tipos de log

[TODO]




