/* global __dirname */
var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var fs = require('fs');
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('/root/Ogame/database.sqlite');
var db2 = new sqlite3.Database('/root/Ogame/galaxy.sqlite')
var router = express.Router();

// ----------------------------------------------------------------------------
// express
// ----------------------------------------------------------------------------

app.use(express.static(__dirname + '/public'));
app.use('/bower_components', express.static(__dirname + '/bower_components'));
app.use('/node_modules', express.static(__dirname + '/node_modules'));
app.use('/views', express.static(__dirname + '/views'));
app.use(function (req, res, next) {
	var ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
	console.log('Client IP:', ip);
	next();
});

// ----------------------------------------------------------------------------
// api
// ----------------------------------------------------------------------------

app.get('/api/players_pts', function(req, res) {
	db.all("SELECT rank, player, trim(alliance) AS alliance, points FROM player_pts WHERE date > datetime('now', '-8 hours', 'localtime')", function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/ally_pts', function(req, res) {
	db.all("SELECT rank, trim(alliance) AS alliance, member, points, perMember FROM ally_pts WHERE date > datetime('now', '-8 hours', 'localtime')", function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/players_flt', function(req, res) {
	db.all("SELECT rank, player, trim(alliance) AS alliance, points FROM player_flt WHERE date > datetime('now', '-8 hours', 'localtime')", function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/ally_flt', function(req, res) {
	db.all("SELECT rank, trim(alliance) AS alliance, member, points, perMember FROM ally_flt WHERE date > datetime('now', '-8 hours', 'localtime')", function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/players_res', function(req, res) {
	db.all("SELECT rank, player, trim(alliance) AS alliance, points FROM player_res WHERE date > datetime('now', '-8 hours', 'localtime')", function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/ally_res', function(req, res) {
	db.all("SELECT rank, trim(alliance) AS alliance, member, points, perMember FROM ally_res WHERE date > datetime('now', '-8 hours', 'localtime')", function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/player_pts/:player', function(req, res) {
	db.all('SELECT date, rank, player, trim(alliance) AS alliance, points FROM player_pts WHERE player = ? LIMIT 90', req.params.player, function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/player_flt/:player', function(req, res) {
	db.all('SELECT date, rank, player, trim(alliance) AS alliance, points FROM player_flt WHERE player = ? LIMIT 90', req.params.player, function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/player_res/:player', function(req, res) {
	db.all('SELECT date, rank, player, trim(alliance) AS alliance, points FROM player_res WHERE player = ? LIMIT 90', req.params.player, function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/player_gal/:player', function(req, res) {
	db2.all('SELECT galaxy, system, position, name, moon, player, alliance FROM galaxy WHERE player LIKE ?', req.params.player+'%', function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

// player_pts top limit 90
app.get('/api/top', function(req, res) {
	db.all('SELECT date, points FROM player_pts WHERE rank = 1 LIMIT 90', function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

// ally_pts/:alliance -8 hours
app.get('/api/ally_pts/:alliance', function(req, res) {
	db.all("SELECT date, rank, player, trim(alliance) AS alliance, points FROM player_pts WHERE trim(alliance) = ? AND date > datetime('now', '-8 hours', 'localtime') ORDER BY rank", req.params.alliance, function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.get('/api/galaxy', function(req, res) {
	db2.all("SELECT galaxy, system, position, name, moon, player, alliance FROM galaxy WHERE galaxy = ? AND system = ?", req.query.galaxy, req.query.system, function(err, rows) {
		if (err){
			// console.err(err);
			res.status(500);
		}else {
			res.json(rows);
		}
		res.end();
	});
})

app.use('*', function(req, res){
	console.log('*');
	res.sendFile(__dirname + '/public/index.html');
});

// ----------------------------------------------------------------------------
// listen:80
// ----------------------------------------------------------------------------

server.listen(80, function() {
    console.log('Server running at localhost:80');
});
