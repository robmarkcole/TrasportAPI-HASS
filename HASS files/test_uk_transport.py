"""The tests for the uk_transport platform."""
import re
from datetime import timedelta

import requests_mock

from homeassistant.components.sensor import uk_transport
from homeassistant.components.sensor.uk_transport import (
    UkTransportSensor,
    ATTR_ATCOCODE, ATTR_LOCALITY, ATTR_STOP_NAME, ATTR_NEXT_BUSES,
    CONF_API_APP_KEY, CONF_API_APP_ID, CONF_LIVE_BUS_TIME,
    CONF_STOP_ATCOCODE, CONF_BUS_DIRECTION, SCAN_INTERVAL)
from homeassistant.setup import setup_component
from tests.common import load_fixture, get_test_home_assistant


class TestUkTransportLiveBusSensor:
    """Test the uk_transport platform."""

    TEST_DIRECTION = 'Wantage'
    TEST_ATCOCODE = '340000368SHE'

    def add_entities(self, new_entities, update_before_add=False):
        """Mock add entities."""
        if update_before_add:
            for entity in new_entities:
                entity.update()

        for entity in new_entities:
            self.entities.append(entity)

    @classmethod
    def setup_class(cls):
        """Initialize values for this testcase class."""
        cls.hass = get_test_home_assistant()
        cls.config = {
            CONF_API_APP_ID: 'foo',
            CONF_API_APP_KEY: 'ebcd1234',
            SCAN_INTERVAL: timedelta(seconds=120),
            CONF_LIVE_BUS_TIME: [{
                CONF_STOP_ATCOCODE: cls.TEST_ATCOCODE,
                CONF_BUS_DIRECTION: cls.TEST_DIRECTION}],
        }
        cls.entities = []

    @classmethod
    def teardown_class(cls):  # pylint: disable=invalid-name
        """Stop everything that was started."""
        cls.hass.stop()

    def test_setup_with_config(self):
        """Test the platform setup with configuration."""
        assert setup_component(
            self.hass, 'sensor', {'uk_transport': self.config}
        ) is True

    def test_setup(self):
        """Test for operational uk_transport sensor with proper attributes."""
        with requests_mock.Mocker() as mock_req:
            uri = re.compile(UkTransportSensor.TRANSPORT_API_URL_BASE + '*')
            mock_req.get(uri, text=load_fixture('uk_transport.json'))
            uk_transport.setup_platform(
                self.hass, self.config, self.add_entities
            )
        assert len(self.entities) ==  1
        sensor = self.entities[0]

        assert sensor.name == 'Next bus to {}'.format(self.TEST_DIRECTION)
        assert type(sensor.state) == int
        assert sensor.icon == 'mdi:bus'
        assert sensor.unit_of_measurement == 'min'

        attrs = sensor.device_state_attributes
        assert attrs[ATTR_ATCOCODE] == self.TEST_ATCOCODE
        assert attrs[ATTR_LOCALITY] == 'Harwell Campus'
        assert attrs[ATTR_STOP_NAME] == 'Bus Station'
        assert len(attrs[ATTR_NEXT_BUSES]) == 2

        direction_re = re.compile(self.TEST_DIRECTION)
        for bus in attrs[ATTR_NEXT_BUSES]:
            print (bus['direction'], direction_re.match(bus['direction']))
            assert direction_re.search(bus['direction']) is not None

    def test_request_error(self, caplog):
        uri = re.compile(UkTransportSensor.TRANSPORT_API_URL_BASE + '*')
        with requests_mock.Mocker() as mock_req:
            mock_req.get(uri, status_code=400)
            uk_transport.setup_platform(
                self.hass, self.config, self.add_entities
            )
        assert 'Invalid response from transportapi.com' in caplog.text
