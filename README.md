# TrasportAPI-HASS
UK bus and train TransportAPI component. Place uk_transport.py in /custom_components/sensor

Requires developer account on http://www.transportapi.com/

Get the status of busses/trains on valid routes. Bus times require ATCO codes and a valid destination.
Train times require valid station codes e.g. Waterloo = WAT

The free tier of the transportAPI allows only 1000 requests daily (approx. 40 an hour). If you create 1 sensor, this will update every 87 seconds with no problems. 2 sensors can be updated every 2*87 = 174 seconds, etc. 

<img src="https://github.com/robmarkcole/TrasportAPI-HASS/blob/master/Usage.png" width="500" >
