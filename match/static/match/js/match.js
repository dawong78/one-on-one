angular.module("matchApp", [])
    .config(function($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    })
    .controller("MatchController", ["$scope", "$http", function ($scope, $http) {
        $scope.groups = [];
        $scope.selectedGroup = null;
        $scope.selectedResults = null;
        
        $scope.refresh = function() {
            $http.get("/match/rest/groups/").success(function(data) {
                $scope.groups = data.results;
                if ($scope.groups.length > 0) {
                    if ($scope.selectedGroup === null) {
                        // Initialize with the first group
                        $scope.selectedGroup = $scope.groups[0];
                    } else {
                        // Try to find the same selected group.
                        for (var i = 0; i < $scope.groups.length; i++) {
                            if ($scope.selectedGroup.id === $scope.groups[i].id) {
                                $scope.selectedGroup = $scope.groups[i];
                                break;
                            }
                        }
                    }
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
            } else {
                $scope.selectedResults = null;
            }
        }
        
        $scope.addUser = function() {
            var params = { 
                name: $scope.add_person_name,
                email: $scope.add_person_email,
            }
            $http.post("/match/rest/people/", params)
                    .success(function(results) {
                var params2 = {
                    person_id: results.id,
                }
                $http.post("/match/group/" + $scope.add_person_group.id + "/people/", params2)
                        .success(function(groupResults) {
                    $scope.add_person_results = "User added";
                    $scope.refresh();
                });
            });
        };
        
        $scope.refresh()
    }]);
