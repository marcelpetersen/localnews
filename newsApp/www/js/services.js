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
        return $http.get(BASE_URL + '?limit=10&offset=1').then(function(response){
        console.log ('got data',response.data);
        news.next = response.data.next
        news.feeds = response.data.results;
      })
        
      },
    getNext: function (){
          var res;
          return $http.get(news.next).then(function(response){

            news.feeds = news.feeds.concat(response.data.results);
            console.log(response.data)
            news.next = response.data.next
            console.log(news.next)
            })
          
        },
    getSources: function(){
      return $http.get(BASE_URL + 'source/').then(function(response){
        console.log(response.data)
        news.sources = response.data;


      })
    },
    
    filter: function(checkvalue, some){
      if (checkvalue === 'true'){
       $localStorage.exclude =$localStorage.exclude.concat(some)
       console.log('added:', news.exclude)
       $http.post(BASE_URL +'exclude/', {source: some}).then (function(response){console.log(response.data)}, function errorCallback(response){console.log ('Error already added')} )
      } 

      if (checkvalue === 'false'){
        index = $localStorage.exclude.indexOf(some)
        if (index > -1){
          $localStorage.exclude.splice(index, 1)
          $http.delete(BASE_URL + 'destroy/' + some).then (function(response){console.log('Deleted', some)})
        }
        console.log('removed', some, $localStorage.exclude)
      }
    }

    }

  

  return news
})

.factory('FavSrvc', function($http, djangoAuth, $location, $localStorage, $state, BASE_URL, $q, SettingsSrvc){


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
        $location.path('/splash')
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
          console.log(response.key)
          $localStorage.token = response.key
        })
    },

  
    populateFavs:function(){
      return $http.get(BASE_URL +'favorite/').then(function(response){  
      console.log('Popuating favs', response.data)
      $localStorage.favs = response.data
      console.log('favs', $localStorage.favs)
      
      })

    },

    returnFavs: function(){
            console.log("returned favs")

      return $localStorage.favs
    },

    deleteFavs: function(index, favorite){

      return $http.delete(BASE_URL +'updatefavorite/' + favorite.id).then(function (response){
        $localStorage.favs.splice(index, 1)
        console.log('deleted', favorite)
      }, function(response){console.log ('Couldnt delete', response.data)} )
    },

    addFavs: function(news){
      
        return $http.post(BASE_URL +'favorite/', {fav_id: news.id, title: news.title, link:news.link, time:news.time, image:news.image, source:news.source} ).then(function(){
     favs.count ++;
  
      }, function(response){
        // console.log("Error", $localStorage.token)
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
        console.log(response.data)
        $localStorage.city = response.data
        console.log($localStorage.city)
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







