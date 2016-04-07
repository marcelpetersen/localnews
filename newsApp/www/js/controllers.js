angular.module('starter.controllers', ['ionic','angularMoment', 'angularDjangoRegistrationAuthApp', 'google.places'])
    .constant('$ionicLoadingConfig',{
      template: '<ion-spinner> </ion-spinner>',
      noBackdrop: true,


    })
    .controller('MainCtrl', function ($scope, newsSrvc, $state, $cordovaInAppBrowser, $ionicPlatform, moment, FavSrvc, $localStorage, $rootScope, $ionicLoading){
    $ionicPlatform.ready(function(){
      var options ={
        location:'no',
        clearcache:'yes',
        toolbar: 'yes',
        closebuttoncaption: '<button class="button button-royal">Done</button>'
      };

      $scope.openBrowser = function(link){
        $cordovaInAppBrowser.open(link.link, '_blank', options)
        .then(function(event){

        })
        .catch(function(event){
        });   
      }
    })


      var loading = function(){
         $ionicLoading.show();
      } 
      loading()

        newsSrvc.all().then(function(){
          $scope.main = newsSrvc.feeds;
          $ionicLoading.hide()
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
      } 

      $scope.addFavorites = function(news){
        FavSrvc.addFavs(news).then(function(){
          $rootScope.$emit("refresh", {})
        })

      };

      $scope.share = function(news){
        window.plugins.socialsharing.share('via Just Local News App: '+ news.title, null, null, news.link)

      }        
})


  .controller('SourceCtrl', function($scope, FavSrvc, newsSrvc, $localStorage, $rootScope, $ionicLoading){
        $scope.checkvalue = {}
        $ionicLoading.show()
     var intiSources = function(){ newsSrvc.getSources().then(function(){
          $scope.sources = newsSrvc.sources
          angular.forEach($scope.sources, function(source){
            var present = $localStorage.exclude.indexOf(source.source)

            if (present === -1){
              source.checkvalue =true;}
              else {
                source.checkvalue = false;
              }
          })
          $ionicLoading.hide()
        });
   }  
          intiSources()
          $rootScope.$on("intiSources", function(){
            intiSources();
          })

        $scope.look = function(checkvalue, some){
          newsSrvc.filter(checkvalue, some.source)
        }
      
 })

 .controller('FavoritesCtrl', function($scope,FavSrvc, $localStorage, $rootScope, $ionicLoading, $ionicPlatform, $cordovaInAppBrowser){
  $ionicPlatform.ready(function(){
      var options ={
        location:'no',
        clearcache:'yes',
        toolbar: 'yes',
        closebuttoncaption: '<button class="button button-royal">Done</button>'
      };

      $scope.openBrowser = function(link){
        $cordovaInAppBrowser.open(link.link, '_blank', options)
        .then(function(event){
        })
        .catch(function(event){
          console.log("error")

        });   
      }
    })
      $ionicLoading.show()
      var init = function(){ 
      FavSrvc.populateFavs().then(function(){
        $scope.favorites = $localStorage.favs
              $ionicLoading.hide()

      })}

      init();

      $rootScope.$on("refresh", function(){
        init()
      })

      $scope.favDelete = function($index, favorite){
          FavSrvc.deleteFavs($index, favorite).then(function(){
           // $scope.favorites = FavSrvc.favorites
           })
      }

        $scope.share = function(news){
        window.plugins.socialsharing.share(('via Just Local News App: '+ news.title), null, null, news.link)
      }


      })


.controller('TabCtrl', function($scope, $state, $window, FavSrvc){
       
        
      $scope.favcount = FavSrvc.favcount

      $scope.onTabSelected = function(){
        
      FavSrvc.count = 0;
      } 
      

      })

.controller('SettingsCtrl', function($scope, FavSrvc, $ionicPopup, SettingsSrvc, $ionicPlatform, $window){

    $scope.logout = function(){
      FavSrvc.logout()
    }

    $scope.showPopup = function() {
        $scope.send = {};

        // An elaborate, custom popup
        var myPopup = $ionicPopup.show({
          templateUrl: 'templates/partials/suggest.html',
          title: 'Missing A Source Around You?',
          subTitle: 'Please let us know below',
          cssClass:'custom',
          scope: $scope,
          buttons: [
            { text: 'Cancel',
              type: 'button-assertive'},
            {
              text: '<b>Send</b>',
              type: 'button-energized',
              onTap: function() {
                SettingsSrvc.suggestion($scope.send.name, $scope.send.link, $scope.send.location)
                }
              }   
          ]
        });
      }

       $scope.popUp = function() {
   var alertPopup = $ionicPopup.alert({
     title: 'Version 1.0.0',
     // template: 'Built With Love, By Fizzle :)'
   });

 };




$ionicPlatform.ready(function(){
      $scope.report = function(){
        window.plugins.socialsharing.shareViaEmail(
            '', 
            'Bug Report',
            ['felix@studentpay.co'], 
            null, // CC: must be null or an array
            null, // BCC: must be null or an array
            null // FILES: can be null, a string, or an array
            );
      }
    })

      $scope.rateApp = function () {
          if (ionic.Platform.isIOS()) {
              $window.open('https://itunes.apple.com/us/app/just-local-news/id1100162952?ls=1&mt=8'); // or itms://
          } else if (ionic.Platform.isAndroid()){
              $window.open('market://details?id=com.fizzle.localnews');
          }
      }


      $scope.shareApp = function(){
        window.plugins.socialsharing.share('Get the Just Local News App, If it\'s happening around you, find out on Local News App', null, null, null)

      }

      })

.controller('SplashCtrl', function($scope, $state, FavSrvc, $ionicPlatform, $cordovaDevice, $localStorage){
    
      $scope.place = null;
      $scope.autocompleteOptions = {
        componentRestrictions:{country: 'us'},
        types: ['(cities)']
      }
    

    $scope.getState = function(state){
      var value = state.formatted_address.split(', ');
      var main = value[1].substring(0,2)
      var city = state.formatted_address
      FavSrvc.states(main, state).then(function(){
        $state.go('tab.dash')

      })
    }


    $ionicPlatform.ready(function() {
         FavSrvc.username().then(function(res){
            FavSrvc.signup(res)
          })

    });

    })


.controller('LocationCtrl', function($scope,$timeout, $ionicPlatform, $ionicPopover, FavSrvc, $state, SettingsSrvc, $localStorage, $rootScope, $ionicLoading){
    $ionicPlatform.ready(function(){
       $ionicPopover.fromTemplateUrl('templates/partials/locationpopover.html', {
        scope: $scope
      }).then(function(popover) {
        $scope.popover = popover;
      });


      $scope.openPopover = function($event) {
        $scope.popover.show($event);
      };
      $scope.closePopover = function() {
        $scope.popover.hide();
      };
        })


var init = function(){
    SettingsSrvc.cities().then(function(){
      $scope.locations = $localStorage.city       // $scope.safeApply()
      $ionicLoading.hide()

    })
  }

    init();
     $ionicLoading.show()

      $scope.place = null;
      $scope.autocompleteOptions ={
        componentRestrictions:{country: 'us'},
        types: ['(cities)']
      }

       $scope.getState = function(state){
        $ionicLoading.show()
      var value = state.formatted_address.split(', ');
      var main = value[1].substring(0,2)
      var city = state.formatted_address
      FavSrvc.states(main, state).then(function(){
       init(); 
             $ionicLoading.hide()

      $rootScope.$emit("intiSources", {}) 
      })
    }

      $scope.delete = function(index, state){
        SettingsSrvc.removeLocation(index, state).then(function(){
          $rootScope.$emit("intiSources", {}) 
        })
      }
})

.controller('PrivacyCtrl', function($scope){
  

})



      






