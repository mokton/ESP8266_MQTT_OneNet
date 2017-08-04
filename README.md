# ESP8266 MQTT OneNet
Esp8266 Connect Onenet via mqtt, subscribe & publish

## Usage:
#### Code Config:
[main.py](https://github.com/mokton/ESP8266_MQTT_OneNet/blob/master/main.py)
```python
product_id = 'YourProductID'
#Change to your product id number as a string
regKey = 'YourEvnRegistKey' 
#Change to your environment key
```
[wifi.py](https://github.com/mokton/ESP8266_MQTT_OneNet/blob/master/wifi.py)
```python
sta_if.connect('SSID', 'PASSOWRD')
#Change to your wifi SSID and PASSWORD
```
#### MQTT Command:
Command format by 'pin n state'.
 - pin as string 'pin'
 - n is pin number, enum by 0,1,2,3,4,5,12,13,14,15,16
 - state is 'on','off' or 'toggle'

## Board:
![image](https://raw.githubusercontent.com/mokton/ESP8266_MQTT_OneNet/master/esp_ht_board.png)

## TODO:
1. auto reconnect
2. web config or smartlink
