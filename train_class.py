# As per bus but route becomes origin_name, direction becomes destination_name, next_suses becomes next_trains

class UkTransportLiveTrainTimeSensor(UkTransportSensor):
    """Live train time sensor from UK transportapi.com."""
    ICON = 'mdi:train'

    def __init__(self, api_app_id, api_app_key, station_code, destination_name):
        """Construct a live bus time sensor."""
        self._station_code = station_code         # stick to the naming convention of transportAPI
        self._destination_name = destination_name
        self._next_trains = {}
        self._destination_re = re.compile(
            '{}'.format(destination_name), re.IGNORECASE
        )

        sensor_name = 'Next train to {}'.format(destination_name)
        query_url =  'train/station/{}/live.json'.format(station_code)

        print(query_url)
        # also requires '&darwin=false&destination=WAT&train_status=passenger'

        UkTransportSensor.__init__(
            self, sensor_name, api_app_id, api_app_key, query_url
        )

    def update(self):
        """Get the latest live departure data for the specified stop."""
        params = {'darwin': 'false', 'destination': self._destination_name, 'train_status': 'passenger'}

        self._do_api_request(params)

        if self._data != {}:
            self._next_trains = []

            for departure in self._data['departures']['all']:      # don't need a regex search as passing in destination to search
                #print_json(departure)   # uncomment to see all fields
                self._next_trains.append({
                    'origin_name': departure['origin_name'],
                    'destination_name': departure['destination_name'],
                    'status': departure['status'],
                    'scheduled': departure['aimed_departure_time'],
                    'estimated': departure['expected_departure_time'],
                    'platform': departure['platform'],
                    'operator_name': departure['operator_name']
                    })

            self._state = min(map(
                _delta_mins, [train['scheduled'] for train in self._next_trains]
            ))

    @property
    def device_state_attributes(self):
        """Return other details about the sensor state."""
        if self._data is not None:
            attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}  # {'attribution': 'Data provided by transportapi.com'}
            for key in [
                    ATTR_ATCOCODE, ATTR_LOCALITY, ATTR_STOP_NAME,
                    ATTR_REQUEST_TIME
            ]:
                attrs[key] = self._data.get(key)           # place these attributes
            attrs[ATTR_NEXT_BUSES] = self._next_buses      # not in
            print_json(attrs)
            return attrs

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return "min" 
