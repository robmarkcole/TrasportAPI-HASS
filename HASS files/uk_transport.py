"""Support for UK public transport data provided by transportapi.com.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.uk_transport/
"""
import logging
import re
from datetime import datetime, timedelta

import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

# Platform wide
CONF_API_APP_KEY = 'app_key'
CONF_API_APP_ID = 'app_id'
CONF_LIVE_TRAIN_TIME = 'live_train_time'

# Sensor specific
ATTRIBUTION = "Data provided by transportapi.com"
ATTR_STATION_CODE = 'station_code'
ATTR_CALLING_AT = 'calling_at'
ATTR_NEXT_TRAINS = 'next_trains'
ATTR_UPDATE_INTERVAL = 'update_interval'

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_APP_ID): cv.string,
    vol.Required(CONF_API_APP_KEY): cv.string,
    vol.Optional(CONF_LIVE_TRAIN_TIME): [{
        vol.Required(ATTR_STATION_CODE): cv.string,
        vol.Required(ATTR_CALLING_AT): cv.string,
        vol.Optional(ATTR_UPDATE_INTERVAL, default=timedelta(seconds=120)): (
        vol.All(cv.time_period, cv.positive_timedelta))}]
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Get the uk_transport sensor."""
    sensors = []
    for live_train_time in config.get(CONF_LIVE_TRAIN_TIME):
        station_code = live_train_time.get(ATTR_STATION_CODE)
        calling_at = live_train_time.get(ATTR_CALLING_AT)
        sensors.append(
            UkTransportLiveTrainTimeSensor(
                config.get(CONF_API_APP_ID),
                config.get(CONF_API_APP_KEY),
                station_code,
                calling_at,
                update_interval = live_train_time.get(ATTR_UPDATE_INTERVAL)))

    add_devices(sensors, True)


class UkTransportSensor(Entity):
    """
    Sensor that reads the UK transport web API.

    transportapi.com provides comprehensive transport data for UK train, tube
    and bus travel across the UK via simple JSON API. Subclasses of this
    base class can be used to access specific types of information.
    """

    TRANSPORT_API_URL_BASE = "https://transportapi.com/v3/uk/"
    ICON = 'mdi:train'

    def __init__(self, name, api_app_id, api_app_key, url):
        """Initialize the sensor."""
        self._data = {}
        self._api_app_id = api_app_id
        self._api_app_key = api_app_key
        self._url = self.TRANSPORT_API_URL_BASE + url
        self._name = name
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.ICON

    def _do_api_request(self, params):
        """Perform an API request."""
        request_params = dict({
            'app_id': self._api_app_id,
            'app_key': self._api_app_key,
        }, **params)

        try:
            response = requests.get(self._url, params=request_params)
            response.raise_for_status()
            self._data = response.json()
        except requests.RequestException as req_exc:
            _LOGGER.warning(
                'Invalid response from transportapi.com: %s', req_exc
            )

class UkTransportLiveTrainTimeSensor(UkTransportSensor):
    """Live train time sensor from UK transportapi.com."""
    ICON = 'mdi:train'

    def __init__(self, api_app_id, api_app_key, station_code, calling_at, update_interval):
        """Construct a live bus time sensor."""
        self._station_code = station_code         # stick to the naming convention of transportAPI
        self._calling_at = calling_at
        self._update_interval = update_interval

        sensor_name = 'Next train to {}'.format(calling_at)
        query_url =  'train/station/{}/live.json'.format(station_code)

        UkTransportSensor.__init__(
            self, sensor_name, api_app_id, api_app_key, query_url
        )

    def update(self):
        """Get the latest live departure data for the specified stop."""
        params = {'darwin': 'false',
                  'calling_at': self._calling_at,
                  'train_status': 'passenger'}

        self._do_api_request(params)
        self._next_trains = [] # Clear

        if self._data != {}:                   # If not empty
            if 'error' in self._data:          # if query returns an error
                self._state = self._data['Error from transportAPI']
            if self._data['departures']['all'] == []:    # if there are no departures
                self._state = 'No departures'
            else:
                for departure in self._data['departures']['all']:      # don't need a regex search as passing in destination to search
                    self._next_trains.append({
                        'origin_name': departure['origin_name'],
                        'destination_name': departure['destination_name'],
                        'status': departure['status'],
                        'scheduled': departure['aimed_departure_time'],
                        'estimated': departure['expected_departure_time'],
                        'platform': departure['platform'],
                        'operator_name': departure['operator_name'],
                        'update_interval':str(self._update_interval)
                        })

                self._state = min(map(
                    _delta_mins, [train['scheduled'] for train in self._next_trains]
            ))

    @property
    def device_state_attributes(self):
        """Return other details about the sensor state."""
        attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}  # {'attribution': 'Data provided by transportapi.com'}
        if self._next_trains:
            attrs[ATTR_NEXT_TRAINS] = self._next_trains # if there is data, append
        return attrs

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return "min"

def _delta_mins(hhmm_time_str):
    """Calculate time delta in minutes to a time in hh:mm format."""
    now = datetime.now()
    hhmm_time = datetime.strptime(hhmm_time_str, '%H:%M')

    hhmm_datetime = datetime(
        now.year, now.month, now.day,
        hour=hhmm_time.hour, minute=hhmm_time.minute
    )
    if hhmm_datetime < now:
        hhmm_datetime += timedelta(days=1)

    delta_mins = (hhmm_datetime - now).seconds // 60
    return delta_mins
