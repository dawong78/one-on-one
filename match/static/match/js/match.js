angular.module("matchApp", [])
    .controller("MatchController", ["$scope", function ($scope) {
        $scope.groups = [
            {
                name:"group name",
                people:[
                    {name:"name1", email:"email1"},
                    {name:"name2", email:"email2"}
                ],
                matches:[
                    {
                        person1:{name:"name1", email:"email1"},
                        person2:{name:"name2", email:"email2"},
                        person3:{}
                    }
                ]
            }
        ];
        
        $scope.addUser = function () {
            for (group in $scope.groups) {
                if (group.name === $scope.addGroup) {
                    group.people.push({name:$scope.addName, email:$scope.addEmail})
                }
            }
        };

    }]);