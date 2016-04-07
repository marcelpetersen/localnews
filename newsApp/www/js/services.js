angular.module('starter.services', ['angularMoment', 'angularDjangoRegistrationAuthApp'])

.factory('httpRequestInterceptor', function ($localStorage, $cookies) {
  return {
    request: function (config) {
      
      if ($localStorage.token)
      {config.headers['Authorization'] = 'Token ' + $localStorage.token;
}
      return config;
    }
  };
})


.config(function ($httpProvider) {
  $httpProvider.interceptors.push('httpRequestInterceptor');
})


.factory ('newsSrvc', function ($http, BASE_URL, $q, $localStorage){

  

  var news  = {


    feeds: [],
    next : [],
    sources:[],
    exclude: [],


    checkSession: function(){
      var defer = $q.defer();

      if ($localStorage.token){
        defer.resolve(true);
        
      }
      else {defer.resolve(false);
      }

        return defer.promise;
      },



    all: function(){
        return $http.get(BASE_URL + '?limit=35&offset=1').then(function(response){
        news.next = response.data.next
        news.feeds = response.data.results;
      })
        
      },
    getNext: function (){
          var res;
          return $http.get(news.next).then(function(response){

            news.feeds = news.feeds.concat(response.data.results);
            news.next = response.data.next
            })
          
        },
    getSources: function(){
      return $http.get(BASE_URL + 'source/').then(function(response){
        news.sources = response.data;


      })
    },
    
    filter: function(checkvalue, some){
      if (checkvalue === 'true'){
       $localStorage.exclude =$localStorage.exclude.concat(some)
       $http.post(BASE_URL +'exclude/', {source: some}).then (function(response){}, function errorCallback(response){console.log ('Error already added')} )
      } 

      if (checkvalue === 'false'){
        index = $localStorage.exclude.indexOf(some)
        if (index > -1){
          $localStorage.exclude.splice(index, 1)
          $http.delete(BASE_URL + 'destroy/' + some).then (function(response){console.log('Deleted', some)})
        }
      }
    }

    }

  

  return news
})

.factory('FavSrvc', function($http, djangoAuth, $location, $localStorage, $state, BASE_URL, $q, SettingsSrvc, $ionicHistory){


  var favs = {

    token: [],
    favorites: [],
    count: 0,
    city:[],

    auth: function(user){

      djangoAuth.login(user.username, user.password).then(function(response){
         $location.path('/tab/chats')
        

      }, function(data){
        console.log('Error')
      })

    },

    logout: function(){
      djangoAuth.logout().then(function(res){
        $ionicHistory.clearCache().then(function(){
          $location.path('/splash')
        })
        
      })
    },

    username: function(){
      var deferred = $q.defer();
      $localStorage.exclude = []
     var math = Math.floor(Math.random() * 120000001)
      deferred.resolve( math, $localStorage.exclude)

      return deferred.promise




    }, 

    signup: function(user){
        djangoAuth.register(username = user,(password1 = 123456), (password2 = 123456) ).then(function (response){
          $localStorage.token = response.key
        })
    },

  
    populateFavs:function(){
      return $http.get(BASE_URL +'favorite/').then(function(response){  
      $localStorage.favs = response.data      
      })

    },

    returnFavs: function(){
      return $localStorage.favs
    },

    deleteFavs: function(index, favorite){

      return $http.delete(BASE_URL +'updatefavorite/' + favorite.id).then(function (response){
        $localStorage.favs.splice(index, 1)
      }, function(response){console.log ('ERROR Couldnt delete', response.data)} )
    },

    addFavs: function(news){
      
        return $http.post(BASE_URL +'favorite/', {fav_id: news.id, title: news.title, link:news.link, time:news.time, image:news.image, source:news.source} ).then(function(){
     favs.count ++;
  
      }, function(response){
      })      
 },
    
    favcount: function(){
      return favs.count;
    },

    states: function(main, location){
      return $http.post(BASE_URL + 'state/', {state: main, city:location.formatted_address}).then(function(){
        
      })
    }
  }
 return favs

})

.factory('SettingsSrvc', function($localStorage, $http, BASE_URL){

  var settings = {

    city: [],

    cities: function(){
      return $http.get(BASE_URL + 'city/').then(function(response){
        $localStorage.city = response.data
      })
    },

    addedLocations: function(){
      return $localStorage.city
    },

    removeLocation: function(index, state){
      return $http.delete(BASE_URL +'stateupdate/' + state.id).then(function(){
        $localStorage.city.splice(index,1)

      })
    },

    suggestion: function(name, link, location){
      return $http.post(BASE_URL + 'suggest/', {name:name, link:link, location:location})

    }


  }
  return settings

})







