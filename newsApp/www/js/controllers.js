angular.module('starter.controllers', ['ionic','angularMoment'])

    .controller('MainCtrl', function ($scope, newsSrvc, $state, $cordovaInAppBrowser, $ionicPlatform, moment, FavSrvc){
    $ionicPlatform.ready(function(){
      var options ={
        location:'yes',
        clearcache:'yes',
        toolbar: 'yes',
        closebuttoncaption: '<button class="button button-royal">Done</button>'
      };

      $scope.openBrowser = function(link){
        $cordovaInAppBrowser.open(link, '_self', options)
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
        
      }  


        
})


    .controller('SourceCtrl', function($scope, newsSrvc){
        newsSrvc.getSources().then(function(){
          $scope.sources = newsSrvc.sources
        });

        
        $scope.checkvalue = 'add';

        $scope.look = function(checkvalue, some){
          newsSrvc.filter(checkvalue, some)
        }
        


 })

    .controller('FavoritesCtrl', function($scope, FavSrvc){

      

      })


     .controller('TabCtrl', function($scope, FavSrvc){
        FavSrvc.getFavs().then(function(){
          $scope.favorites = FavSrvc.favorites
        })
        
        $scope.favcount = FavSrvc.favcount

        $scope.onTabSelected = function(){
        FavSrvc.count = 0;
        console.log("Entered")
        
      } 
      

      })





