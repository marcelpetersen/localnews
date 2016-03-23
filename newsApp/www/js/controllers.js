angular.module('starter.controllers', ['ionic','angularMoment', 'angularDjangoRegistrationAuthApp', 'google.places'])

    .controller('MainCtrl', function ($scope, newsSrvc, $state, $cordovaInAppBrowser, $ionicPlatform, moment, FavSrvc, $localStorage, $rootScope){
    $ionicPlatform.ready(function(){
      var options ={
        location:'no',
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
        FavSrvc.addFavs(news).then(function(){
          $rootScope.$emit("refresh", {})
        })

      };

      $scope.share = function(news){
        console.log(news.link)
        console.log(news.title)
        window.plugins.socialsharing.share('via LocalNews App: '+ news.title, null, null, news.link)

      }




        
})


  .controller('SourceCtrl', function($scope, FavSrvc, newsSrvc, $localStorage, $rootScope){
        $scope.checkvalue = {}

     var intiSources = function(){ newsSrvc.getSources().then(function(){
          $scope.sources = newsSrvc.sources
          angular.forEach($scope.sources, function(source){
            var present = $localStorage.exclude.indexOf(source.source)
            console.log(source.source)

            console.log(present)
            if (present === -1){
              source.checkvalue =true;}
              else {
                source.checkvalue = false;
              }
              console.log($localStorage.exclude)
          })
        });
   }  
          intiSources()
          $rootScope.$on("intiSources", function(){
            intiSources();
            console.log("intiSources")
          })

        $scope.look = function(checkvalue, some){
          console.log(checkvalue, some.source)
          newsSrvc.filter(checkvalue, some.source)
        }

        


        
 })

 .controller('FavoritesCtrl', function($scope,FavSrvc, $localStorage, $rootScope){

      var init = function(){ 
      FavSrvc.populateFavs().then(function(){
        $scope.favorites = $localStorage.favs
      })}

      init();

      $rootScope.$on("refresh", function(){
        init()
        console.log("emitted")
      })

      // $scope.favorites = $localStorage.favs

      $scope.favDelete = function($index, favorite){
          FavSrvc.deleteFavs($index, favorite).then(function(){
           // $scope.favorites = FavSrvc.favorites
          
          console.log(favorite); })
      }

        $scope.share = function(news){
        console.log(news.link)
        console.log(news.title)
        window.plugins.socialsharing.share(('via LocalNews App: '+ news.title), null, null, news.link)
      }


      })


.controller('TabCtrl', function($scope, $state, $window, FavSrvc){
       
        
      $scope.favcount = FavSrvc.favcount

      $scope.onTabSelected = function(){
        
      FavSrvc.count = 0;
      console.log("Entered")
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
          title: 'Missing a Source Around You?',
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
                console.log($scope.send.name)
                console.log($scope.send.link)

                SettingsSrvc.suggestion($scope.send.name, $scope.send.link, $scope.send.location)
                }
              }   
          ]
        });
      }

$ionicPlatform.ready(function(){
      $scope.report = function(){
        window.plugins.socialsharing.shareViaEmail(
            'Message', 
            'Bug Report',
            ['felix@studentpay.co'], 
            null, // CC: must be null or an array
            null, // BCC: must be null or an array
            null // FILES: can be null, a string, or an array
            );
      }
    })

      $scope.rateApp = function () {
        console.log("rating waiting")
          if (ionic.Platform.isIOS()) {
              $window.open('itms-apps://itunes.apple.com/us/app/domainsicle-domain-name-search/id511364723?ls=1&mt=8'); // or itms://
          } else if (ionic.Platform.isAndroid()){
              $window.open('market://details?id=<package_name>');
          }
      }


      $scope.shareApp = function(){
        window.plugins.socialsharing.share('Get the Local News app, If it\'s happening around you, find out on Local News App', null, null, null)

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
      console.log(main)
      console.log(state.formatted_address)
      FavSrvc.states(main, state).then(function(){
        $state.go('tab.dash')

      })
    }


    $ionicPlatform.ready(function() {
         FavSrvc.username().then(function(res){
            console.log(res)
            FavSrvc.signup(res)
          })

    });

    })


.controller('LocationCtrl', function($scope,$timeout, $ionicPlatform, $ionicPopover, FavSrvc, $state, SettingsSrvc, $localStorage, $rootScope){
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
    })
  }

    init();
  

  
    

      $scope.place = null;
      $scope.autocompleteOptions ={
        componentRestrictions:{country: 'us'},
        types: ['(cities)']
      }

       $scope.getState = function(state){
      var value = state.formatted_address.split(', ');
      var main = value[1].substring(0,2)
      var city = state.formatted_address
      console.log(main)
      console.log(state.formatted_address)
      FavSrvc.states(main, state).then(function(){
       init(); 
      $rootScope.$emit("intiSources", {})  
        console.log("trynidngdfl")
      })
    }

      $scope.delete = function(index, state){
        SettingsSrvc.removeLocation(index, state).then(function(){
          $rootScope.$emit("intiSources", {}) 
        })
      }












})



      






