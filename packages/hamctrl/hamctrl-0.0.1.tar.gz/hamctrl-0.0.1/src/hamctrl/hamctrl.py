'''
Author: Marcel Miljak
Klasse: 5aHEL - HTL Anichstraße
Diplomarbeit: Entwicklung eines Hamster Roboters
Jahrgang: 2021/22
'''

import time  
from time import sleep
import RPi.GPIO as GPIO

DIR_2 = 18           # Direction-Pin vom 2ten Modul
DIR_1 = 24           # Direction-pin vom 1sten Modul
STEP_1 = 25          # Step-Pin vom 1sten Modul
STEP_2 = 23          # Step-Pin vom 2ten Modul

CW = 1               # Clockwise Rotation
CCW = 0              # Counterclockwise Rotation

SENS_TRIG = 6        # Trigger-Pin HC-SR04
SENS_ECHO = 5        # Echo-Pin HC-SR04

whole_cycle = 300     # ganze Umdrehung (360 / 7.5) was aber foisch is
cycle_left = 548      # Viertel Umdrehung
delay = 0.005

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR_2, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)
    GPIO.setup(STEP_2, GPIO.OUT)
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(SENS_TRIG, GPIO.OUT)
    GPIO.setup(SENS_ECHO, GPIO.IN)


def vor():
    '''
    lässt den Hamster eine ganze Motor-Umdrehung
    nach vorne fahren (360°)
    '''
    setup()
    GPIO.output(DIR_1, CW)
    GPIO.output(DIR_2, CW)
    print("Vorwärts...")
    for i in range(3):
        dist = vornFrei()
        if dist < 20.0:
            print("Achtung - Hinderniss voraus!")
            stop()
            time.sleep(delay)
            linksUm()
            time.sleep(delay)
            break  
        else:
            for i in range (100):
                GPIO.output(STEP_1, GPIO.HIGH)
                GPIO.output(STEP_2, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP_1, GPIO.LOW)
                GPIO.output(STEP_2, GPIO.LOW)
                sleep(delay)


def linksUm():
    '''
    Dreht sich um 90° nach links
    '''
    setup()
    GPIO.output(DIR_1, CW)
    GPIO.output(DIR_2, CCW)
    print("Ausrichtung nach links...")
    for i in range(298):
        GPIO.output(STEP_1, GPIO.HIGH)
        GPIO.output(STEP_2, GPIO.LOW)
        sleep(delay)
        GPIO.output(STEP_1, GPIO.LOW)
        GPIO.output(STEP_2, GPIO.HIGH)
        sleep(delay)


def rechtsUm():
    '''
    Nur als Test angesehen, ob Hamster auch wirklich nach
    rechts ausrichtet
    '''
    setup()
    print("Ausrichtung nach rechts...")
    linksUm()
    linksUm()
    linksUm()
    GPIO.cleanup()


def vornFrei():
    '''
    liefert true, wenn sich keine Mauer vor dem Hamster
    befindet.
    Kommt gemeinsam mit Obstacle-Avoidance-Sensor in 
    Einsatz.
    '''
    setup()
    
    GPIO.output(SENS_TRIG,1)
    time.sleep(0.00001)
    GPIO.output(SENS_TRIG,0)
    
    
    while GPIO.input(SENS_ECHO) == 0:
        pass
    start = time.time()
    
    timer = 0
    while (GPIO.input(SENS_ECHO) == 1 and timer <= 12):
        timer +=1
        time.sleep(0.0001)
    stop = time.time()
    
    return (stop-start) * 34300 / 2


def stop():
    '''
    Wenn sich eine Mauer vor dem Hamster befindet,
    soll diese Funktion die Motoren stoppen. 
    '''
    setup()
    print("Stop des Hamsters...")
    GPIO.output(DIR_1, GPIO.LOW)
    GPIO.output(DIR_2, GPIO.LOW)
    GPIO.output(STEP_1, GPIO.LOW)
    GPIO.output(STEP_2, GPIO.LOW)
  
''' 
def kornDa():
    
    liefert true, wenn sich auf dem Feld, auf der der 
    Hamster steht, sich mindestens ein Korn befindet.
    
    setup()
    print("Check ob Korn auf Feld vorhanden...")
    korn_indicator = GPIO.input(SENS_Korn)
    if korn_indicator == 0:
        print("Es befindet sich ein Korn auf dem Feld")
        return True
    else:
        return False 
'''

def nimm():
    '''
    nimmt von dem Feld, auf dem er gerade steht, ein Korn auf
    '''
    pass


def gib():
    '''
    lege auf dem Feld, auf dem er gerade steht, ein Korn
    aus seinem Maul ab.
    '''
    pass


def maulLeer():
    '''
    liefert true, wenn der Hamster keinen Körner
    im Maul hat.
    '''
    pass