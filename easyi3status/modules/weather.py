# CONFIG VARIABLES
# * appid: openweathermaps API KEY. Required
# * city: openweathermaps city id. Required. Find yours here: http://bulk.openweathermap.org/sample/
# * units: either one of 'standard', 'metrics' or 'imperial'. Optional. Default to 'standard'
# * language: Optional

import requests
import json

_apiUrl = None

timeoutPeriod = 10800 #3 hours

def setup(config):
	global _apiUrl

	_apiUrl = 'http://api.openweathermap.org/data/2.5/weather?id=' + config['city'] + '&APPID=' + config['appid']

	if 'units' in config:
		_apiUrl = _apiUrl +  '&units=' + config['units']
	
	if 'language' in config:
		_apiUrl = _apiUrl + '&lang=' + config['language']
		
	
	

def query():
	resp = requests.get(_apiUrl)

	if resp.status_code != 200:
		return []
	
	jsonobj = resp.json()

	descriptions = []

	for weather in jsonobj['weather']:
		descriptions.append(weather['description'])

	return [{
		'full_text': '; '.join(descriptions) + ' ' + str(jsonobj['main']['temp']) + '\u00B0'.decode('unicode-escape'),
		'separator_block_width': 40
	}]
