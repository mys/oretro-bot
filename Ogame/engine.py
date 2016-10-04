#!/usr/bin/python
import math
import requests
import socket
import socks
import sqlite3
import smtplib
import json
import time
import settings
from bs4 import BeautifulSoup

class engine():

	def __init__(self):
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
		}
		self.session = requests.Session()
		self.sessionId = ''

	def session_get(self, url):
		time.sleep(1)
		return self.session.get(url)


	def session_post(self, url, post):
		time.sleep(1)
		answer = self.session.post(url, data = post, headers = self.headers, \
			timeout = 30)
		return answer

	
	def send_mail(self, content):
		SMTP_SERVER = ''
		SMTP_PORT = 587
		GMAIL_USERNAME = ''
		GMAIL_PASSWORD = '' #CAUTION: This is stored in plain text!

		recipient = ''
		subject = '[Imperator]'
		# emailText = 'under attack'

		emailText = '' + str(content) + ''

		headers = ["From: " + GMAIL_USERNAME,
				"Subject: " + subject,
				"To: " + recipient,
				"MIME-Version: 1.0",
				"Content-Type: text/html"]
		headers = "\r\n".join(headers)

		try:
			session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

			session.ehlo()
			session.starttls()
			session.ehlo

			session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

			session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + emailText)
			session.quit()
		except Exception, e:
			print e


	def login(self, login, password):
		answer = self.session_get('http://ogame1304.de/game/index.php?page=overview&session=' + self.sessionId)
		# print answer.content

		if 'Please remember that this is an INTERNATIONAL server' in answer.content or \
		   'Your session is invalid' in answer.content or \
		   'Please log in again' in answer.content:
			print 'logging..'
			post_data = {
				'login':login,
				'pass':password,
				'Abschicken':'Login',
				'v':'2'
			}

			answer = self.session_post('http://ogame1304.de/game/reg/login2.php', post_data)
			
			print answer
			self.sessionId = answer.content[81:-8]
			print self.sessionId

			redirectUrl = answer.content[43:-2]

			answer = self.session_get('http://ogame1304.de' + redirectUrl)
			print answer

		if 'flight attack' in answer.content:
			print 'under attack!'
			self.send_mail('under attack')

		return {
			'attacks': answer.content.count('return ownattack'),
			'transports': answer.content.count('return owntransport'),
			'probes': answer.content.count(';Espionage Probe ' + '{:,}'.format(settings.probes).replace(",","."))
		}

	def active(self):
		# Bela Tegeuse
		self.session_get('http://ogame1304.de/game/index.php?page=overview&session=' + self.sessionId + '&cp=33654210&mode=&gid=&messageziel=&re=0')
		# Caladan
		self.session_get('http://ogame1304.de/game/index.php?page=overview&session=' + self.sessionId + '&cp=33656662&mode=&gid=&messageziel=&re=0')
		# Ix
		self.session_get('http://ogame1304.de/game/index.php?page=overview&session=' + self.sessionId + '&cp=33657821&mode=&gid=&messageziel=&re=0')

	def sendProbes(self, galaxy, system, planet):
		answer = self.session_get('http://ogame1304.de/game/index.php?page=flotten1&session=' + self.sessionId + '&mode=Flotte')
		print answer

		post_data = {
			'maxship210':settings.probes,
			'consumption210':1,
			'speed210':180000000,
			'capacity210':5,
			'ship210':settings.probes
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flotten2&session=' + self.sessionId, post_data)
		print answer
		
		post_data = {
			'thisgalaxy':4,
			'thissystem':64,
			'thisplanet':5,
			'thisplanettype':1,
			'speedfactor':1,
			'ship210':settings.probes,
			'consumption210':1,
			'speed210':180000000,
			'capacity210':5,
			'galaxy':galaxy,
			'system':system,
			'planet':planet,
			'planettype':1,
			'speed':10
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flotten3&session=' + self.sessionId, post_data)
		print answer
		
		post_data = {
			'thisgalaxy':4,
			'thissystem':64,
			'thisplanet':5,
			'thisplanettype':1,
			'speedfactor':1,
			'galaxy':galaxy,
			'system':system,
			'planet':planet,
			'planettype':1,
			'ship210':settings.probes,
			'consumption210':1,
			'speed210':180000000,
			'capacity210':5,
			'speed':10,
			'order':1,
			'resource1':'',
			'resource2':'',
			'resource3':'',
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flottenversand&session=' + self.sessionId, post_data)
		print answer

		answer = self.session_get('http://ogame1304.de/game/index.php?page=overview&session=' + self.sessionId)
		if answer.content.count(';Espionage Probe ' + '{:,}'.format(settings.probes).replace(",",".")) == 0:
			self.send_mail('delete [' + str(galaxy) + ':' + str(system) + ':' + str(planet) + '] ?')
	
	def sendAttack(self, galaxy, system, planet):
		answer = self.session_get('http://ogame1304.de/game/index.php?page=flotten1&session=' + self.sessionId + '&mode=Flotte')
		print answer

		post_data = {
			'maxship202':4,
			'consumption202':20,
			'speed202':20000,
			'capacity202':5000,
			'ship202':4
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flotten2&session=' + self.sessionId, post_data)
		print answer
		
		post_data = {
			'thisgalaxy':4,
			'thissystem':64,
			'thisplanet':5,
			'thisplanettype':1,
			'speedfactor':1,
			'ship202':4,
			'consumption202':20,
			'speed202':20000,
			'capacity202':5000,
			'galaxy':galaxy,
			'system':system,
			'planet':planet,
			'planettype':1,
			'speed':10
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flotten3&session=' + self.sessionId, post_data)
		print answer
		
		post_data = {
			'thisgalaxy':4,
			'thissystem':64,
			'thisplanet':5,
			'thisplanettype':1,
			'speedfactor':1,
			'galaxy':galaxy,
			'system':system,
			'planet':planet,
			'planettype':1,
			'ship202':4,
			'consumption202':20,
			'speed202':20000,
			'capacity202':5000,
			'speed':10,
			'order':1,
			'resource1':'',
			'resource2':'',
			'resource3':'',
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flottenversand&session=' + self.sessionId, post_data)
		print answer

	def sendTransport(self, cp, galaxy, system, planet):
		answer = self.session_get('http://ogame1304.de/game/index.php?page=overview&session=' + self.sessionId + '&cp=' + cp + '&mode=&gid=&messageziel=&re=0')
		print answer

		answer = self.session_get('http://ogame1304.de/game/index.php?page=flotten1&session=' + self.sessionId + '&mode=Flotte')
		print answer

		post_data = {
			'maxship203':8,
			'consumption203':50,
			'speed203':13500,
			'capacity203':25000,
			'ship203':8
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flotten2&session=' + self.sessionId, post_data)
		print answer

		soup = BeautifulSoup(answer.content)
		resources = soup.findAll('td', {'class': 'header', 'width': '90'})
		metal = resources[0].text.replace('.', '')
		print metal
		crystal = resources[1].text.replace('.', '')
		print crystal
		deuter = resources[2].text.replace('.', '')
		print deuter

		post_data = {
			'thisgalaxy':galaxy,
			'thissystem':system,
			'thisplanet':planet,
			'thisplanettype':1,
			'speedfactor':1,
			'thisresource1':metal,
			'thisresource2':crystal,
			'thisresource3':deuter,
			'ship203':8,
			'consumption203':50,
			'speed203':13500,
			'capacity203':25000,
			'galaxy':'4',
			'system':'64',
			'planet':'5',
			'planettype':1,
			'speed':10
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flotten3&session=' + self.sessionId, post_data)
		print answer

		post_data = {
			'thisgalaxy':galaxy,
			'thissystem':system,
			'thisplanet':planet,
			'thisplanettype':1,
			'speedfactor':1,
			'thisresource1':metal,
			'thisresource2':crystal,
			'thisresource3':deuter,
			'galaxy':'4',
			'system':'64',
			'planet':'5',
			'planettype':1,
			'ship203':8,
			'consumption203':50,
			'speed203':13500,
			'capacity203':25000,
			'speed':10,
			'order':3,
			'resource1':metal,
			'resource2':crystal,
			'resource3':deuter,
		}
		answer = self.session_post('http://ogame1304.de/game/index.php?page=flottenversand&session=' + self.sessionId, post_data)
		print answer

	def attack(self, probes = False):
		if probes:
			print 'sending probes'
		else:
			print 'sending attack'
		planets = []
		lastAttack = time.time()
		planetToAttack = {}
		with open('/root/Ogame/planets.json', 'r') as file: 
			planets = json.load(file)
			for planet in planets:
				if planet['lastAttack'] < lastAttack:
					if probes or math.fabs(planet['coordinates'][1] - 64) < 50:
						lastAttack = planet['lastAttack']
						planetToAttack = planet

		print planetToAttack['coordinates']
		
		if probes:
			self.sendProbes(
				planetToAttack['coordinates'][0], 
				planetToAttack['coordinates'][1], 
				planetToAttack['coordinates'][2])
		else:
			self.sendAttack(
				planetToAttack['coordinates'][0], 
				planetToAttack['coordinates'][1], 
				planetToAttack['coordinates'][2])

		planetToAttack['lastAttack'] = time.time()
		
		with open('/root/Ogame/planets.json', 'w') as file: 
			json.dump(planets, file, indent=4)

	def transport(self):
		print 'sending transport'
		colonies = []
		lastTransport = time.time()
		colony = {}
		with open('/root/Ogame/colonies.json', 'r') as file:
			colonies = json.load(file)
			for col in colonies:
				if col['lastTransport'] < lastTransport:
					lastTransport = col['lastTransport']
					colony = col

		self.sendTransport(
			colony['cp'],
			colony['coordinates'][0], 
			colony['coordinates'][1], 
			colony['coordinates'][2])
		colony['lastTransport'] = time.time()

		with open('/root/Ogame/colonies.json', 'w') as file:
			json.dump(colonies, file, indent=4)

	def getTableResult(self, post_data):
		answer = self.session_post('http://ogame1304.de/game/index.php?page=stat&session=' + self.sessionId, post_data)
		# print answer
		# print answer.content
		s = answer.content[answer.content.index('<!-- begin show stats -->'):answer.content.index('<!-- end show stats -->')]
		
		s = s.replace('&nbsp;', '')
		s = s.replace('\n', '')
		# UTF-8
		s = s.replace('   	\t', '')
		s = s.replace('\t', '')
		s = s.replace('    ', '')
		s = s.replace('*', '')
		s = s.replace('+', '')
		s = s.replace('&ndash;', '')
		# print s

		soup = BeautifulSoup(s)
		table = soup.find("table")

		# The first tr contains the field names.
		headings = [th.get_text() for th in table.find("tr").find_all("td")]

		datasets = []
		for row in table.find_all("tr")[1:]:
			dataset = zip(headings, (td.get_text().strip() for td in row.find_all("th")))
			datasets.append(dataset)

		print len(datasets)
		return datasets
		
	def parseGalaxy(self):
		conn = sqlite3.connect('/root/Ogame/galaxy.sqlite')
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE if not exists galaxy(id INTEGER PRIMARY KEY, date DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, \'LOCALTIME\')), galaxy INT, system INT, position INT, name TEXT, moon TEXT, player TEXT, alliance TEXT)')
		
		for galaxy in range(1, 10):
			for system in range(1, 500):
				print galaxy, system
				post_data = {
					'session':self.sessionId,
					'galaxy':galaxy,
					'system':system
				}
				answer = self.session_post('http://ogame1304.de/game/index.php?page=galaxy&session=' + self.sessionId, post_data)
				
				s = answer.content
				s = s.replace('\r\n\r\n', ' ')
				
				soup = BeautifulSoup(s)
				table = soup.find("table", { "width": "569" })
				# table = soup.select('table[width=569]')
				# print table
				
				# The first tr contains the field names.
				# headings = [th.get_text() for th in table.find("tr").find_all("td")]
				headings = ['Slot', 'Planet', 'Name', 'Moon', 'DF', 'Player', 'Alliance', 'Actions']

				datasets = []
				for row in table.find_all("tr")[1:]:
					dataset = zip(headings, (td.get_text().strip() for td in row.find_all("th")))
					# print dataset
					datasets.append(dataset)

				# print len(datasets)
				# print datasets
				
				for dataset in datasets:
					print dataset
					if dataset and dataset[0][1] and int(dataset[0][1]) < 16:
						# #position
						# print dataset[0][1]
						# #name
						# print dataset[2][1]
						name = dataset[2][1]
						if u'\xa0' in dataset[2][1]:
							index = dataset[2][1].index(u'\xa0')
							name = dataset[2][1][:index]
						# #player
						# print dataset[5][1]
						# #alliance
						# print dataset[6][1]
						# print 'executing'
						cursor.execute("INSERT OR REPLACE INTO galaxy(id, galaxy, system, position, name, player, alliance) VALUES((SELECT id FROM galaxy WHERE galaxy='%d' AND system='%d' AND position='%d'),'%d','%d','%d','%s','%s','%s')" % (galaxy, system, int(dataset[0][1]), galaxy, system, int(dataset[0][1]), name, dataset[5][1], dataset[6][1]))
				conn.commit()

	def parseStats(self):
		# player_pts
		conn = sqlite3.connect('/root/Ogame/database.sqlite')
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE if not exists player_pts(id INTEGER PRIMARY KEY, date DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, \'LOCALTIME\')), rank INT, player TEXT, alliance TEXT, points INT)')

		start = 1
		lastRank = 0
		while True:
			post_data = {
				'who':'player',
				'type':'pts',
				'start':start,
				'ignorestart':0
			}
			
			datasets = self.getTableResult(post_data)

			if int(datasets[0][0][1]) == lastRank:
				break
			lastRank = int(datasets[0][0][1])

			for dataset in datasets:
				cursor.execute("INSERT INTO player_pts(rank, player, alliance, points) VALUES('%d','%s','%s','%d')" % (int(dataset[0][1]), dataset[1][1], dataset[3][1], int(dataset[4][1].replace('.',''))))
			conn.commit()
			
			start = start + 100
			print start
			
		# player_flt
		cursor.execute('CREATE TABLE if not exists player_flt(id INTEGER PRIMARY KEY, date DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, \'LOCALTIME\')), rank INT, player TEXT, alliance TEXT, points INT)')
		conn.commit()
		
		start = 1
		while True:
			post_data = {
				'who':'player',
				'type':'flt',
				'start':start,
				'ignorestart':0
			}
			
			datasets = self.getTableResult(post_data)

			if int(datasets[0][0][1]) == lastRank:
				break
			lastRank = int(datasets[0][0][1])

			for dataset in datasets:
				cursor.execute("INSERT INTO player_flt(rank, player, alliance, points) VALUES('%d','%s','%s','%d')" % (int(dataset[0][1]), dataset[1][1], dataset[3][1], int(dataset[4][1].replace('.',''))))
			conn.commit()
			
			start = start + 100
			print start
			
		# player_res
		cursor.execute('CREATE TABLE if not exists player_res(id INTEGER PRIMARY KEY, date DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, \'LOCALTIME\')), rank INT, player TEXT, alliance TEXT, points INT)')
		conn.commit()
		
		start = 1
		while True:
			post_data = {
				'who':'player',
				'type':'res',
				'start':start,
				'ignorestart':0
			}
			
			datasets = self.getTableResult(post_data)

			if int(datasets[0][0][1]) == lastRank:
				break
			lastRank = int(datasets[0][0][1])

			for dataset in datasets:
				cursor.execute("INSERT INTO player_res(rank, player, alliance, points) VALUES('%d','%s','%s','%d')" % (int(dataset[0][1]), dataset[1][1], dataset[3][1], int(dataset[4][1].replace('.',''))))
			conn.commit()
			
			start = start + 100
			print start
			
		# ally_pts
		cursor.execute('CREATE TABLE if not exists ally_pts(id INTEGER PRIMARY KEY, date DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, \'LOCALTIME\')), rank INT, alliance TEXT, member INT, points INT, perMember INT)')
		conn.commit()
		
		start = 1
		while True:
			post_data = {
				'who':'ally',
				'type':'pts',
				'start':start,
				'ignorestart':0
			}
			
			datasets = self.getTableResult(post_data)

			if int(datasets[0][0][1]) == lastRank:
				break
			lastRank = int(datasets[0][0][1])

			for dataset in datasets:
				cursor.execute("INSERT INTO ally_pts(rank, alliance, member, points, perMember) VALUES('%d','%s','%d','%d', '%d')" % (int(dataset[0][1]), dataset[1][1], int(dataset[3][1]), int(dataset[4][1].replace('.','')), int(dataset[5][1].replace('.',''))))
			conn.commit()
			
			start = start + 100
			print start
			
		# ally_flt
		cursor.execute('CREATE TABLE if not exists ally_flt(id INTEGER PRIMARY KEY, date DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, \'LOCALTIME\')), rank INT, alliance TEXT, member INT, points INT, perMember INT)')
		conn.commit()
		
		start = 1
		while True:
			post_data = {
				'who':'ally',
				'type':'flt',
				'start':start,
				'ignorestart':0
			}
			
			datasets = self.getTableResult(post_data)

			if int(datasets[0][0][1]) == lastRank:
				break
			lastRank = int(datasets[0][0][1])

			for dataset in datasets:
				cursor.execute("INSERT INTO ally_flt(rank, alliance, member, points, perMember) VALUES('%d','%s','%d','%d', '%d')" % (int(dataset[0][1]), dataset[1][1], int(dataset[3][1]), int(dataset[4][1].replace('.','')), int(dataset[5][1].replace('.',''))))
			conn.commit()
			
			start = start + 100
			print start
			
		# ally_res
		cursor.execute('CREATE TABLE if not exists ally_res(id INTEGER PRIMARY KEY, date DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, \'LOCALTIME\')), rank INT, alliance TEXT, member INT, points INT, perMember INT)')
		conn.commit()
		
		start = 1
		while True:
			post_data = {
				'who':'ally',
				'type':'res',
				'start':start,
				'ignorestart':0
			}
			
			datasets = self.getTableResult(post_data)

			if int(datasets[0][0][1]) == lastRank:
				break
			lastRank = int(datasets[0][0][1])

			for dataset in datasets:
				cursor.execute("INSERT INTO ally_res(rank, alliance, member, points, perMember) VALUES('%d','%s','%d','%d', '%d')" % (int(dataset[0][1]), dataset[1][1], int(dataset[3][1]), int(dataset[4][1].replace('.','')), int(dataset[5][1].replace('.',''))))
			conn.commit()
			
			start = start + 100
			print start
