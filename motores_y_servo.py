from machine import Pin, PWM
import time

# Configura el pin, por ejemplo, el GPIO 2
blancos = Pin(6, Pin.OUT)
# Configuración de motores (dos motores controlando ruedas)
motorA1 = Pin(18, Pin.OUT)  # Motor A1, dirección 1
motorA2 = Pin(19, Pin.OUT)  # Motor A2, dirección 2
motorB1 = Pin(20, Pin.OUT)  # Motor B1, dirección 1
motorB2 = Pin(21, Pin.OUT)  # Motor B2, dirección 2

servo = PWM(Pin(1))
servo.freq(50)


def mover_servo(angulo):
    min_pulse = 500
    max_pulse = 2500
    pulse_width = min_pulse + (angulo / 180) * (max_pulse - min_pulse)
    duty = int(pulse_width * 65535 / 20000)
    servo.duty_u16(duty)
    time.sleep(0.3)


def adelante():
    motorA1.low()
    motorA2.high()
    motorB1.high()
    motorB2.low()


def atras():
    motorA1.high()
    motorA2.low()
    motorB1.low()
    motorB2.high()


def derecha():
    motorA1.high()
    motorA2.low()
    motorB1.high()
    motorB2.low()


def izquierda(): 
    motorA1.low()
    motorA2.high()
    motorB1.low()
    motorB2.high()


def esperando_orden():
    motorA1.low()
    motorA2.low()
    motorB1.low()
    motorB2.low()


def para(): 
    motorA1.low()
    motorA2.low()
    motorB1.low()
    motorB2.low()

# Bucle infinito
while True:
    mover_servo(180)
    time.sleep(1)
    mover_servo(90)
    time.sleep(1)
    adelante()  # Encender
    time.sleep(1)     # Esperar 1 segundo
    para() # Apagar
    time.sleep(1)     # Esperar 1 segundo
    atras()
    time.sleep(1)
