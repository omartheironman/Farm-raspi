# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time

import board
import busio
from adafruit_seesaw.seesaw import Seesaw
from prometheus_client import Gauge, Summary


REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
TEMP_SENSOR = Gauge('temp_sensor', 'temperature sensed')
MOISTURE_SENSOR = Gauge('moisture_sensor', 'moisture sensed')


@REQUEST_TIME.time()
def get_sensor_reading():
    """Read Sensor Info"""
    # i2c_bus = board.I2C()
    # GPIO.setmode(GPIO.BCM)
    i2c_bus = busio.I2C(board.D3, board.D2) ## The signal pins for the capactive sensor

    ss = Seesaw(i2c_bus, addr=0x36)
    try:
        while True:
            # read moisture level through capacitive touch pad
            touch = ss.moisture_read()

            # read temperature from the temperature sensor
            temp = ss.get_temp()
            print("temp: " + str(temp) + "  moisture: " + str(touch))
            MOISTURE_SENSOR.set(str(temp))
            TEMP_SENSOR.set(str(touch))
            time.sleep(1)
        # GPIO.output(37, False)
    except KeyboardInterrupt:  # If user pressed ctrl+c while loop was still running, then this will be useful
        pass
