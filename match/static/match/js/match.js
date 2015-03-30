angular.module("matchApp", ["ngRoute", "ngResource"])
    .config(["$httpProvider", "$routeProvider", "$resourceProvider",
            function($httpProvider, $routeProvider, $resourceProvider) {
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
                
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    .controller("MatchController", ["$scope", "$http", "$routeParams", "Group",
            function ($scope, $http, $routeParams, Group) {
        $scope.selectedGroupId = -1;
        if ($routeParams.group_id != null) {
            $scope.selectedGroupId = parseInt($routeParams.group_id);
        }
        $scope.groups = [];
        $scope.selectedGroup = null;
        $scope.selectedResults = null;
        $scope.message = null;
        
        $scope.refresh = function() {
            Group.get({}, function(data) {
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
            var newGroup = new Group({
                name: $scope.add_group_name,
                people: []
            });
            newGroup.$save(function() {
                $scope.refresh();
            });
        };
        
        $scope.runMatch = function() {
            var group = Group.get({group_id: $scope.selectedGroup.id}, function() {
                group.$run_match(function() {
                    $scope.refresh();
                })
            });
        };
        
        $scope.refresh();
    }])
    .controller("GroupController", ["$scope", "Group", "$routeParams", 
            function ($scope, Group, $routeParams) {
        $scope.group_id = $routeParams.group_id;
        $scope.members = [];
        Group.get({group_id:$scope.group_id}, function(result) {
                $scope.members = result.people;
        });
            
    }])
    .factory("Group", ["$resource", function($resource) {
            return $resource("/match/rest/groups/:group_id/", {group_id:"@id"}, 
            {
                run_match: {
                    method: "POST",
                    url: "/match/rest/groups/:group_id/run_match/"
                }
            });
    }]);
