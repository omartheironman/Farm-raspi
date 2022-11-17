# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import http
import uvicorn
import os
import signal
import time
from threading import Thread
from modules import actions, reader
import auth
from fastapi import Depends, FastAPI, Request
from prometheus_client import start_http_server
from fastapi.security import HTTPBasic


app = FastAPI()
security = HTTPBasic()



def loop_over_sensor_reading():
    thread = Thread(target=reader.get_sensor_reading)
    thread.start()

@app.get("/")
async def root():
    actions.turn_on_pump()
    return {"message": "Pump run for 3 seconds"}


## Request is not currently being used but it will be
@app.post("/pump", status_code=http.HTTPStatus.ACCEPTED)
async def pump(request: Request=Depends(auth.get_auth)):
    print("turn on pump")
    actions.turn_on_pump()
    return{}

@app.post("/light_on", status_code=http.HTTPStatus.ACCEPTED)
async def pump(request: Request=Depends(auth.get_auth)):
    print("turn on light")
    actions.turn_on_light()
    return{}

@app.post("/light_off", status_code=http.HTTPStatus.ACCEPTED)
async def pump(request: Request=Depends(auth.get_auth)):
    print("turn off light")
    actions.turn_off_light()
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
    ##GPIO.cleanup()
    os.kill(os.getpid(), signal.SIGUSR1)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)