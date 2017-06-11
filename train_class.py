class UkTransportLiveTrainTimeSensor(UkTransportSensor):
    """Live train time sensor from UK transportapi.com."""
    ICON = 'mdi:train'

    def __init__(self, api_app_id, api_app_key, station_code, destination_name):
        """Construct a live bus time sensor."""
        self._station_code = station_code         # stick to the naming convention of transportAPI
        self._destination_name = destination_name
        self._next_train_time = None
        self._next_train_status = None

        sensor_name = 'Next train to {}'.format(destination_name)
        query_url =  'train/station/{}/live.json'.format(station_code)
        
        # also requires '&darwin=false&destination=WAT&train_status=passenger'

        UkTransportSensor.__init__(
            self, sensor_name, api_app_id, api_app_key, query_url
        )

    def update(self):
        """Get the latest live departure data for the specified stop."""
        params = {'darwin': 'false', 'destination': self._destination_name, 'train_status': 'passenger'}

        self._do_api_request(params)

        if self._data != {}:
            self._next_train_time = self._data['departures']['all'][0]['aimed_arrival_time']
            self._next_train_status = self._data['departures']['all'][0]['status']
