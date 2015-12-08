import imaplib
from time import time
import os
import subprocess

myConfig = None

criterion = 'UNSEEN'
hide_if_zero = False
mailbox = 'inbox'
format = 'Mail: {unseen}'
new_mail_color = '#00f210'

statusColors = {
	"In Progress": "#268bd2"
}

def setup(config):
	global myConfig
	myConfig = config

def _get_mail_count():
	try:
		mail_count = 0
		directories = mailbox.split(',')
		connection = imaplib.IMAP4_SSL(myConfig['imap_server'], myConfig['port'])
		res = connection.login(myConfig['user'], myConfig['password'])

		for directory in directories:
			connection.select(directory)
			unseen_response = connection.search(None, criterion)
			mails = unseen_response[1][0].split()
			mail_count += len(mails)

		connection.close()
		return mail_count

	except Exception, e:
		return e


def query():

	elements = []
	imapElem = {'name': 'imap'}

	mail_count = _get_mail_count()

	if mail_count == 'N/A':
		imapElem['full_text'] = mail_count
	elif mail_count != 0:
		imapElem['color'] = new_mail_color
		imapElem['full_text'] = format.format(unseen=mail_count)
	else:
		imapElem['full_text'] = format.format(unseen=mail_count)

	elements.append(imapElem)
	
	if (len(elements) > 0):
		elements[-1]['separator_block_width'] = 40
	
	return elements
