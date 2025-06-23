from machine import UART, Pin, PWM
import time, _thread

# Configuración de pines
# Sensor ultrasónico
trig = Pin(7, Pin.OUT)  # Pin para enviar el pulso
echo = Pin(8, Pin.IN)   # Pin para recibir el pulso

# Configuración del UART
modulo = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

# Configuración del buzzer
BUZZER_PIN = 22
buzzer = PWM(Pin(BUZZER_PIN, Pin.OUT))

# Configuración de los pines de los LEDs
blancos = Pin(6, Pin.OUT)  # LED blanco en GPIO 6
verdes = Pin(27, Pin.OUT)  # LED verde en GPIO 27
rojos = Pin(26, Pin.OUT)   # LED rojo en GPIO 26

# Configuración de motores (dos motores controlando ruedas)
motorA1 = Pin(18, Pin.OUT)  # Motor A1, dirección 1
motorA2 = Pin(19, Pin.OUT)  # Motor A2, dirección 2
motorB1 = Pin(20, Pin.OUT)  # Motor B1, dirección 1
motorB2 = Pin(21, Pin.OUT)  # Motor B2, dirección 2

# Funciones para el movimiento del robot
def adelante():
    rojos.value(0)
    motorA1.high()
    motorA2.low()
    motorB1.low()
    motorB2.high()

def atras():
    rojos.value(0)
    motorA1.low()
    motorA2.high()
    motorB1.high()
    motorB2.low()

def derecha():
    rojos.value(0)
    motorA1.low()
    motorA2.high()
    motorB1.low()
    motorB2.high()

def izquierda():
    rojos.value(0)
    motorA1.high()
    motorA2.low()
    motorB1.high()
    motorB2.low()
    
def esperando_orden():
    motorA1.low()
    motorA2.low()
    motorB1.low()
    motorB2.low()

def para():
    rojos.value(1)
    motorA1.low()
    motorA2.low()
    motorB1.low()
    motorB2.low()
    
def bocina():
    """Emite un sonido con el buzzer."""
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
    
def baliza():
    blancos.value(1)
    verdes.value(0)
    rojos.value(0) 
    bocina()
    verdes.value(1)
    blancos.value(0)
    rojos.value(0)
    bocina()
    rojos.value(1) 
    blancos.value(0)
    verdes.value(0)
    bocina()
    
def ultrasonido():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    while echo.value() == 0:
        pulse_start = time.ticks_us()
    while echo.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distancia = pulse_duration * 0.0343 / 2
    return distancia < 20
    
def autonomo():
   print("Modo autónomo activado.")
   while True:
        if ultrasonido():
            blancos.value(0)
            verdes.value(0)
            rojos.value(1)
            para()
            time.sleep(0.5)
            atras()
            verdes.value(1)
            time.sleep(0.5)
            derecha()
            blancos.value(1)
            time.sleep(0.3)
            blancos.value(0)
            verdes.value(0)
            rojos.value(1)
            para()
            time.sleep(0.5)
        else:
            blancos.value(1)
            verdes.value(0)
            rojos.value(0)
            adelante()
        if modulo.any():
            dato = modulo.read().decode('utf-8').strip()
            if dato == "E":
                para()
                print("Saliendo del modo autónomo.")
                break

luces = [
    (blancos, 0.5), (verdes, 0.5), (rojos, 0.5),
    (blancos, 0.25), (verdes, 0.25), (rojos, 0.25),
    (verdes, 0.5), (blancos, 0.5), (rojos, 0.5),
    (blancos, 0.5),(rojos, 0.25),(verdes, 0.25),
    (verdes, 0.5), (blancos, 0.5), (rojos, 0.5),
    (blancos, 0.5), (verdes, 0.5), (rojos, 0.5)
] 
# Diccionario de notas musicales con sus frecuencias
notas = {
    'Do': 261, 'Do*': 523, 'Re': 293, 'Re*': 587, 'Mi': 329, 'Mi*': 659,
    'Fa': 349, 'Fa*': 698, 'Sol': 392, 'Sol*': 784, 'La': 440, 'La*': 880,
    'Si': 493, 'Sib': 466, 'Silencio': 0
}

# Melodía de Mario Bros con duraciones
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



# Función para reproducir una nota
def reproducir_nota(nota, duracion):
    if nota in notas:
        frecuencia = notas[nota]
        if frecuencia == 0:  # Silencio
            buzzer.duty_u16(0)
            
        else:
            buzzer.freq(frecuencia)
            buzzer.duty_u16(10000)  # Ajusta el volumen
        time.sleep(duracion)
        buzzer.duty_u16(0)
        time.sleep(0.05)  # Pequeño espacio entre notas
    else:
        print(f'Nota "{nota}" no definida en el diccionario.')

# Función para reproducir la melodía completa
def reproducir_melodia1():
    for nota, duracion in melodia1:
        reproducir_nota(nota, duracion)
    time.sleep(1)  # Pausa al final de la melodía
# Melodía de Jingle Bells con duraciones
melodia2 = [
    ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.6), ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.6),
    ('Mi', 0.3), ('Sol', 0.3), ('Do', 0.3), ('Re', 0.3), ('Mi', 0.6),
    ('Fa', 0.3), ('Fa', 0.3), ('Fa', 0.3), ('Fa', 0.3), ('Fa', 0.3),
    ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.3), ('Mi', 0.3),
    ('Re', 0.3), ('Re', 0.3), ('Mi', 0.3), ('Re', 0.6), ('Sol', 0.6)
]

# Función para reproducir una nota con luces sincronizadas
def reproducir_nota_con_luces(nota, duracion):
    if nota in notas:
        frecuencia = notas[nota]
        blancos.value(1)
        verdes.value(0)
        rojos.value(0)
        if frecuencia == 0:
            buzzer.duty_u16(0)
        else:
            buzzer.freq(frecuencia)
            buzzer.duty_u16(10000)
            time.sleep(duracion / 3)
        blancos.value(0)
        verdes.value(1)
        time.sleep(duracion / 3)
        verdes.value(0)
        rojos.value(1)
        time.sleep(duracion / 3)
        buzzer.duty_u16(0)
        rojos.value(0)
        time.sleep(0.05)
    else:
        print(f'Nota "{nota}" no definida en el diccionario.')

# Función para reproducir la melodía completa
def reproducir_melodia2():
    for nota, duracion in melodia2:
        reproducir_nota_con_luces(nota, duracion)    
def controlar_luces():     
    for led, duracion in luces:
            led.on()
            time.sleep(duracion)
            led.off()  
# Función para enviar datos a través de UART
def enviar_datos(dato):
    modulo.write(dato + '\n')

# Función para recibir datos a través de UART
def recibir_datos():
    if modulo.any():
        dato = modulo.read().decode('utf-8').strip()
        return dato
    return None

# Función para reproducir melodía en un hilo separado
def hilo_melodia():
    
    print("Iniciando melodía en hilo separado.")
   
    reproducir_melodia1()
   
_thread.start_new_thread(hilo_melodia,())
controlar_luces()
# Bucle principal
while True:
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
             autonomo()
        elif datos == "F":
             enviar_datos('f')
             reproducir_melodia2()
        elif datos == "G":
             enviar_datos('g')
             adelante() 
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
    if ultrasonido() and datos == "G":
       detecta()



