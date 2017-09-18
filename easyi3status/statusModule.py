class EasyI3StatusModule:
	def __init__(self, config):
		self.setDefaults()
	
	def setDefaults(self):
		if not hasattr(self, 'values'):
			self.values = []

		if not hasattr(self, 'validuntil'):
			self.validUntil = 0

		if not hasattr(self, 'validDuration'):
			self.validDuration = 60;

	def update(self):
		pass
