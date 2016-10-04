var app = angular.module('malinkaApp',
    ['ngMaterial', 'ngAnimate', 'ngRoute', 'md.data.table', 'highcharts-ng']);

app.controller('malinkaController', function ($scope, $http) {

    $scope.hideAds = false;
    $scope.stats = [];

    // $(document).ready(function(){
    //     $('ins').each(function(){
    //         console.log('ads');
    //         (adsbygoogle = window.adsbygoogle || []).push({});
    //     });
    // });
});

app.config(function($locationProvider) {
    $locationProvider
        .html5Mode({
            enabled: true, // set HTML5 mode
            requireBase: false // I removed this to keep it simple, but you can set your own base url
        });
})

app.config(function($routeProvider) {
    $routeProvider
        .when('/players_pts', {templateUrl: '/views/players_pts.html', controller: 'PlayerPtsCtrl'})
        .when('/ally_pts', {templateUrl: '/views/ally_pts.html', controller: 'AllyPtsCtrl'})
        .when('/map', {templateUrl: '/views/map.html', controller: 'MapCtrl'})
        .when('/api', {templateUrl: '/views/api.html', controller: 'ApiCtrl'})
        .otherwise('/players_pts');
})

app.controller('PlayerPtsCtrl', function ($scope, $http) {

    $scope.type = 'pts';
    $scope.rank = 0;
    $scope.ranks = [];
    $scope.selectedPlayer = '';
	$scope.planets = [];

    $scope.reload = function(){
        $http.get('/api/players_' + $scope.type).then(function(response) {
            $scope.stats = response.data;
            $scope.ranks.length = 0;
            for (var i = 0; i < $scope.stats.length; i+=100){
                $scope.ranks.push(i);
            }
        });
    }

    $scope.getPlayer = function(player){
        $scope.selectedPlayer = player;
        $http.get('/api/player_pts/' + player).then(function(response) {
            $scope.chartConfigPoints.series[0].data.length = 0;
            for (var i = 0; i < response.data.length; i++){
                $scope.chartConfigPoints.series[0].data.push([Date.parse(response.data[i].date), response.data[i].points]);
            }
        });
        $http.get('/api/player_flt/' + player).then(function(response) {
            $scope.chartConfigFleet.series[0].data.length = 0;
            for (var i = 0; i < response.data.length; i++){
                $scope.chartConfigFleet.series[0].data.push([Date.parse(response.data[i].date), response.data[i].points]);
            }
        });
        $http.get('/api/player_res/' + player).then(function(response) {
            $scope.chartConfigResearch.series[0].data.length = 0;
            for (var i = 0; i < response.data.length; i++){
                $scope.chartConfigResearch.series[0].data.push([Date.parse(response.data[i].date), response.data[i].points]);
            }
        });
        $http.get('/api/player_gal/' + player).then(function(response) {
            $scope.planets = response.data;
        });
    }

    $scope.chartConfigPoints = {
        options: {
            chart: {
                // type: 'bar'
            },
            rangeSelector: {
                enabled: false
            },
            navigator: {
                enabled: false
            }
        },
        series: [{
            name: 'Points',
            data: []
        }],
        title: {
            text: 'Points'
        },
        useHighStocks: true
    }

    $scope.chartConfigFleet = {
        options: {
            chart: {
                // type: 'bar'
            },
            rangeSelector: {
                enabled: false
            },
            navigator: {
                enabled: false
            }
        },
        series: [{
            name: 'Fleet',
            data: []
        }],
        title: {
            text: 'Fleet'
        },
        useHighStocks: true
    }

    $scope.chartConfigResearch = {
        options: {
            chart: {
                // type: 'bar'
            },
            rangeSelector: {
                enabled: false
            },
            navigator: {
                enabled: false
            }
        },
        series: [{
            name: 'Research',
            data: []
        }],
        title: {
            text: 'Research'
        },
        useHighStocks: true
    }

    $scope.reload();
});

app.controller('AllyPtsCtrl', function ($scope, $http) {

    $scope.type = 'pts';
    $scope.rank = 0;
    $scope.ranks = [];
    $scope.players = [];
    $scope.selectedPlayer = '';
	$scope.planets = [];

	$scope.reload = function(){
        $http.get('/api/ally_' + $scope.type).then(function(response) {
            $scope.stats = response.data;            
            $scope.ranks.length = 0;
            for (var i = 0; i < $scope.stats.length; i+=100){
                $scope.ranks.push(i);
            }
        });
    }

    $scope.getAlliance = function(alliance){
        $scope.selectedAlliance = alliance;
        $http.get('/api/ally_pts/' + alliance).then(function(response) {
            $scope.players = response.data;
        })
        // .then(function(){
        //     console.log($scope.players);
        //     for (var i = 0; i < $scope.players.length; i++){
        //         console.log($scope.players);
        //         console.log($scope.players[i].player);
        //         $http.get('/api/player_pts/' + $scope.players[i].player).then(function(responsee) {
        //             var data = [];
        //             for (var j = 0; j < responsee.data.length; j++){
        //                 data.push([Date.parse(responsee.data[j].date), responsee.data[j].points]);
        //             }
        //             console.log(responsee.data);
        //             $scope.chartConfig.series.push({ 'name': responsee.data[0].player, 'data': data });
        //         });
        //     }
        //     console.log($scope.chartConfig.series);
        // });
    }

    

    $scope.getPlayer = function(player){
        $scope.selectedPlayer = player;
        $http.get('/api/player_pts/' + player).then(function(response) {
            $scope.chartConfigPoints.series[0].data.length = 0;
            for (var i = 0; i < response.data.length; i++){
                $scope.chartConfigPoints.series[0].data.push([Date.parse(response.data[i].date), response.data[i].points]);
            }
        });
        $http.get('/api/player_flt/' + player).then(function(response) {
            $scope.chartConfigFleet.series[0].data.length = 0;
            for (var i = 0; i < response.data.length; i++){
                $scope.chartConfigFleet.series[0].data.push([Date.parse(response.data[i].date), response.data[i].points]);
            }
        });
        $http.get('/api/player_res/' + player).then(function(response) {
            $scope.chartConfigResearch.series[0].data.length = 0;
            for (var i = 0; i < response.data.length; i++){
                $scope.chartConfigResearch.series[0].data.push([Date.parse(response.data[i].date), response.data[i].points]);
            }
        });
        $http.get('/api/player_gal/' + player).then(function(response) {
            $scope.planets = response.data;
        });
    }

    $scope.chartConfig = {
        options: {
            chart: {
                // type: 'bar'
            },
            rangeSelector: {
                enabled: false
            },
            navigator: {
                enabled: false
            }
        },
        series: [],
        title: {
            text: 'Points'
        },
        useHighStocks: true
    }

    $scope.chartConfigPoints = {
        options: {
            chart: {
                // type: 'bar'
            },
            rangeSelector: {
                enabled: false
            },
            navigator: {
                enabled: false
            }
        },
        series: [{
            name: 'Points',
            data: []
        }],
        title: {
            text: 'Points'
        },
        useHighStocks: true
    }

    $scope.chartConfigFleet = {
        options: {
            chart: {
                // type: 'bar'
            },
            rangeSelector: {
                enabled: false
            },
            navigator: {
                enabled: false
            }
        },
        series: [{
            name: 'Fleet',
            data: []
        }],
        title: {
            text: 'Fleet'
        },
        useHighStocks: true
    }

    $scope.chartConfigResearch = {
        options: {
            chart: {
                // type: 'bar'
            },
            rangeSelector: {
                enabled: false
            },
            navigator: {
                enabled: false
            }
        },
        series: [{
            name: 'Research',
            data: []
        }],
        title: {
            text: 'Research'
        },
        useHighStocks: true
    }

    $scope.reload();
});

app.controller('MapCtrl', function ($scope, $http) {

    $scope.galaxy = 1;
    $scope.system = 1;
    $scope.planets = [];

    $scope.getGalaxy = function(){
        $http.get('/api/galaxy?galaxy=' + $scope.galaxy + '&system=' + $scope.system).then(function(response) {
            $scope.planets = response.data;
        });
    }
    $scope.getGalaxy();
});

app.controller('ApiCtrl', function ($scope, $http) {

});

app.config(function($mdThemingProvider) {
    $mdThemingProvider.theme('dark-grey').backgroundPalette('grey').dark();
    $mdThemingProvider.theme('dark-orange').backgroundPalette('orange').dark();
    $mdThemingProvider.theme('dark-purple').backgroundPalette('deep-purple').dark();
    $mdThemingProvider.theme('dark-blue').backgroundPalette('blue').dark();
});