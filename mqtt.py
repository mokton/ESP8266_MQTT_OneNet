from simple import MQTTClient
from machine import Pin, Timer
#import machine
import time
#import micropython
#import esp
import dht
import ujson as json
import urequests as requests
from chipid import chipid

class mqtt:
    def __init__(self, client_id='', username='', password=''):
        self.server = "183.230.40.39"
        self.client_id = client_id
        self.username = username
        self.password = password
        self.topic = (chipid() + '-sub').encode('ascii') if client_id == '' else (client_id + '-' + chipid() + '-sub').encode('ascii')
        self.mqttClient = MQTTClient(self.client_id, self.server,6002,self.username,self.password)
        self.dht11 = dht.DHT11(Pin(14))
        self.pid = 0 # publish count

    def isPin(self, pin = '-1'):
        if int(pin) in (0,1,2,3,4,5,12,13,14,15,16):
            return int(pin)
        else:
            return -1

    def pubData(self, t):
        self.dht11.measure()
        value = {'datastreams':[{"id":"temp","datapoints":[{"value":self.dht11.temperature()}]}, {"id":"humi","datapoints":[{"value":self.dht11.humidity()}]}]}
        jdata = json.dumps(value)
        jlen = len(jdata)
        bdata = bytearray(jlen+3)
        bdata[0] = 1 # publish data in type of json
        bdata[1] = int(jlen / 256) # data lenght
        bdata[2] = jlen % 256      # data lenght
        bdata[3:jlen+4] = jdata.encode('ascii') # json data
        #print(bdata)
        print('publish data', str(self.pid + 1))
        self.mqttClient.publish('$dp', bdata)
        self.pid += 1

    def sub_callback(self, topic, msg):
        print((topic,msg))
        cmd = msg.decode('ascii').split(" ")
        if len(cmd) == 3:
            if cmd[0] == 'pin' and self.isPin(cmd[1]) >= 0:
                value = Pin(int(cmd[1])).value()
                if cmd[2] == 'on':
                    value = 1
                elif cmd[2] == 'off':
                    value = 0
                elif cmd[2] == 'toggle':
                    value = 0 if value == 1 else 1
                
                pin = Pin(int(cmd[1]), Pin.OUT) #, value=(1 if cmd[2] == 'on' else 0))
                pin.value(value)
            else:
                print('Pin number outof range.')
        

    def connect(self):
        self.mqttClient.set_callback(self.sub_callback)
        self.mqttClient.connect()
        tim = Timer(-1)
        tim.init(period=30000, mode=Timer.PERIODIC, callback=self.pubData) #Timer.PERIODIC   Timer.ONE_SHOT
        self.mqttClient.subscribe(self.topic)
        print("Connected to %s, subscribed to %s topic." % (self.server, self.topic))
        try:
            while 1:
                #self.mqttClient.wait_msg()
                self.mqttClient.check_msg()
        finally:
            #self.mqttClient.unsubscribe(self.topic)
            self.mqttClient.disconnect()
            print('mqtt closed')
            tim.deinit()

    

