var myappControllers = angular.module('myappControllers', []);

myappControllers.controller("userController", function($scope, $http) {
  var url="data/data.txt";
    $http.get(url).success( function(response)
      {$scope.users = response;});
  });

myappControllers.controller("tableController", function($scope, $http) {
  var url2="data/tabledata.json";
    $http.get(url2).success( function(response)
      {$scope.users = response;});
  });


myappControllers.controller('MyController', function($scope, $http) {
       $scope.myForm = {};
       $scope.myForm.name = "Jakob Jenkov";
       $scope.myForm.car  = "nissan";

     $scope.myForm.submitTheForm1 = function(item, event) {
       console.log("--> Submitting form");
       var dataObject = {
          name : $scope.myForm.name
          ,phone  : $scope.myForm.phoneNo
          ,partySize  : $scope.myForm.partySize
          ,notes  :  $scope.myForm.notes
          ,quote : $scope.myForm.quote
       };

       var responsePromise1 = $http.post("data/writedata2.json", dataObject, {});
       responsePromise1.success(function(dataFromServer, status, headers, config) {
          console.log(dataFromServer.title);
       });
        responsePromise1.error(function(data, status, headers, config) {
          alert("Submitting form failed!");
       });
     }

     $scope.myForm.submitTheForm2 = function(item, event) {
       console.log("--> Submitting form");
       var dataObject = {
          name : $scope.myForm.name
          ,phone  : $scope.myForm.phoneNo
          ,partySize  : $scope.myForm.partySize
          ,notes  :  $scope.myForm.notes
       };

       var responsePromise2 = $http.post("data/writedata2.json", dataObject, {});
       responsePromise.success(function(dataFromServer, status, headers, config) {
          console.log(dataFromServer.title);
       });
        responsePromise2.error(function(data, status, headers, config) {
          alert("Submitting form failed!");
       });
     }

  });

