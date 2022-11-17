# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time

import RPi.GPIO as GPIO

## TO-DO Make pin dynamic in the call
## TO-DO Make pass parameter into actions such as time to keep light on and pump etc
def turn_on_pump():
    """A Function to turn pump on"""
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(16, GPIO.LOW)

def turn_off_light():
    """A Function to turn light off"""
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.LOW)

def turn_on_light():
    """A Function to turn lights on"""
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.HIGH)

