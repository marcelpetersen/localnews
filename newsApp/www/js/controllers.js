angular.module('starter.controllers', ['ionic','angularMoment', 'angularDjangoRegistrationAuthApp', 'google.places'])

    .controller('MainCtrl', function ($scope, newsSrvc, $state, $cordovaInAppBrowser, $ionicPlatform, moment, FavSrvc, $localStorage){
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
      };

      $scope.share = function(news){
        console.log(news.link)
        console.log(news.title)
        window.plugins.socialsharing.share(('via LocalNews App: '+ news.title), null, null, news.link)


      }




        
})


  .controller('SourceCtrl', function($scope, FavSrvc, newsSrvc, $localStorage){
        $scope.checkvalue = {}
        newsSrvc.getSources().then(function(){
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
        var array = ['local', 'smokal', 'okal']
        var weak = array.indexOf('local')
        console.log (weak)

        $scope.look = function(checkvalue, some){
          console.log(checkvalue, some.source)
          newsSrvc.filter(checkvalue, some.source)
        }

        


        
 })

 .controller('FavoritesCtrl', function($scope,FavSrvc, $localStorage){

       
      FavSrvc.populateFavs().then(function(){
        $scope.favorites = $localStorage.favs
      })

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
            'Subject',
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
       $scope.result2 = '';
    $scope.options2 = {
      country: 'ca',
      types: '(cities)'
    };    $scope.details2 = '';
    

    $scope.restrictState = function(state){

      $scope.place = null;
      $scope.autocompleteOptions ={
        componentRestrictions:{country: 'us'},
        types: ['cities']
      }
    };

    $scope.getState = function(state){
      var value = state.formatted_address.split(', ');
      var main = value[1]
      var city = state.formatted_address
      console.log(main)
      console.log(state.formatted_address)
      FavSrvc.states(main, city).then(function(){
        $state.go('tab.dash')

      })
    }


    $ionicPlatform.ready(function() {
      if(ionic.Platform.isAndroid()){
        // var num = Math.floor(Math.random() * 12000000)
        var UUID = $cordovaDevice.getUUID();
        console.log("UUID", UUID)
        // var result = UUID + num
        // console.log('iosID' + UUID)
        // console.log(result)
        var shaUser = new jsSHA("SHA-1", "TEXT");
        shaUser.update(UUID);
        var hash = shaUser.getHash("HEX");
        console.log(hash)
        FavSrvc.signup(hash)
        
        }else{
        console.log("Is not Android");
        var result= "878dsdiofjg"
        console.log(result)
        var shaUser = new jsSHA("SHA-1", "TEXT");
        shaUser.update(result);
        var hash = shaUser.getHash("HEX");
        console.log(hash)
        FavSrvc.signup(hash)
        
      };
      $localStorage.exclude = []
    });

    })


.controller('LocationCtrl', function($scope, $ionicPlatform, $ionicPopover, FavSrvc, $state, SettingsSrvc, $localStorage){
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



    SettingsSrvc.cities().then(function(){
      $scope.locations = $localStorage.city
    })
    $scope.locations = SettingsSrvc.addedLocations()

    
    $scope.restState = function(state){

      $scope.place = null;
      $scope.autocompleteOptions ={
        componentRestrictions:{country: 'us'},
        types: ['cities']
      }
    };

      $scope.getState = function(state){
      var value = state.formatted_address.split(', ');
      var main = value[1]
      var city = state.formatted_address
      console.log(main)
      console.log(state.formatted_address)
      FavSrvc.states(main, city).then(function(){
        console.log($localStorage.city)
        $state.reload()
      })
    }

      $scope.delete = function(index, state){
        SettingsSrvc.removeLocation(index, state).then(function(){
          $state.reload()
        })
      }












})



      






