#!/usr/bin/python
import engine as engine
import logging
import sys
import time
import settings

engine = engine.engine()

try:
	print '=== start loop', time.strftime("%c"), '==='

	own = engine.login('login', 'password')
	print own

	engine.parseGalaxy()

	print '=== end loop', time.strftime("%c"), '==='

except Exception, e:
	print e
	logging.exception("")
	engine.send_mail(e)

sys.exit()
