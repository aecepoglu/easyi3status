import requests
import json
import sys

myConfig = None

statusColors = {
	"In Progress": "#268bd2"
}

def setup(config):
	global myConfig
	myConfig = config

def query():

	statuses = '+AND+'.join(json.loads(myConfig['statuses']))
	projects = ','.join(json.loads(myConfig['projects']))
	reqFilter = "assignee={}+AND+project+in+({})+AND+{}".format("'%s'"%myConfig['username'], projects, statuses)
	req = myConfig['api'] + "search?jql=" + reqFilter

	resp = requests.get(req, auth=(myConfig['username'], myConfig['password']))

	if resp.status_code != 200:
		return []
	
	jsonobj = resp.json()

	elements = []
	
	for it in jsonobj['issues']:
		key = it['key']
		issuetype = it['fields']['issuetype']['name']
		status = it['fields']['status']['name']
	
		elem = {
			'full_text': key,
			'name': key
		}
	
		if status in statusColors:
			elem['color'] = statusColors[status]
			
		elements.append(elem)
	
	if (len(elements) > 0):
		elements[-1]['separator_block_width'] = 40
	
	return elements

def get(key):
	resp = requests.get(myConfig['api'] + "issue/" + key, auth=(myConfig['username'], myConfig['password']))
	
	if resp.status_code != 200:
		return []
	
	jsonobj = resp.json()

	title = key
	summary = jsonobj['fields']['summary']
	description = jsonobj['fields']['description']
	reporter = jsonobj['fields']['reporter']['name']

	return "%s\n%s\n%s\n\n- %s" % (title, description, summary, reporter)

def listActions():
	return ['resolve', 'start', 'todo']

def transit(key, tId):
	resp = requests.post(myConfig['api'] + "issue/" + key + "/transitions", headers={'content-type': 'application/json'}, data=json.dumps({'transition': {'id': tId}}), auth=(myConfig['username'], myConfig['password']))

def resolve(key):
	transit(key, 31)

def start(key):
	transit(key, 21)

def todo(key):
	transit(key, 11)
