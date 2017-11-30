"""
Script to receive alerts for trains of interest.
"""
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import time

# Use hooks into home assistant? Useful for when testing
HASS = 0

# Set config
SOURCE_SENSOR_PREFIX = 'sensor.next_train_to_'
TRAIN_SENSOR_PREFIX = 'sensor.train_'
# Commute stations and times, codes from
TIMES = {'VIC' : ['07:34', '07:49'],
         'HHE' : ['18:30', '18:44', '19:00']}
# Set notification details
MSG_TITLE = 'Train Status Update'
NOTIFY_ID = 'tris'
LAMP_ID = ''



def processTrain(train, times):

    # We won't notify unless the state has changed
    NOTIFY = 0
    # If we are monitoring more than one train we need to sequence the light, this will occur until the trains are no longer scheduled
    if len(times) > 1:
        # Set the lamp to blue for 1 second, National rail has blue in the logo... so this is why I used blue
        if HASS and bool(LAMP_ID):
            hass.services.call('light', 'turn_on', {
                "entity_id": LAMP_ID,
                'color_name': 'blue'})
            time.sleep(1)

    logger.info('Found the ' + train['scheduled'])
    # If the status has changed compared to what's in HASS update it and then notify
    if HASS and hass.states.get(TRAIN_SENSOR_PREFIX + train['scheduled']).state != train['status']:
        #Set the state in HASS
        hass.states.set(DEST_PREFIX + train['scheduled'], train['status'])
        # We've an update, let's notify
        NOTIFY = 1

    if train['status'] == 'ON TIME' or train['status'] == 'EARLY':
        logger.info('The ' + train['scheduled'] + ' appears to be ' + train['status'].lower())

        # Notify and form the message depending on the info
        if NOTIFY and HASS:
            if bool(train['platform']):
                message = "The " + train['scheduled'] + " " + train['operator_name'] + " train from " + train['origin_name'] + " to " + train['destination_name'] + " is " + train['status'].lower() + " (" + train['estimated'] + ") and should land on platform" + train['platform']
            else:
                message = "The " + train['scheduled'] + " " + train['operator_name'] + " train from " + train['origin_name'] + " to " + train['destination_name'] + " is " + train['status'].lower() + " (" + train['estimated'] + ")"

            hass.services.call('notify', NOTIFY_ID, {
               "title": MSG_TITLE,
               "message": message})
        # Change the lamp colour
        if HASS and bool(LAMP_ID):
            hass.services.call('light', 'turn_on', {
                "entity_id": LAMP_ID,
                'color_name': 'green'})

    elif train['status'] == 'LATE':
        logger.info('The ' + train['scheduled'] + ' is is late (' + train['estimated'] + ')')
        # Notify and form the message depending on the info
        if NOTIFY and HASS:
            if bool(train['platform']):
                message = "The " + train['scheduled'] + " " + train['operator_name'] + " train from " + train['origin_name'] + " to " + train['destination_name'] + " is " + train['status'].lower() + " (" + train['estimated'] + ") and should land on platform" + train['platform']
            else:
                message = "The " + train['scheduled'] + " " + train['operator_name'] + " train from " + train['origin_name'] + " to " + train['destination_name'] + " is " + train['status'].lower() + " (" + train['estimated'] + ")"

            hass.services.call('notify', NOTIFY_ID, {
               "title": MSG_TITLE,
               "message": message})
        # Change the lamp colour
        if HASS and bool(LAMP_ID):
            hass.services.call('light', 'turn_on', {
                "entity_id": LAMP_ID,
                'color_name': 'orange'})

    elif train['status'] == 'CANCELLED':
        logger.info('The ' + train['scheduled'] + ' is cancelled')
        # Notify and form the message depending on the info
        if NOTIFY and HASS:
            message = "The " + train['scheduled'] + " " + train['operator_name'] + " train from " + train['origin_name'] + " to " + train['destination_name'] + " is " + train['status'].lower()

            hass.services.call('notify', NOTIFY_ID, {
               "title": MSG_TITLE,
               "message": message})
        # Change the lamp colour
        if HASS and bool(LAMP_ID):
            hass.services.call('light', 'turn_on', {
                "entity_id": LAMP_ID,
                'color_name': 'red'})
    # Sleep to keep the lamp colour shown for 1 second
    if HASS and boot(LAMP_ID): time.sleep(1)

attributes = {
            'VIC' :
            {
            "calling_at": "VIC",
            "station_code": "HHE",
            "icon": "mdi:train",
            "unit_of_measurement": "min",
            "next_trains": [
            {
            "operator_name": "Gatwick Express",
            "destination_name": "London Victoria",
            "scheduled": "07:03",
            "estimated": "07:03",
            "status": "ON TIME",
            "platform": "4",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "07:06",
            "estimated": "07:06",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Gatwick Express",
            "destination_name": "London Victoria",
            "scheduled": "07:34",
            "estimated": "07:34",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "07:40",
            "estimated": "07:40",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Littlehampton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "07:43",
            "estimated": "07:43",
            "status": "LATE",
            "platform": "4",
            "origin_name": "Seaford"
            },
            {
            "operator_name": "Gatwick Express",
            "destination_name": "London Victoria",
            "scheduled": "07:49",
            "estimated": "07:49",
            "status": "ON TIME",
            "platform": "4",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "08:00",
            "estimated": "08:00",
            "status": "ON TIME",
            "platform": "4",
            "origin_name": "Littlehampton"
            },
            {
            "operator_name": "Gatwick Express",
            "destination_name": "London Victoria",
            "scheduled": "08:06",
            "estimated": "08:06",
            "status": "ON TIME",
            "platform": "4",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "08:15",
            "estimated": "08:15",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Hastings"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "08:29",
            "estimated": "08:29",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Littlehampton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "08:44",
            "estimated": "08:44",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Hastings"
            }
            ],
            "friendly_name": "Next train to VIC"
            },
            'HHE' :
            {
            "calling_at": "VIC",
            "station_code": "HHE",
            "icon": "mdi:train",
            "unit_of_measurement": "min",
            "next_trains": [
            {
            "operator_name": "Gatwick Express",
            "destination_name": "London Victoria",
            "scheduled": "07:03",
            "estimated": "07:03",
            "status": "ON TIME",
            "platform": "4",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "07:06",
            "estimated": "07:06",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Gatwick Express",
            "destination_name": "London Victoria",
            "scheduled": "07:34",
            "estimated": "07:34",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "07:40",
            "estimated": "07:40",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Littlehampton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "07:43",
            "estimated": "07:43",
            "status": "LATE",
            "platform": "4",
            "origin_name": "Seaford"
            },
            {
            "operator_name": "Gatwick Express",
            "destination_name": "London Victoria",
            "scheduled": "18:44",
            "estimated": "18:49",
            "status": "ON TIME",
            "platform": "4",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "08:00",
            "estimated": "08:00",
            "status": "ON TIME",
            "platform": "4",
            "origin_name": "Littlehampton"
            },
            {
            "operator_name": "Gatwick Express",
            "destination_name": "London Victoria",
            "scheduled": "08:06",
            "estimated": "08:06",
            "status": "ON TIME",
            "platform": "4",
            "origin_name": "Brighton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "08:15",
            "estimated": "08:15",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Hastings"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "08:29",
            "estimated": "08:29",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Littlehampton"
            },
            {
            "operator_name": "Southern",
            "destination_name": "London Victoria",
            "scheduled": "08:44",
            "estimated": "08:44",
            "status": "ON TIME",
            "platform": "3",
            "origin_name": "Hastings"
            }
            ],
            "friendly_name": "Next train to VIC"
            }
            }

if len(TIMES) > 0:
    for direction in TIMES:
        if HASS == 0 or hass.states.get(SOURCE_SENSOR_PREFIX + direction).state != "No departures":
            try:
                # Let's look for our trains in those scheduled
                found = []
                for train in attributes[direction]['next_trains']:
                    # If we match mark it as found and process it
                    if train['scheduled'] in TIMES[direction]:
                        found.append(train['scheduled'])
                        processTrain(train, TIMES[direction])

                # Turn the light off once we've delivered our notification
                if HASS and bool(LAMP_ID):
                    hass.services.call('light', 'turn_off', {
                        "entity_id": LAMP_ID})

                # If we didn't find any its likely they've not been announced yet
                if len(found) == 0:
                    logger.warn('No ' + direction.lower() + ' departures found')

                # Let's tidy up hass states for trains that were not found
                for train in TIMES[direction]:
                    if train not in found:
                        logger.info('We did not find the ' + train + ' so mark it as no data in HASS')
                        if HASS: hass.states.set(TRAIN_SENSOR_PREFIX + train['scheduled'], 'No data')

            except:
                logger.error('Error in processing train times')
        else:
            logger.error('No departures found in ' + SOURCE_SENSOR_PREFIX + direction)
else:
    logger.error('TIMES dict not set correctly')
