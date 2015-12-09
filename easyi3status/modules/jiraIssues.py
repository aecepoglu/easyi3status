import requests
import json
import sys

from sh import zenity, ErrorReturnCode

myConfig = None

statusColors = {
	"In Progress": "#268bd2"
}

def setup(config):
	global myConfig, myAuth
	myConfig = config
	myAuth = (config['username'], config['password'])

def query():

	statuses = '+AND+'.join(json.loads(myConfig['statuses']))
	projects = ','.join(json.loads(myConfig['projects']))
	reqFilter = "assignee={}+AND+project+in+({})+AND+{}".format("'%s'"%myConfig['username'], projects, statuses)
	req = myConfig['api'] + "search?jql=" + reqFilter

	resp = requests.get(req, auth=myAuth)

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

def transit(key, tId):
	resp = requests.post(myConfig['api'] + "issue/" + key + "/transitions", headers={'content-type': 'application/json'}, data=json.dumps({'transition': {'id': tId}}), auth=myAuth)

def handleClick(ev):
	key = ev['name']

	taskResp = requests.get(myConfig['api'] + 'issue/' + key, auth=myAuth)
	task = taskResp.json()

	transitionsResp = requests.get(myConfig['api'] + 'issue/' + key + '/transitions', auth=myAuth)

	currentStatus = task['fields']['status']

	transitions = []
	for it in transitionsResp.json()['transitions']:
		if it['to']['id'] != currentStatus['id']:
			transitions += [it['id'], it['name']]
	
	
	summary = task['fields']['summary']
	description = task['fields']['description']
	reporter = task['fields']['reporter']['name']

	if description == None:
		description = ''
	
	try:
		transitionId = zenity(
			'--list',
			'--title', key,
			'--text', '<b>' + summary + ':</b> ' + description + '\n-<i>' + reporter + '</i>',
			'--column', 'ID', '--column', 'Transition',
			transitions
		).strip()

		if transitionId:
			transit(key, transitionId)
	except ErrorReturnCode:
		pass
