# TrasportAPI-HASS
UK bus and train TransportAPI component. Place uk_transport.py in /custom_components/sensor

Requires developer account on http://www.transportapi.com/

Get the status of busses/trains on valid routes. Bus times require ATCO codes and a valid destination.
Train times require valid station codes e.g. Waterloo = WAT

The free tier of the transportAPI allows only 1000 requests daily (approx. 40 an hour). If you create 1 sensor, this will update every 90 seconds with no problems. 2 sensors can be updated every 3 mins, and 3 sensors every 5 minutes. 
You can change the sensor scan interval in config.yaml by adding e.g. scan_interval: 90 to the config file as per https://home-assistant.io/docs/configuration/platform_options/

An option is to use an automation to only update the sensor in the windows of time about your daily commute. E.g. if you catch the same train every day and that is your main concern, just update the sensor in the hour up to and about that train.

<img src="https://github.com/robmarkcole/TrasportAPI-HASS/blob/master/Usage.png" width="500" >
