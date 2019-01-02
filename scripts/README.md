# TransportAPI-HASS scripts

Here are a couple of scripts which make use of the transport information provided by the home assistant component (https://www.home-assistant.io/components/sensor.uk_transport/)

* train_state.py
  * Monitors one train
  * Notifies on status change
  * Changes a light colour based on train status 
* train_monitor.py
  * Monitors multiple train times
  * Monitors both directions of your commute
  * Notifies schedule changes along with platform numbers
  * Has the ability to work with a light (untested)