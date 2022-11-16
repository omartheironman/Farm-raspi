# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import http
import uvicorn
import os
import signal
import time
from threading import Thread

import board
import busio
import RPi.GPIO as GPIO
import auth
from adafruit_seesaw.seesaw import Seesaw
from fastapi import Depends, FastAPI, Request
from prometheus_client import Gauge, Summary, start_http_server



REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
TEMP_SENSOR = Gauge('temp_sensor', 'temperature sensed')
MOISTURE_SENSOR = Gauge('moisture_sensor', 'moisture sensed')


app = FastAPI()



@REQUEST_TIME.time()
def get_sensor_reading():
    """Read Sensor Info"""
    # i2c_bus = board.I2C()
    # GPIO.setmode(GPIO.BCM)
    i2c_bus = busio.I2C(board.D3, board.D2)

    ss = Seesaw(i2c_bus, addr=0x36)
    try:
        while True:
            # read moisture level through capacitive touch pad
            touch = ss.moisture_read()

            # read temperature from the temperature sensor
            temp = ss.get_temp()
            print("temp: " + str(temp) + "  moisture: " + str(touch))

            #Export Metrics to prometheus
            MOISTURE_SENSOR.set(str(temp))
            TEMP_SENSOR.set(str(touch))
            time.sleep(1)
        # GPIO.output(37, False)
    except KeyboardInterrupt:  # If user pressed ctrl+c while loop was still running, then this will be useful
        pass

def turn_on_pump():
    """ This function will turn on water pump for a second"""
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(16, GPIO.LOW)

def loop_over_sensor_reading():
    thread = Thread(target=get_sensor_reading)
    thread.start()

@app.post("/pump", status_code=http.HTTPStatus.ACCEPTED)
async def pump(request: Request=Depends(auth.get_auth)):
    turn_on_pump()
    return{}



@app.on_event("startup")
async def startup_event():
    # Start up the server to expose the metrics.
    start_http_server(9100)
    # Generate some requests.
    loop_over_sensor_reading()


@app.on_event("shutdown")
def shutdown_event():
    print("shutting down in 5 seconds...")
    time.sleep(5)
    os.kill(os.getpid(), signal.SIGUSR1)




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)