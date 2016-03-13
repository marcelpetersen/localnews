angular.module('starter.services', ['angularMoment', 'angular-jwt', 'angularDjangoRegistrationAuthApp'])

// .factory('httpRequestInterceptor', function ($localStorage) {
//   return {
//     request: function (config) {

//       // use this to destroying other existing headers
//       // config.headers = {'Authentication':'authentication'}

//       // use this to prevent destroying other existing headers
//       // var token = $localstorage.get('token')
//       config.headers['Authorization'] = 'Token ' + $localStorage.token;

//       return config;
//     }
//   };
// })

// .config(function ($httpProvider) {
//   $httpProvider.interceptors.push('httpRequestInterceptor');
// })

.factory ('newsSrvc', function ($http, BASE_URL){

  

  var news  = {

    feeds: [],
    next : [],
    sources:[],
    exclude: [],



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

.factory('FavSrvc', function($http, djangoAuth, $location, $localStorage){


  var favs = {


    // username: false,
    token: [],
    favorites: [],
    count: 0,

    // setsession: function(token){
     

    //   $localstorage.set('user', token: favs.token)
    // },


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
        return $http.post('http://localhost:8000/api/feeds/users/', {username: user.username, password:user.password} ).then(function(response){
          console.log(response.data)
        })


    },

    // verify: function(user){
    //   return $http.post('http://localhost:8000/api-token-verify', $localstorage.get('token')).then(function(response){
    //     console.log(response)
    //   }, function(response){
    //     console.log('error', response)
    //   })
    // },
    populateFavs:function(){
      return $http.get('http://localhost:8000/api/feeds/favorite/').then(function(response){
        favs.favorites = response.data
      $localStorage.favs = favs.favorites;
      console.log($localStorage.favs)
      
      })

    },

    getFavs: function (){

      return $localStorage.favs
      
      
    },

    deleteFavs: function( index, favorite){

      var jump = indexOf(favorite.title)
      if (title > -1)

      return $http.delete('http://localhost:8000/api/feeds/updatefavorite/' + favorite.id).then(function (response){
        favs.favorites.splice(index, 1)
        console.log('deleted', favorite)
        // favs.getFavs()
      }, function(response){console.log ('Couldnt delete', response.data)} )
    },

    addFavs: function(news){
        
      return $http.post('http://localhost:8000/api/feeds/favorite/', 
        { pk: news.id, title:news.title, link: news.link, time: news.time, image:news.image, source:news.source}).then(function(){
        $localStorage.favs.unshift(news)
        console.log($localStorage.favs)
        // favs.getFavs()

        
        favs.count ++;
  
      }, function(response){
        console.log("Error", $localStorage.token)

      })
 },
    favcount: function(){
      return favs.count;
    }


  }

  return favs
})









