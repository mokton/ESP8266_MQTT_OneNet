import mqtt
from chipid import chipid
import register
import wifi

def main():
    wifi.do_connect()

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