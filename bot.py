#!/bin/env python
# -*- coding: utf-8 -*-

# Set default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import socket
import time
from actions import *

network  = 'irc.freenode.net'
port     = 6667
# make shure to choose a uniq nickname
nick     = 'ctreffos-bot'
channel  = '#CTreffOS'
realname = 'JZ9mcOiAb9iopGPRQGij'

def irc_connect():
	irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
	irc.connect ( ( network, port ) )
	irc.send ( 'USER ' + realname + ' ' + network + ' blubb :pyIRCBot\n' )
	irc.send ( 'NICK ' + nick + '\n')
	return irc


def parse_msg( text ):
	data    = text.split()
	if len(data) >= 4 and data[1] == 'PRIVMSG':
		user    = text.split('!~')[0].replace( ':', '')
		try:
			message = text.split(':', 2)[2].rstrip('\n\r')
		except:
			message = ''
		if data[2].startswith('#'): # channel or user
			receiver = channel
		else:
			receiver = user
		return {
				'valid'    : 1,
				'user'     : user,
				'channel'  : data[2],
				'command'  : data[3],
				'receiver' : receiver,
				'message'  : message
			}
	# not a valid message
	return { 'valid' : 0 }



irc = irc_connect()

try:
	while True:
		text = irc.recv(4096)
		#print( text )

		# join channel after connect
		if text.find('Message of the Day') != -1:
			irc.send ( 'JOIN ' + channel + '\n')
		else:
			for line in text.replace('\r', '').split('\n'):

				# play ping pong
				if line.find('PING') != -1:
					irc.send('PONG ' + line.split()[1] + '\n')

				#reconnect
				elif line.find('Closing Link') != -1:
					time.sleep( 5 ) # wait five seconds
					irc = irc_connect()

				# we were to fast. wait a little bit longer
				elif line.startswith('ERROR') and line.find('throttled') != -1:
					time.sleep( 90 ) # wait five seconds
					irc = irc_connect()

				# check for commands
				try:
					msg = parse_msg( line )
					print '--> valid: %s' % msg
					if msg['valid']:

						if msg['command'] == ':!say':
							action_say( irc, msg )

						elif msg['command'] == ':!help':
							action_help( irc, msg )

						elif msg['command'] == ':!date':
							action_date( irc, msg )
					if line.endswith(' JOIN #CTreffOS'):
						action_date( irc, {'receiver':'#CTreffOS'})
				except:
					pass

finally:
	# send quit command
	irc.send ( 'QUIT :' + nick + ' waves goodbye...\n')
