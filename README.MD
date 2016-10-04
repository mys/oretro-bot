# ORETRO

Ogame Retro Uni1 scripts in python

### Engine functions

Ogame/engine.py functions

  - autologin
  - enemy flight attack check
  - activity* sets for planets
  - send attacks (+ probe farming)
  - send transports
  - crawl statistics page
  - crawl galaxy view
  - store data in SQL
  - extract data in HTTP webserver
  - email notifications (enemy flight attack, spying, errors etc.)

### Run scripts

Statistics page scan.
You need to edit Ogame/ogame-statistics.py:13 (login, password)

```sh
$ cd Ogame
$ python ogame-statistics.py
```

Galaxy page scan.
You need to edit Ogame/ogame-galaxy.py:13 (login, password)

```sh
$ cd Ogame
$ python ogame-galaxy.py
```

Full bot.
You need to edit Ogame/ogame.py:16 (login, password)
  - enemy flight attack email notifications
  - send farmings
  - send transports from colonies to base

```sh
$ cd Ogame
$ python ogame.py
```

### Run HTTP server

ORETRO requires [Node.js](https://nodejs.org/) v4+ to run (tested on v4.2.1)

```sh
$ cd www
$ sudo apt-get install nodejs
$ node www/server.js
```