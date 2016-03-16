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
      return $http.get('http://localhost:8000/api/feeds/source/').then(function(response){
        console.log(response.data)
        news.sources = response.data;

      })
    },
    
    filter: function(checkvalue, some){
      if (checkvalue === 'add'){
       news.exclude =news.exclude.concat(some)
       console.log('added:', news.exclude)
       $http.post('http://localhost:8000/api/feeds/exclude/', {source: some}).then (function(response){console.log(response.data)}, function errorCallback(response){console.log ('Error already added')} )
      } 

      if (checkvalue === 'remove'){
        index = news.exclude.indexOf(some)
        if (index > -1){
          news.exclude.splice(index, 1)
          $http.delete('http://localhost:8000/api/feeds/destroy/' + some).then (function(response){console.log('Deleted', some)})
        }
        console.log('removed', some, news.exclude)
      }

    }

    }

  

  return news
})

.factory('FavSrvc', function($http, djangoAuth, $location, $localStorage, $state){


  var favs = {

    token: [],
    favorites: [],
    count: 0,

    auth: function(user){
      djangoAuth.login(user.username, user.password).then(function(response){
        console.log($localStorage.token)
        $location.path('/tab/chats')

      }, function(data){
        console.log('Error')
      })

    },

    logout: function(){
      djangoAuth.logout().then(function(res){
        $location.path('/login')
      })
    },

    signup: function(user){
        djangoAuth.register(user.username,(password1 = 123456), (password2 = 123456) ).then(function (response){
          console.log(response.key)
          $localStorage.token = response.key
          $state.go('tab.dash')


        })


    },

  
    populateFavs:function(){
      return $http.get('http://localhost:8000/api/feeds/favorite/').then(function(response){  
      console.log('Popuating favs', response.data)
      $localStorage.favs = response.data
      console.log('favs', $localStorage.favs)
      
      })

    },

    deleteFavs: function( index, favorite){

      return $http.delete('http://localhost:8000/api/feeds/updatefavorite/' + favorite.id).then(function (response){
        $localStorage.favs.splice(index, 1)
        console.log('deleted', favorite)
      }, function(response){console.log ('Couldnt delete', response.data)} )
    },

    addFavs: function(news){
      
        return $http.post('http://localhost:8000/api/feeds/favorite/', {fav_id: news.id, title: news.title, link:news.link, time:news.time, image:news.image, source:news.source} ).then(function(){
        favs.favorites.unshift(news)
        // favs.populateFavs()
        console.log(favs.favorites)
     favs.count ++;
  
      }, function(response){
        console.log("Error", $localStorage.token)
      })      
 },
    
    favcount: function(){
      return favs.count;
    },

    states: function(main){
      return $http.post('http://localhost:8000/api/feeds/state/', {state: main})
    }


  }

  return favs

})









