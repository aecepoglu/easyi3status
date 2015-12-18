import json
import fileinput
import threading
import sys
import time
import collections

import ConfigParser, os, sys

class EasyI3Status:

	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

	# keeps a dict of modules in the form:
	#  {
	# 	module1: { timeout: T, module: M, latestValues: V },
	# 	module2: { timeout: T, module: M, latestValues: V },
	# 	...
	#  }
	# where
	#	T is timestamp until V is valid. Once current time is ahead of T, V will be updated
	#	M is the module instance
	modules = collections.OrderedDict()
	DEFAULT_TIMEOUT_PERIOD = 60

	def readModules(self):
		now = time.time()

		elements = []

		for modName, mod in self.modules.iteritems():
			module = mod['module']

			if mod['timeout'] > now:
				elements = elements + mod['latestValues']
				continue
			elif hasattr(module, 'timeoutPeriod'):
				mod['timeout'] = now + module.timeoutPeriod
			else:
				mod['timeout'] = now + self.DEFAULT_TIMEOUT_PERIOD

			fetched = module.query()

			for it in fetched:
				it['instance'] = modName
				elements.append(it)

			mod['latestValues'] = fetched

		print json.dumps(elements) + ","
		threading.Timer(1, self.readModules).start()

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
			self.modules[name] = {
				'module': module,
				'timeout': 0,
				'latestValues': []
			}

		self.readModules()

		sys.stdin.readline()

		while 1:
			line = sys.stdin.readline()

			if line.startswith(","):
				line = line[1:]
			
			jsonobj = json.loads(line)

			moduleContainer = self.modules[jsonobj['instance']]
			module = moduleContainer['module']

			if hasattr(module, 'handleClick'):
				if module.handleClick(jsonobj):
					moduleContainer['timeout'] = 0

def run():
	app = EasyI3Status()
	app.run()

if __name__ == '__main__':
	run()
