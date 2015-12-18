import time

_STATE_OFF = 0
_STATE_COUNTING = 1
_STATE_PAUSED = 2

_state = _STATE_OFF
_value = 'stopwatch'

_LONG_WAIT_PERIOD = 600
timeoutPeriod = _LONG_WAIT_PERIOD
tickPeriod = 1

def setup(config):
	if 'timeoutPeriod' in config:
		global tickPeriod
		tickPeriod = config['tickPeriod']

def query():
	global _value

	if _state == _STATE_COUNTING:
		_value = _value + tickPeriod
	
	_v = None
	if _state != _STATE_OFF:
		_v = time.strftime("%H:%M:%S", time.gmtime(_value))
	else:
		_v = _value

	return [{
		'full_text': _v,
		'name': 'mystopwatch',
		'separator_block_width': 40
	}]

def handleClick(ev):
	global _state, timeoutPeriod, _value

	if ev['button'] == 1:
		if _state == _STATE_OFF:
			_value = 0
			_state = _STATE_COUNTING
			timeoutPeriod = tickPeriod
		elif _state == _STATE_COUNTING:
			_state = _STATE_PAUSED
			timeoutPeriod = _LONG_WAIT_PERIOD
		else:
			_state = _STATE_COUNTING
			timeoutPeriod = tickPeriod
	else:
		_value = 0
	
	return True
