import requests
import json

_apiUrl = 'https://btcturk.com/api/ticker'

timeoutPeriod = 60

def setup(config):
	pass

def query():
	resp = requests.get(_apiUrl, verify=True)

	if resp.status_code != 200:
		return []
	
	jsonobj = resp.json()

	descriptions = []

	return [{
		'full_text': u'B⃦/₺ ' + str(jsonobj['average']) + ' (' + str(round(jsonobj['average'] - jsonobj['open'], 1)) + ')',
		'separator_block_width': 40
	}]
