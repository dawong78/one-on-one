angular.module("matchApp", [])
    .config(function($httpProvider) {
         $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    })
    .controller("MatchController", ["$scope", "$http", function ($scope, $http) {
        $scope.groups = [];
        $scope.selectedGroup = null;
        
        $scope.refresh = function() {
            $http.get("/match/groups").success(function(data) {
               $scope.groups = data;
               if (data.length > 0) {
                   $scope.selectedGroup = $scope.groups[0];
               }
            });
        };

        $scope.addUser = function() {
            var params = { 
                name: $scope.add_person_name,
                email: $scope.add_person_email,
            }
            $http.post("/match/add_user", params)
                    .success(function(results) {
                $scope.add_person_results = "User added";
                $scope.refresh()
            });
        };
        
        $scope.refresh()
    }]);
