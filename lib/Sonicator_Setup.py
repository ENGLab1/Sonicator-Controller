import pyfirmata
import pyfirmata.boards
import pyfirmata.util
import PyTime_master.GS_timing as timing
import json 
import time
import os, sys
from enum import Enum
from config import *
import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports
# initialized = False

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()

ESC_ASCII_VALUE = 0x1b
U_ASCII_VALUE = 0x55
D_ASCII_VALUE = 0x44
V_REF = 4.915


class Arduino_Sonicator():
        #com port 3 for hyb 24 for sp
    def __init__(self, data = None):
        ports = list(serial.tools.list_ports.comports())

        use_port = "placeholder"  
        for p in ports:
                print ( p )
                print (p.description)
                if "CP210" in p.description:
                    print( "This is the port", p.name)
                    use_port = p.name
                    break

        if "CP210" not in p.description:
                messagebox.showwarning("Cal Board Error", "Cal Board Error.")
                return
        
        self.run = True
        self.laststate=True

        self.board = pyfirmata.Arduino(use_port)
        

        self.ud_pin = self.board.get_pin('d:9:o') 
        self.inc_pin = self.board.get_pin('d:8:o')
        self.cs_pin = self.board.get_pin('d:7:o')
        self.wiper_pin = self.board.get_pin('a:0:i')
        self.switch_pin = self.board.get_pin('d:6:o')

        self.it = pyfirmata.util.Iterator(self.board)
        self.it.start()
        
        print("arduino init")


    def turn_sonicator_horn_on(self):
        self.switch_pin.write(1)
        return

    def turn_sonicator_horn_off(self):
        self.switch_pin.write(0)
        return

    def close_serial_port(self):
        self.board.sp.close()
    def sonicate(self):
        self.set_initial_voltage()
        self.set_ADC_value(value = INPUT_VOLTAGE_SETTING)
        for i in range(INPUT_CYCLE_REPS):
            self.turn_sonicator_horn_on()
            timing.delay(INPUT_TIME_ON_SECONDS*1000)
            self.turn_sonicator_horn_off()
            timing.delay(INPUT_TIME_OFF_SECONDS*1000)
        print("Sonication complete")
        self.turn_sonicator_horn_off()

    def set_initial_voltage(self):
        while self.wiper_pin.read() != 0.0:
            self.ud_pin.write(0)
            timing.delayMicroseconds(5)
            self.inc_pin.write(0)
            timing.delayMicroseconds(5)
            self.inc_pin.write(1)
            timing.delay(20)
        print(f"Initial voltage set to {self.wiper_pin.read()} V.")

    def set_ADC_value(self,value):
            while self.wiper_pin.read() < value/V_REF:
                    self.ud_pin.write(1)
                    timing.delayMicroseconds(5)
                    self.inc_pin.write(0)
                    timing.delayMicroseconds(5)
                    self.inc_pin.write(1)
                    timing.delay(50)
                    print(self.wiper_pin.read())
            print(f"Wiper ADC value: {self.wiper_pin.read()}")

    def test_ADC_value(self):
        while 1:
            print("Press U to move voltage up, D to move down, ESC to quit!")
            if getch() == chr(U_ASCII_VALUE):
                print("UP")
                timing.delay(10)
                self.ud_pin.write(1)
                timing.delayMicroseconds(5)
                self.inc_pin.write(0)
                timing.delayMicroseconds(5)
                self.inc_pin.write(1)
                print(self.wiper_pin.read())
            elif getch() == chr(D_ASCII_VALUE):
                print("DOWN")
                timing.delay(10)
                self.ud_pin.write(0)
                timing.delayMicroseconds(5)
                self.inc_pin.write(0)
                timing.delayMicroseconds(5)
                self.inc_pin.write(1)
                print(self.wiper_pin.read())
            elif getch() == chr(ESC_ASCII_VALUE):
                break