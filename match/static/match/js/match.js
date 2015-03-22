angular.module("matchApp", [])
    .config(function($httpProvider) {
         $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    })
    .controller("MatchController", ["$scope", "$http", function ($scope, $http) {
        $scope.groups = [];
        $scope.selectedGroup = null;
        $scope.selectedResults = null;
        
        $scope.refresh = function() {
            $http.get("/match/rest/groups").success(function(data) {
               $scope.groups = data.results;
               if ($scope.groups.length > 0) {
                   $scope.selectedGroup = $scope.groups[0];
                   $scope.fetchGroupLatestResults();
               }
            });
        };
        
        $scope.fetchGroupLatestResults = function() {
            if ($scope.selectedGroup.results.length > 0) {
                var groupResults = $scope.selectedGroup.results;
                var lastResults = groupResults[groupResults.length-1];
                $http.get(lastResults).success(function(lastData) {
                    $scope.selectedResults = lastData;
                })
            }
        }
        
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
