angular.module('starter.controllers', ['ionic','angularMoment', 'angularDjangoRegistrationAuthApp'])

    .controller('MainCtrl', function ($scope, newsSrvc, $state, $cordovaInAppBrowser, $ionicPlatform, moment, FavSrvc){
    $ionicPlatform.ready(function(){
      var options ={
        location:'yes',
        clearcache:'yes',
        toolbar: 'yes',
        closebuttoncaption: '<button class="button button-royal">Done</button>'
      };

      $scope.openBrowser = function(link){
        $cordovaInAppBrowser.open(link, '_blank', options)
        .then(function(event){
          console.log("Browser opened")

        })
        .catch(function(event){
          console.log("error")

        });
        
      }


    })
      

        newsSrvc.all().then(function(){
          $scope.main = newsSrvc.feeds;
        })
      
      $scope.doRefresh = function(){
        newsSrvc.all().then (function(){
          $scope.main = newsSrvc.feeds
        })
        .finally(function(){
          $scope.$broadcast('scroll.refreshComplete');
        })
      }

      $scope.getMore = function(){
        newsSrvc.getNext().then(function(){
          $scope.main = newsSrvc.feeds
        })
        console.log('More Gotten')
      } 

      $scope.addFavorites = function(news){
        console.log (news)
        FavSrvc.addFavs(news)
        // .then (function(){
        //   FavSrvc.getFavs()
        //   $scope.favorites = FavSrvc.favorites
        // })
        
      }  


        
})


  .controller('SourceCtrl', function($scope, FavSrvc, newsSrvc){
        
        newsSrvc.getSources().then(function(){
          $scope.sources = newsSrvc.sources
        });

        
        // $scope.checkvalue = 'add';

        $scope.look = function(checkvalue, some){
          newsSrvc.filter(checkvalue, some)
        }
        


 })

 .controller('FavoritesCtrl', function($scope, FavSrvc, $localStorage){

        
      FavSrvc.populateFavs()
       $scope.favorites = $localStorage.favs

       $scope.favDelete = function($index, favorite){
          FavSrvc.deleteFavs($index, favorite).then(function(){
           // $scope.favorites = FavSrvc.favorites
          
          console.log(favorite); })
      }


      })


.controller('TabCtrl', function($scope, FavSrvc){
       
        
        $scope.favcount = FavSrvc.favcount



        $scope.onTabSelected = function(){
          
          // FavSrvc.getFavs().then(function(){
          //   $scope.favorites = FavSrvc.favorites
          // })
        FavSrvc.count = 0;
        console.log("Entered")
      } 
      

      })

  .controller('LoginCtrl', function($scope, FavSrvc){
    
    $scope.submit = function(user){
      FavSrvc.auth(user)
    }

    $scope.signup = function(user){
      FavSrvc.signup(user)
    }

      })

    .controller('SettingsCtrl', function($scope, FavSrvc){

    $scope.logout = function(){
      FavSrvc.logout()

    }

      })






      






