#!/usr/bin/env python3

import collections
import fileinput
import os
import sys
import threading

from importlib import import_module
from json import load as loadJson, dumps as dumpJson
from statusModule import EasyI3StatusModule
from time import time, sleep
from yaml import load as loadYaml

class EasyI3Status:
	modules = []
	DEFAULT_TIMEOUT_PERIOD = 60
	configDir = os.path.expanduser('~/.config/easyi3status')

	def readModules(self):
		now = time()

		elements = []

		for mod in self.modules:
			if mod.validUntil < now:
				mod.update()
				mod.validUntil = now + mod.validDuration

			elements = elements + mod.values

		print(dumpJson(elements) + ',')
		sys.stdout.flush()
	
	def loadConfig(self):
		fp = open(os.path.join(self.configDir, 'config.yaml'))
		values = loadYaml(fp)
		fp.close()

		if 'modules' not in values:
			raise '"modules" not in config'

		modConfigs = values['modules']

		for i in range(len(modConfigs)):
			it = modConfigs[i]
			if type(it) is str:
				it = {
					'name': it
				}
				modConfigs[i] = it
			elif type(it) is not dict:
				raise 'bad config at index ' + str(i) + '. It should be a dict'

			if 'config' not in it:
				it['config'] = {}

		return values

	def run(self):
		print('{"version":1, "click_events": false}\n[')

		config = self.loadConfig()

		sys.path.append(os.path.join(self.configDir, 'modules/'))


		for it in config["modules"]:
			module = import_module(it['name']).Module

			if not issubclass(module, EasyI3StatusModule):
				raise 'module must be subclass of EasyI3StatusModule'

			moduleInstance = module(it['config'])
			moduleInstance.setDefaults()
			self.modules.append(moduleInstance)

		while True:
			self.readModules()
			sleep(1)

if __name__ == '__main__':
	app  = EasyI3Status()
	app.run()
