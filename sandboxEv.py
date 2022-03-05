import sys
import time
import ctypes
import random

user = ctypes.windll.user32
kernel = ctypes.windll.kernel32

teclasPulsadas = 0
clicksMouse = 0
clicksDobles = 0

class LASTINPUT(ctypes.Structure):
    fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

def get_ultimoInput():
    structUltimoInput = LASTINPUT()
    structUltimoInput.cbSize = ctypes.sizeof(LASTINPUT)

     # Obtener el ultimo input que se registro
    user.GetlastInputInfo(ctypes.byref(structUltimoInput))

     # Tiempo activo del objetivo
    runtime = kernel.GetTickCount()

    elapsed = runtime - structUltimoInput.dwTime

     # Print del debugger para ver que todo esta bien
    print(elapsed)

    return elapsed

 # Funcion para detectar las teclas pulsadas
def obtenerTecla():
    global clicksMouse
    global teclasPulsadas

    for keys in range(0, 0xff):
        if user.GetAsyncKeyState(keys) == -32767:

            if keys == 0x1:
                clicksMouse += 1
                return time.time()
            elif keys >= 32 and keys < 127:
                teclasPulsadas += 1
    return None

def detectSandbox():
    global clicksMouse
    global teclasPulsadas
    global tiempoPresionada

    maxteclasPulsadas = random.randint(10, 25)
    maxclicksMouse = random.randint(5, 25)

    clicksDobles = 0
    maxclicksDobles = 10

    dobleClickSos = 0.250  # Esto es en segundos
    primerDClick = None

    average_mousetime = 0
    maxInputs = 30000  # Milisegundos

    teclaAnterior = None
    deteccion = False

    ultimoInput = get_ultimoInput()

    if ultimoInput >= maxInputs:
        while not deteccion:
            teclasPressTiempo = obtenerTecla()
            if teclasPressTiempo is not None and teclaAnterior is not None:
                #se calcula cuanto timpo hay entre los doble clicks
                elapsed = teclasPressTiempo - teclaAnterior
                #los clicks dobles 
                if elapsed <= dobleClickSos:
                    clicksDobles += 1
                    if primerDClick is None:
                        primerDClick = time.time()
                    else:
                        #ve si todo se comprueba si no deja de ejecutarse 
                        if clicksDobles == maxclicksDobles:
                            sys.exit(0)
                    return
        teclaAnterior = tiempoPresionada
    elif tiempoPresionada is not None:
        teclaAnterior = tiempoPresionada
 
detectSandbox()
 # Print del debugger
print ("Todo funciono bien")
