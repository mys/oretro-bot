#!/usr/bin/python
import engine as engine
import logging
import sys
import time
import settings

engine = engine.engine()

try:
	while True:
		print '=== start loop', time.strftime("%c"), '==='
		sendProbes = False 
		# time.localtime().tm_hour >= 22 or time.localtime().tm_hour < 8
		# sys.exit()
		own = engine.login('login', 'password')
		print own

		if sendProbes:
			if not own['probes']:
				engine.attack(sendProbes)

		else:
			numberOfAttacks = 7
			if time.localtime().tm_hour >= 15 and time.localtime().tm_hour < 22 or time.localtime().tm_wday > 4:
				numberOfAttacks = 5

			for i in range(0, numberOfAttacks - own['attacks']):
				engine.attack()

		for i in range(0, 3 - own['transports']):
			engine.transport()

		# engine.active()

#		if time.localtime().tm_hour >= 2 and time.localtime().tm_hour < 3 and time.localtime().tm_min > 30:
#			engine.parseStats()

#		if time.localtime().tm_hour >= 8 and time.localtime().tm_hour < 9 and time.localtime().tm_min > 30:
#			engine.parseStats()

#		if time.localtime().tm_hour >= 16 and time.localtime().tm_hour < 17 and time.localtime().tm_min > 30:
#			engine.parseStats()

		print '=== end loop', time.strftime("%c"), '==='
		# time.sleep(1620) # 27 minutes

		if sendProbes:
			time.sleep(180) # 3 minutes
		else:
			break;

except Exception, e:
	print e
	logging.exception("")
	engine.send_mail(e)

sys.exit()
