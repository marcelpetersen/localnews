angular.module('main', ['ui.router', 'ui.bootstrap'])
.config(function($stateProvider, $urlRouterProvider){
	$urlRouterProvider.otherwise('/');

	$stateProvider
		.state('home', {
			url: '/',
			templateUrl: 'static/partials/home.html'
		})

		.state('privacy',{
			url: '/privacy',
			templateUrl: 'static/partials/privacy.html'
		})

		.state('contact',{
			'url': '/support',
			templateUrl:'static/partials/contact.html',
			controller: 'Mail'
		})


})

.factory('Factory', ['$http', function($http){
	var serve = {

		send_email: function(email){
			return $http.post('http://polar-spire-13485.herokuapp.com/api/feeds/email/', {email:email.email, subject: email.subject, message:email.message})
		
		}

	}
	return serve
}])

.controller('Mail', ['$scope', '$http', '$uibModal','Factory', '$location', function($scope, $http, $uibModal, Factory, $location){
	$scope.submit = function(email){
		

		Factory.send_email(email).then(function(res){
			
			$uibModal.open({
      animation: $scope.animationsEnabled,
      template: '<div> <p class = "lead padding">Mail Sent, We\'ll be in Touch. Thanks </p> </div>',
      controller: 'Mail',
      closed: $location.path('/'),
      
      size: 'sm',
    
    })
		})		
	}






}])

