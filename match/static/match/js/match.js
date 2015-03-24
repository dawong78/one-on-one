angular.module("matchApp", ["ngRoute"])
    .config(["$httpProvider", "$routeProvider", function($httpProvider, $routeProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        
        $routeProvider
                .when("/groups/", {
                    templateUrl: "/static/match/partials/view_group.html",
                    controller: "MatchController"
                })
                .when("/groups/:group_id/", {
                    templateUrl: "/static/match/partials/view_group.html",
                    controller: "MatchController"
                })
                .when("/groups/:group_id/members/", {
                    templateUrl: "/static/match/partials/view_members.html",
                    controller: "GroupController"
                })
                .when("/register_user", {
                    templateUrl: "/static/match/partials/add_user.html",
                    controller: "MatchController"
                })
                .otherwise({
                    redirectTo: "/groups/"
                });
    }])
    .controller("MatchController", ["$scope", "$http", "$routeParams",
            function ($scope, $http, $routeParams) {
        $scope.selectedGroupId = -1;
        if ($routeParams.group_id != null) {
            $scope.selectedGroupId = parseInt($routeParams.group_id);
        }
        $scope.groups = [];
        $scope.selectedGroup = null;
        $scope.selectedResults = null;
        
        $scope.refresh = function() {
            $http.get("/match/rest/groups/").success(function(data) {
                $scope.groups = data.results;
                if ($scope.groups.length > 0) {
                    if ($scope.selectedGroup === null) {
                        if ($scope.selectedGroupId !== null) {
                            // Try to find the requested group.
                            for (var i = 0; i < $scope.groups.length; i++) {
                                if ($scope.selectedGroupId === $scope.groups[i].id) {
                                    $scope.selectedGroup = $scope.groups[i];
                                    break;
                                }
                            }
                        }
                        if ($scope.selectedGroup === null) {
                            // Initialize with the first group
                            $scope.selectedGroup = $scope.groups[0];
                        }
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
                });
            } else {
                $scope.selectedResults = null;
            }
        };
        
        $scope.addUser = function() {
            var params = { 
                name: $scope.add_person_name,
                email: $scope.add_person_email
            };
            $http.post("/match/rest/people/", params)
                    .success(function(results) {
                var params2 = {
                    person_id: results.id
                };
                $http.post("/match/group/" + $scope.add_person_group.id + 
                        "/people/", params2)
                        .success(function(groupResults) {
                    $scope.add_person_results = "User added";
                    $scope.refresh();
                });
            });
        };
        
        $scope.addGroup = function() {
            var params = {
                name: $scope.add_group_name,
                people: []
            };
            $http.post("/match/rest/groups/", params)
                    .success(function(results) {
                $scope.refresh();
            });
        };
        
        $scope.runMatch = function() {
            $http.post("/match/rest/groups/" + $scope.selectedGroup.id + 
                    "/run_match/")
                    .success(function(result) {
                $scope.refresh();
            })
        }
        
        $scope.refresh();
    }])
    .controller("GroupController", ["$scope", "$http", "$routeParams", 
            function ($scope, $http, $routeParams) {
        $scope.group_id = $routeParams.group_id;
        $scope.members = [];
        $http.get("/match/rest/groups/" + $scope.group_id)
                .success(function(result) {
                    $scope.members = result.people;
        })
            
    }]);
