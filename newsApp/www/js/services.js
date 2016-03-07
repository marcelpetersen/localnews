angular.module('starter.services', ['angularMoment'])

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

.factory('FavSrvc', function($http){

  var favs = {
    favorites: [],
    count: 0,

    getFavs: function (){
      return $http.get('http://localhost:8000/api/feeds/favorite/').then(function(response){
        console.log('gotten Favorites')
        favs.favorites = favs.favorites.concat(response.data)
      })
    },

    deleteFavs: function(favorite){
      return http.delete('http://localhost:8000/api/feeds/updafavorite/', favorite.id).then(function (response){
        console.log('deleted', favorie)
      }, function(response){console.log ('Couldnt delete', response.data)} )
    },

    addFavs: function(news){
      return $http.post('http://localhost:8000/api/feeds/favorite/', news).then(function(response){
        favs.favorites = favs.favorites.concat(news);
        favs.count ++;
        favs.getFavs()
      }, function(response){
        console.log("Error")
      })

      
    
      console.log(favs.favorites, favs.count)
 },
    favcount: function(){
      return favs.count;
    }


  }

  return favs
})









