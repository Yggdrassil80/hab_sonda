
import RPi.GPIO as GPIO
import time

buzzerPin = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT, initial=GPIO.LOW)


class buzzer():

    def on():
        if ()
        GPIO.output(buzzerPin,GPIO.HIGH)
        print ("Buzzer ON - Emitiendo sonido...")
        time.sleep(2) # Delay in seconds
        

    def off():
        GPIO.output(buzzerPin,GPIO.LOW)
        print ("Buzzer OFF - No sound")
        time.sleep(1)


     #thresholdOp:GPS.0.lt.10000:buzzer.on