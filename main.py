import mqtt
from chipid import chipid
from machine import Timer
import register
import wifi

def checkWifi(t):
    wifi.do_connect(False)

def main():
    wifi.do_connect(True)
    netTim = Timer(1)
    netTim.init(period=60000, mode=Timer.PERIODIC, callback=checkWifi)

    sn = 'ESP' + chipid()
    title = 'Device' + sn
    product_id = 'YourProductID'
    regKey = 'YourEvnRegistKey'
    url = 'http://api.heclouds.com/register_de?register_code=' + regKey
    reg = register.Register(url=url, title=title, sn=sn)
    if reg.regist()==0:
        mq = mqtt.mqtt(client_id=reg.device_id, username=product_id, password=reg.key)
        mq.connect()
    else:
        print('Error: No Client ID!')
    
main()
