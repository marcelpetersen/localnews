// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic', 'starter.controllers', 'starter.services', 'ngCordova', 'angularMoment','ngCookies', 'ngStorage' ])

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }

  });
})


.constant ('BASE_URL', 'https://polar-spire-13485.herokuapp.com/api/feeds/')


.config(function($httpProvider, $stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider

  // setup an abstract state for the tabs directive
    .state('tab', {
    url: '/tab',
    abstract: true,
    templateUrl: 'templates/tabs.html',
    controller: 'TabCtrl',
    onEnter: function($state, newsSrvc){
      newsSrvc.checkSession().then(function(session){
        if (!session) $state.go('splash')
      })
    }
  })

  // Each tab has its own nav history stack:
  .state('main', {
    url: '/main',
    templateUrl: 'templates/main.html',
    onEnter: function($state, newsSrvc){
      newsSrvc.checkSession().then(function (session){
        if (session){
          $state.go('tab.dash')}
          else{
            $state.go('splash')
          }
        
      })
    }
  })

  .state('login', {
    url: '/login',
    templateUrl: 'templates/login.html',
    controller: 'LoginCtrl'
})

  .state('splash',{
    url:'/splash',
    templateUrl: 'templates/splash.html',
    controller: 'SplashCtrl',
    onEnter: function($state, newsSrvc){ newsSrvc.checkSession().then(
      function(session){
        if (session) $state.go('tab.dash');
      })
  }
})

  .state('tab.favorites',{
    url: '/favorites',
    views:{
    'tab-favorites':{
      templateUrl: 'templates/favorites.html',
      controller: 'FavoritesCtrl'
       }
     }
  })

  .state('tab.dash', {
    url: '/dash',
    views: {
      'tab-dash': {
        templateUrl: 'templates/tab-dash.html',
        controller: 'MainCtrl'
      }
    }
  })

  .state('tab.chats', {
      url: '/chats',
      views: {
        'tab-chats': {
          templateUrl: 'templates/tab-sources.html',
          controller: 'SourceCtrl'
        }
      }
    })

  .state('tab.account', {
    url: '/account',
    views: {
      'tab-account': {
        templateUrl: 'templates/tab-account.html',
        controller: 'SettingsCtrl'
      }
    }
  })

  .state('tab.location', {
    url: '/account/location',
    views:{
      'tab-account':{
          templateUrl: 'templates/tab-location.html',
          controller: 'LocationCtrl'
        }
      }
  })

  ;

  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/main');


})


