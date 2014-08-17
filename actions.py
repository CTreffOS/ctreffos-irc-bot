#!/bin/env python
# -*- coding: utf-8 -*-

# Set default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
from datetime import date, timedelta

def eventdate(target_day, target_ordinal):
	d = date.today()
	f = date(d.year, d.month, 1)

	match = 0
	while True:
		match += int(f.weekday() == target_day)
		if d <= f and match == target_ordinal:
			return f
		f += timedelta(1)
		if f.day == 1:
			match == 0;

def action_say( irc, msg ):
	irc.send('PRIVMSG ' + msg['receiver'] + ' :hello!\n')


def action_help( irc, msg ):
	irc.send('PRIVMSG ' + msg['user'] + ' :!say       -- simple test. the bot will say hallo.\n')
	irc.send('PRIVMSG ' + msg['user'] + ' :!date      -- Post the next meeting date.\n')
	irc.send('PRIVMSG ' + msg['user'] + ' :!help      -- you know what will happen.\n')
	# make shure not too much messages are send in a row
	time.sleep(0.7)

def action_date( irc, msg ):
	irc.send('PRIVMSG %s :Das nächste Treffen des Chaostreffs Osnabrück ist: %s\n' % ( msg.get('receiver'), eventdate(0, 4) ))
	time.sleep(0.7)
