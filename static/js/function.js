var app = angular.module("app", []);

app.controller("AppCtrl", function($http) {
    var app = this;
    addUsersUrl="";
    removeUsersUrl="";
    usersUrl="/static/data/data.txt";



    $http.get(usersUrl)
      .success(function(data) {
        app.users = data;
      })

    app.addUser = function(person) {
        $http.post(addUserUrl, person)
          .success(function(data) {
            app.users = data;
          })
    }

    app.removeUser= function(person) {
        $http.post(removeUserUrl, person)
          .success(function(data) {
            app.users = data;
          })
    }
    addTablesUrl="";
    removeTablesrl="";
    tablesUrl="/static/data/tabledata.json";



    $http.get(tablesUrl)
      .success(function(data) {
        app.tables = data;
      })

    app.addTable = function(person) {
        $http.post(addTableUrl, person)
          .success(function(data) {
            app.tables = data;
          })
    }

    app.removeTable = function(person) {
        $http.post(removeTableUrl, person)
          .success(function(data) {
            app.tables = data;
          })
    }
})