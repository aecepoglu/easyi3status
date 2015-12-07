import json
import fileinput
import threading
import sys
import time

import ConfigParser, os, sys

from sh import zenity, ErrorReturnCode

print '{"version":1, "click_events": true}'
print '['

modules = {}

config = ConfigParser.ConfigParser()
config.read([
	os.path.expanduser('~/.easyi3status/config.cfg')
])

sys.path.append(os.path.expanduser('~/.easyi3status/'))

for name in config.sections():
	module = __import__(name)

	module.setup( dict(config.items(name)) )
	modules[name] = module

elements = []

def readModules():
	elements = []
	for modName, mod in modules.iteritems():
		fetched = mod.query()
		for it in fetched:
			it['instance'] = modName
			elements.append(it)
	
	print json.dumps(elements) + ","
	threading.Timer(10, readModules).start()

readModules()

sys.stdin.readline()

while 1:
	line = sys.stdin.readline()

	if line.startswith(","):
		line = line[1:]
	
	jsonobj = json.loads(line)

	module = modules[jsonobj['instance']]

	possibleActions = module.listActions()
	msg = module.get(jsonobj['name'])

	selected = False
	while not selected:
		try:
			selection = zenity("--entry", "--title", "jira", "--text", msg + "\n(" + "/".join(possibleActions) + ") ?")
			selection = selection.strip()

			if selection in possibleActions:
				selected = True
				method = getattr(module, selection)
				method(jsonobj['name'])
		except ErrorReturnCode:
			selected = True
