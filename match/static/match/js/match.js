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
        $scope.group_view = {
            message: null,
            selectedGroup: null,
            selectedGroupId: -1,
            selectedResults: null,
            viewName: "group"
        };
        $scope.admin = {
            alerts: [],
            selectedGroup: null,
            selectedGroupId: -1,
            selectedResults: null,
            viewName: "admin"
        };
        $scope.register = {
            alerts: []
        };
        $scope.current_user = {
            user: null,
            member_groups: [],
            owner_groups: []
        };
        
        if ($routeParams.group_id != null) {
            $scope.group_view.selectedGroupId = parseInt($routeParams.group_id);
            $scope.admin.selectedGroupId = parseInt($routeParams.group_id);
        }
        $scope.groups = [];

        $scope.selectGroupById = function(container, groups) {
            container.selectedGroup = null;

            if (container.selectedGroupId >= 0) {
                // Try to find the same selected group and update with latest results
                for (var i = 0; i < groups.length; i++) {
                    if (container.selectedGroupId === groups[i].id) {
                        container.selectedGroup = groups[i];
                        break;
                    }
                }
            }
            if (container.selectedGroup === null) {
                // No group selected
                // Initialize with the first group
                if (groups.length > 0) {
                    container.selectedGroup = groups[0];
                }
            }
        }
        
        $scope.refresh = function() {
            $http.get('current_user')
                .success(function(data, status, headers, config) {
                    var id = data.id;
                    Person.get({person_id: id}, function(data, status, headers, config) {
                        $scope.current_user.user = data;
                    })
                }
            );
            $http.get('member_groups')
                .success(function(data, status, headers, config) {
                    $scope.current_user.member_groups = data;
                    $scope.selectGroupById($scope.group_view, $scope.current_user.member_groups);
                }
            );
            $http.get('owner_groups')
                .success(function(data, status, headers, config) {
                    $scope.current_user.owner_groups = data;
                    $scope.selectGroupById($scope.admin, $scope.current_user.owner_groups);
                }
            );
            Group.get({}, function(data) {
                $scope.groups = data.results;
            });
        };
        
        $scope.addUser = function() {
            Group.get({group_id: $scope.register.add_person_group.id}, function(data, status, headers, config) {
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
        
        $scope.removeUserFromGroup = function(index) {
            var selectedGroup = $scope.current_user.member_groups[index];
            Group.get({group_id: selectedGroup.id}, function(data, status, headers, config) {
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
            newGroup.people = []
            newGroup.latest_matches = []
            Group.save(newGroup, function(savedGroup) {
                // Success
                $scope.admin.alerts = [{
                    type:"success",
                    message:"Added group " + savedGroup.name
                }];
                $scope.admin.add_group_name = "";
                Group.get({group_id: savedGroup.id}, function(data, status, headers, config) {
                    $log.debug("adding to group: " + savedGroup);
                    data.$add_user(function() {
                        $scope.admin.alerts.push({
                            type:"success",
                            message: "User added"
                        });
                        $scope.refresh();
                    });
                });
            }, function(data) {
                // Failure
                $scope.admin.alerts = [{
                        type: "failure",
                        message: "Group failed to be added.  data=" +
                                data.data + ", status=" + data.status
                }];
            });
        };
        
        $scope.removeGroup = function(index) {
            var group = $scope.current_user.owner_groups[index];
            $log.debug("removing group " + group.ame);
            Group.get({group_id:group.id}, function(data) {
                data.$delete();
                $scope.refresh();
            });
        }
        
        $scope.closeAdminMsg = function() {
            $scope.admin.alerts = [];
        };
        
        $scope.clearGroupResultsForMyGroup = function(index) {
            // Run the match for a group you own
            $scope.clearGroupResults($scope.current_user.owner_groups[index]);
        };

        $scope.clearGroupResults = function(group) {
            Group.clear_results({group_id:group.id}, function(data) {
                $scope.admin.alerts = [{
                        type: "success",
                        message: "Results cleared for group: " + group.name
                }];
                $scope.refresh()
            });
        };
        
        $scope.runMatchForMyGroup = function(index) {
            // Run the match for a group you own
            $scope.runMatch($scope.current_user.owner_groups[index]);
        };
        
        $scope.runMatch = function(group) {
            $scope.admin.alerts = [{
                    type: "success",
                    message: "Calculating matches.."
            }];
            $log.debug("running matches for group: " + group.name);
            Group.get({group_id: group.id}, function(data) {
                data.$run_match(function() {
                    $scope.admin.alerts = [{
                            type: "success",
                            message: "Matches made for " + group.name
                    }];
                    $scope.admin.selectedGroupId = group.id
                    $scope.refresh();
                });
            });
        };
        
        $scope.refresh();
    }])
    .controller("GroupController", ["$scope", "Group", "Person", "$routeParams", "$log",
            function ($scope, Group, Person, $routeParams, $log) {
        $scope.group_id = $routeParams.group_id;
        $scope.group = null;
        $scope.people = [];
        $scope.addable_people = [];
        $scope.refresh = function() {
            Group.get({group_id:$scope.group_id}, function(data) {
                $scope.group = data
                Person.list({}, function(data) {
                    $scope.people = data.results
                    let group_people_ids = new Set();
                    for (let i = 0; i < $scope.group.people.length; i++) {
                        group_people_ids.add($scope.group.people[i].id);
                    }
                    $scope.addable_people = []
                    $log.info($scope.group.people);
                    for (let i = 0; i < $scope.people.length; i++) {
                        if (!group_people_ids.has($scope.people[i].id)) {
                            $scope.addable_people.push($scope.people[i])
                        }
                    }
                });
            });
        };

        $scope.add_person = function(person_id) {
            Group.get({group_id: $scope.group.id}, function(data) {
                data.$add_person({person_id: person_id}, function() {
                    $scope.refresh();
                });
            });
        };
        $scope.remove_person = function(person_id) {
            Group.get({group_id: $scope.group.id}, function(data) {
                data.$remove_person({person_id: person_id}, function() {
                    $scope.refresh();
                });
            });
        }

        $scope.refresh();
    }])
    .factory("Group", ["$resource", function($resource) {
            return $resource("/match/rest/groups/:group_id/", {group_id:"@id"}, 
            {
                get: {
                    method: "GET",
                    url: "/match/rest/groups/:group_id"
                },
                run_match: {
                    method: "POST",
                    url: "/match/rest/groups/:group_id/run_match/"
                },
                add_user: {
                    method: "POST",
                    url: "/match/rest/groups/:group_id/add_user/"
                },
                add_person: {
                    method: "POST",
                    url: "/match/rest/groups/:group_id/add_person/"
                },
                remove_person: {
                    method: "POST",
                    url: "/match/rest/groups/:group_id/remove_person/"
                },
                remove_user_from_group: {
                    method: "POST",
                    url: "/match/rest/groups/:group_id/remove_user_from_group/"
                },
                clear_results: {
                    method: "DELETE",
                    url: "/match/rest/groups/:group_id/clear_results/"
                }
            });
    }])
    .factory("Person", ["$resource", function($resource) {
            return $resource("/match/rest/people/:person_id/", {person_id:"@id"},
            {
                list: {
                    method: "GET",
                    url: "/match/rest/people/"
                }
            });
    }]);
