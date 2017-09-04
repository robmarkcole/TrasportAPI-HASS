############################################
# Enter your your sensor name here.        #
############################################
entity_id = 'sensor.next_train_to_wim'
scheduled = False   # Check if train scheduled
train_time = '07:15'

if hass.states.get(entity_id).state == "No departures":
  logger.warn('No Departures')
else:
  attributes = hass.states.get(entity_id).attributes
  morning_train_status = hass.states.get('sensor.morning_train').state
  try:
    for train in attributes['next_trains']:
      if train['scheduled'] == train_time:
          scheduled = True   # Check if train scheduled
          if train['status'] != morning_train_status:
              hass.states.set('sensor.morning_train', train['status'])

              if train['status'] == 'ON TIME':
                  hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'green' })
                  hass.services.call('notify', 'robins_and_marias_iphones', { "title": "Train Status Update", "message": "The {} is scheduled to be on time.".format(train_time)})
              elif train['status'] == 'LATE':
                  hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'orange' })
                  hass.services.call('notify', 'robins_and_marias_iphones', { "title": "Train Status Update", "message": "The {} will be late and is now sheduled at".format(train_time) + train['estimated']})
              elif train['status'] == 'CANCELLED':
                  hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'red' })
                  hass.services.call('notify', 'robins_and_marias_iphones', { "title": "Train Status Update", "message": "The {} has been cancelled.".format(train_time)})
          break
  except:
    logger.warn('Failed to get next trains')

if not scheduled:
    hass.states.set('sensor.my_early_train', 'No data')  # check no data
#logger.warn('Test complete')
