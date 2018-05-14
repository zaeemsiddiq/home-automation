import subprocess
import RPi.GPIO as GPIO
from flask import Flask
import dht11
import time
import datetime
import json
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/currentTemp', methods=['GET'])
def currentTemp(): 
    instance = dht11.DHT11(pin=4)
    result = instance.read()
    data = {}
    if result.is_valid():
       print("Last valid input: " + str(datetime.datetime.now()))
       print("Temperature: %d C" % result.temperature)
       print("Humidity: %d %%" % result.humidity)
       data['temperature'] = str(result.temperature)
       data['humidity'] = str(result.humidity)
    return json.dumps(data)

@app.route('/lights/status', methods=['GET'])
def lightStatus():
    indoorPin = 2
    outdoorPin = 3
    data = {}
    data['indoor'] = False if GPIO.input(indoorPin) == 1 else True
    data['outdoor'] = False if GPIO.input(outdoorPin) == 1 else True
    return json.dumps(data)

@app.route('/light/set')
def lightSet():
    light = request.args.get('light')
    turnOn = True if request.args.get('value') == 'true' else False
    data = {}
    if light == 'indoor':
        if turnOn:
            GPIO.setup(2, GPIO.OUT)
            GPIO.output(2, GPIO.LOW)
            data['success'] = True
        else:
            GPIO.output(2, GPIO.HIGH)
            data['success'] = True

    if light == 'outdoor':
        if turnOn:
            GPIO.setup(3, GPIO.OUT)
            GPIO.output(3, GPIO.LOW)
            data['success'] = True
        else:
            GPIO.output(3, GPIO.HIGH)
            data['success'] = True
    return json.dumps(data)



@app.route('/fan/status', methods=['GET'])
def fanStatus():
    fanPin = 14
    data = {}
    data['fan'] = False if GPIO.input(fanPin) == 1 else True
    return json.dumps(data)

@app.route('/fan/set')
def fanSet():
    fan = request.args.get('fan')
    turnOn = True if request.args.get('value') == 'true' else False
    data = {}
    if turnOn:
        GPIO.output(14, GPIO.LOW)
        data['success'] = True
    else:
        GPIO.output(14, GPIO.HIGH)
        data['success'] = True

    return json.dumps(data)

@app.route('/heater/status', methods=['GET'])
def heaterStatus():
    heaterPin = 15
    data = {}
    data['heater'] = False if GPIO.input(heaterPin) == 1 else True
    return json.dumps(data)

@app.route('/heater/set')
def heaterSet():
    turnOn = True if request.args.get('value') == 'true' else False
    data = {}
    if turnOn:
         print ('turning heater on now')
         GPIO.output(15, GPIO.LOW)
         data['success'] = True
    else:
         GPIO.output(15, GPIO.HIGH)
         data['success'] = True

    return json.dumps(data)

@app.route('/partyMode')
def partyMode():
    pinList = [2, 3]
    timer = 0
    SleepTimeL = 0.1
    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)
    data = {}
    #subprocess.call("omxplayer -o local dance.mp3", shell=True)
    while True:
       if timer == 50:
          GPIO.output(2, GPIO.HIGH)
          GPIO.output(3, GPIO.HIGH)
          break
       for i in pinList:
        GPIO.output(i, GPIO.HIGH)
        time.sleep(SleepTimeL);
        GPIO.output(i, GPIO.LOW)

        pinList.reverse()

        for i in pinList:
         GPIO.output(i, GPIO.HIGH)
         time.sleep(SleepTimeL);
         GPIO.output(i, GPIO.LOW)

        pinList.reverse()
        timer+=1
    data['success'] = True
    return json.dumps(data)

if __name__ == '__main__':
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(2, GPIO.IN)
    GPIO.setup(3, GPIO.IN)

    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, GPIO.HIGH)

    GPIO.setup(15, GPIO.OUT)
    GPIO.output(15, GPIO.HIGH)

    # read data using pin 14
    # instance = dht11.DHT11(pin=4)
    app.run(debug=True, port=80, host='0.0.0.0')
