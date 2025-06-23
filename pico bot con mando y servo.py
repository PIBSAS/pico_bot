from machine import UART, Pin, PWM
import time, _thread

# Sensor ultrasónico
trig = Pin(7, Pin.OUT)
echo = Pin(8, Pin.IN)

# UART
modulo = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

# Buzzer
BUZZER_PIN = 22
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty_u16(0)

# LEDs
blancos = Pin(6, Pin.OUT)
verdes = Pin(27, Pin.OUT)
rojos = Pin(26, Pin.OUT)

# Motores
motorA1 = Pin(18, Pin.OUT)
motorA2 = Pin(19, Pin.OUT)
motorB1 = Pin(20, Pin.OUT)
motorB2 = Pin(21, Pin.OUT)

# Servo
servo = PWM(Pin(0))
servo.freq(50)

# ---------------- FUNCIONES DE MOVIMIENTO ----------------
def mover_servo(angulo):
    min_pulse = 500
    max_pulse = 2500
    pulse_width = min_pulse + (angulo / 180) * (max_pulse - min_pulse)
    duty = int(pulse_width * 65535 / 20000)
    servo.duty_u16(duty)
    time.sleep(0.3)

def adelante():
    rojos.value(0)
    motorA1.low()
    motorA2.high()
    motorB1.high()
    motorB2.low()

def atras():
    rojos.value(0)
    motorA1.high()
    motorA2.low()
    motorB1.low()
    motorB2.high()

def derecha():
    rojos.value(0)
    motorA1.high()
    motorA2.low()
    motorB1.high()
    motorB2.low()

def izquierda():
    rojos.value(0)
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
    rojos.value(1)
    esperando_orden()

def bocina():
    buzzer.freq(500)
    buzzer.duty_u16(10000)
    time.sleep(0.5)
    buzzer.duty_u16(0)

def detecta():
    para()
    time.sleep(1)
    bocina()
    blancos.value(1)
    time.sleep(1)
    enviar_datos('l')
    blancos.value(0)
    rojos.value(0)
    buzzer.duty_u16(0)
    time.sleep(1)
    rojos.value(0)

# ---------------- DETECCIÓN DE OBSTÁCULOS ----------------
def medir_distancia():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()

    tiempo_inicio = time.ticks_us()
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), tiempo_inicio) > 30000:
            return 100
    pulse_start = time.ticks_us()

    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), pulse_start) > 30000:
            return 100
    pulse_end = time.ticks_us()

    duracion = time.ticks_diff(pulse_end, pulse_start)
    distancia = duracion * 0.0343 / 2
    return distancia

def autonomo():
    print("Modo autónomo activado.")
    while True:
        mover_servo(90)
        distancia_centro = medir_distancia()

        if distancia_centro < 25:
            para()
            time.sleep(0.5)

            mover_servo(150)
            distancia_izquierda = medir_distancia()

            mover_servo(30)
            distancia_derecha = medir_distancia()

            mover_servo(90)

            if distancia_derecha > distancia_izquierda:
                atras()
                time.sleep(0.7)
                derecha()
                time.sleep(0.7)
            else:
                atras()
                time.sleep(0.7)
                izquierda()
                time.sleep(0.7)
            para()
        else:
            adelante()

        if modulo.any():
            dato = modulo.read().decode('utf-8').strip()
            if dato == "E":
                para()
                print("Saliendo del modo autónomo.")
                break

# ---------------- LUCES Y BALIZA ----------------
luces = [
    (blancos, 0.5), (verdes, 0.5), (rojos, 0.5),
    (blancos, 0.25), (verdes, 0.25), (rojos, 0.25),
    (verdes, 0.5), (blancos, 0.5), (rojos, 0.5),
    (blancos, 0.5), (rojos, 0.25), (verdes, 0.25),
    (verdes, 0.5), (blancos, 0.5), (rojos, 0.5),
    (blancos, 0.5), (verdes, 0.5), (rojos, 0.5)
]

def baliza():
    blancos.value(1); verdes.value(0); rojos.value(0); bocina()
    blancos.value(0); verdes.value(1); rojos.value(0); bocina()
    blancos.value(0); verdes.value(0); rojos.value(1); bocina()

def controlar_luces():
    for led, duracion in luces:
        led.on()
        time.sleep(duracion)
        led.off()

# ---------------- MELODÍAS ----------------
notas = {
    'Do': 261, 'Do*': 523, 'Re': 293, 'Re*': 587, 'Mi': 329, 'Mi*': 659,
    'Fa': 349, 'Fa*': 698, 'Sol': 392, 'Sol*': 784, 'La': 440, 'La*': 880,
    'Si': 493, 'Sib': 466, 'Silencio': 0
}

melodia1 = [
    ('Mi*', 0.15), ('Mi*', 0.15), ('Silencio', 0.1), ('Mi*', 0.15),
    ('Silencio', 0.1), ('Do*', 0.15), ('Mi*', 0.15), ('Sol*', 0.3),
    ('Silencio', 0.3), ('Sol', 0.3), ('Silencio', 0.3),
    ('Do*', 0.15), ('Silencio', 0.1), ('Sol', 0.15), ('Mi', 0.15),
    ('La', 0.15), ('Si', 0.15), ('Sib', 0.15), ('La', 0.15),
    ('Sol*', 0.15), ('Mi*', 0.15), ('Sol*', 0.15), ('La*', 0.3),
    ('Fa*', 0.15), ('Sol*', 0.15), ('Mi*', 0.15), ('Do*', 0.15),
    ('Re', 0.15), ('Si', 0.15)
]

melodia2 = [
    ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.6), ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.6),
    ('Mi', 0.3), ('Sol', 0.3), ('Do', 0.3), ('Re', 0.3), ('Mi', 0.6),
    ('Fa', 0.3), ('Fa', 0.3), ('Fa', 0.3), ('Fa', 0.3), ('Fa', 0.3),
    ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.3),
    ('Re', 0.3), ('Re', 0.3), ('Mi', 0.3), ('Re', 0.6), ('Sol', 0.6)
]

def reproducir_nota(nota, duracion):
    frecuencia = notas.get(nota, 0)
    if frecuencia == 0:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(frecuencia)
        buzzer.duty_u16(10000)
    time.sleep(duracion)
    buzzer.duty_u16(0)
    time.sleep(0.05)

def reproducir_melodia1():
    for nota, duracion in melodia1:
        reproducir_nota(nota, duracion)

def reproducir_melodia2():
    for nota, duracion in melodia2:
        reproducir_nota(nota, duracion)

# ---------------- UART ----------------
def enviar_datos(dato):
    modulo.write(dato + '\n')

def recibir_datos():
    if modulo.any():
        return modulo.read().decode('utf-8').strip()
    return None

def hilo_melodia():
    reproducir_melodia1()

# ---------------- EJECUCIÓN PRINCIPAL ----------------
_thread.start_new_thread(hilo_melodia, ())
controlar_luces()

modo_autonomo = False

while True:
    if not modo_autonomo:
        datos = recibir_datos()
        if datos:
            print(f"Caracter Recibido: {datos}")
            if datos == "A":
                enviar_datos('a')
                blancos.toggle()
            elif datos == "B":
                enviar_datos('b')
                verdes.toggle()
            elif datos == "C":
                enviar_datos('c')
                rojos.toggle()
            elif datos == "D":
                enviar_datos('d')
                bocina()
            elif datos == "E":
                enviar_datos('e')
                modo_autonomo = True
                autonomo()
                modo_autonomo = False
            elif datos == "F":
                enviar_datos('f')
                reproducir_melodia2()
            elif datos == "G":
                enviar_datos('g')
                adelante()
                if medir_distancia() < 25:
                    detecta()
            elif datos == "H":
                enviar_datos('h')
                atras()
            elif datos == "I":
                enviar_datos('i')
                izquierda()
            elif datos == "J":
                enviar_datos('j')
                derecha()
            elif datos == "K":
                enviar_datos('k')
                esperando_orden()
            elif datos == "LL":
                enviar_datos('ll')
                baliza()
