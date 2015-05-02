angular.module("matchApp", ["ngRoute", "ngResource", "ui.bootstrap"])
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
    .controller("MatchController", ["$scope", "$http", "$routeParams", "Group", "Person", "$log",
            function ($scope, $http, $routeParams, Group, Person, $log) {
        $scope.group_view = {};
        $scope.admin = {};
        $scope.register = {user_groups:[]};
        $scope.current_user = {};
        
        $scope.group_view.selectedGroupId = -1;
        if ($routeParams.group_id != null) {
            $scope.group_view.selectedGroupId = parseInt($routeParams.group_id);
        }
        $scope.groups = [];
        $scope.group_view.selectedGroup = null;
        $scope.group_view.selectedResults = null;
        $scope.group_view.message = null;
        
        $scope.refresh = function() {
            $http.get('current_user')
                .success(function(data, status, headers, config) {
                    var id = data.id;
                    Person.get({person_id: id}, function(data, status, headers, config) {
                        $scope.current_user = data;
                    })
                }
            );
            $http.get('user_groups')
                .success(function(data, status, headers, config) {
                    $scope.register.user_groups = data;
                }
            );
            Group.get({}, function(data) {
                $scope.groups = data.results;
                if ($scope.groups.length > 0) {
                    if ($scope.group_view.selectedGroup === null) {
                        if ($scope.group_view.selectedGroupId !== null) {
                            // Try to find the requested group.
                            for (var i = 0; i < $scope.groups.length; i++) {
                                if ($scope.group_view.selectedGroupId === $scope.groups[i].id) {
                                    $scope.group_view.selectedGroup = $scope.groups[i];
                                    break;
                                }
                            }
                        }
                        if ($scope.group_view.selectedGroup === null) {
                            // Initialize with the first group
                            $scope.group_view.selectedGroup = $scope.groups[0];
                        }
                    } else {
                        // Try to find the same selected group.
                        for (var i = 0; i < $scope.groups.length; i++) {
                            if ($scope.group_view.selectedGroup.id === $scope.groups[i].id) {
                                $scope.group_view.selectedGroup = $scope.groups[i];
                                break;
                            }
                        }
                    }
                    $scope.fetchGroupLatestResults();
                }
            });
        };
        
        $scope.fetchGroupLatestResults = function() {
            $log.debug("Fetching results for " + $scope.group_view.selectedGroup.name);
            if ($scope.group_view.selectedGroup.results.length > 0) {
                var groupResults = $scope.group_view.selectedGroup.results;
                var lastResults = groupResults[groupResults.length-1];
                $http.get(lastResults).success(function(lastData) {
                    $scope.group_view.selectedResults = lastData;
                });
            } else {
                $scope.group_view.selectedResults = null;
            }
        };
        
        $scope.addUser = function() {
            Group.get({group_id: $scope.group_view.selectedGroup.id}, function(data, status, headers, config) {
                $log.debug("adding to group: " + data);
                data.$add_user(function() {
                    $scope.register.alerts =  [{
                        type:"success",
                        message: "User added"
                    }];
                    $scope.refresh();
                });
            });
        };
        
        $scope.removeUserFromGroup = function() {
            Group.get({group_id: $scope.group_view.selectedGroup.id}, function(data, status, headers, config) {
                $log.debug("removing from group: " + data);
                data.$remove_user_from_group(function() {
                    $scope.register.alerts = [{
                        type:"success",
                        message:"User removed from group"
                    }];
                    $scope.refresh();
                });
            });
        };
        
        $scope.closeRegisterMsg = function() {
            $scope.register.alerts = [];
        };
        
        $scope.addGroup = function() {
            $log.debug("add group name: " + $scope.admin.add_group_name);
            var newGroup = new Group();
            newGroup.name = $scope.admin.add_group_name;
            newGroup.people = [];
            Group.save(newGroup, function() {
                $scope.admin.alerts = [{
                    type:"success",
                    message:"Added group " + newGroup.name
                }];
                $scope.admin.add_group_name = "";
                $scope.refresh();
            });
        };
        
        $scope.closeAdminMsg = function() {
            $scope.admin.alerts = [];
        }
        
        $scope.runMatch = function() {
            $log.debug("running matches for group: " + $scope.group_view.selectedGroup.name);
            var group = Group.get({group_id: $scope.group_view.selectedGroup.id}, function() {
                group.$run_match(function() {
                    $scope.refresh();
                });
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
                },
                add_user: {
                    method: "POST",
                    url: "/match/rest/groups/:group_id/add_user/"
                },
                remove_user_from_group: {
                    method: "POST",
                    url: "/match/rest/groups/:group_id/remove_user_from_group/"
                }
            });
    }])
    .factory("Person", ["$resource", function($resource) {
            return $resource("/match/rest/people/:person_id/", {person_id:"@id"});
    }]);
