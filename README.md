# TrasportAPI-HASS
UK bus and train TransportAPI component. Place uk_transport.py in /custom_components/sensor

Requires developer account on http://www.transportapi.com/

Get the status of busses/trains on valid routes. Bus times require ATCO codes and a valid destination.
Train times require valid station codes e.g. Waterloo = WAT

1000/(60 x 24) = 0.69 therefore 1 sensor updating every minute will run into trouble at about 5pm daily. You can calc the max refresh rate for n sensors from rate_mins = 1000/(24 x n) e.g. 3 sensors can update every 1000/(24*3) =~ 14 minutes.
You can change the scan interval by adding e.g. scan_interval: 90 to the config file as per https://home-assistant.io/docs/configuration/platform_options/

An option is to use an automation to only update the sensor in the windows of time about your daily commute. E.g. if you catch the same train every day and that is your main concern, just update the sensor in the hour up to and about that train.

<img src="https://github.com/robmarkcole/TrasportAPI-HASS/blob/master/Usage.png" width="500" >
