import json
import fileinput
import threading
import sys
import time
import collections

import ConfigParser, os, sys

class EasyI3Status:

	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
	modules = collections.OrderedDict()

	def readModules(self):
		elements = []
		for modName, mod in self.modules.iteritems():
			fetched = mod.query()
			for it in fetched:
				it['instance'] = modName
				elements.append(it)
		
		print json.dumps(elements) + ","
		threading.Timer(10, self.readModules).start()

	def run(self):
		print '{"version":1, "click_events": true}'
		print '['


		config = ConfigParser.ConfigParser()
		config.read([
			os.path.expanduser('~/.easyi3status/config.cfg')
		])

		sys.path.append(os.path.expanduser('~/.easyi3status/modules/'))

		for name in config.sections():
			module = __import__(name)

			module.setup( dict(config.items(name)) )
			self.modules[name] = module

		elements = []

		self.readModules()

		sys.stdin.readline()

		while 1:
			line = sys.stdin.readline()

			if line.startswith(","):
				line = line[1:]
			
			jsonobj = json.loads(line)

			module = self.modules[jsonobj['instance']]

			if hasattr(module, 'handleClick'):
				module.handleClick(jsonobj)

def run():
	app = EasyI3Status()
	app.run()

if __name__ == '__main__':
	run()
