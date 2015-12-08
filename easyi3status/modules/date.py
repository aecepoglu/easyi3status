from datetime import datetime

myConfig = None

def setup(config):
	global myConfig
	myConfig = config

def query():

	elements = []
	key = datetime.now().strftime('%d-%m-%Y %H:%M')

	elem = {
		'full_text': key,
		'name': key
	}

	elements.append(elem)
	
	elements[-1]['separator_block_width'] = 40
	
	return elements
