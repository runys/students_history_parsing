var app = angular.module("StudentPerformanceApp", []);

app.controller('HomeController', function ($scope) {
    $scope.title = "Home";
});

app.controller('StudentsController', function ($scope, $http) {
    $scope.title = "Estudantes";
    $scope.students = {};

    var processingStudentsData = function (data, status, headers, config) {
        console.log('Got students processed data from alunos_data.json.');

        var studentsProcessedInfo = data;

        $scope.max_student_performance = studentsProcessedInfo.max_ira.toFixed(2);
        $scope.max_student_performance_prog = studentsProcessedInfo.max_ira_prog.toFixed(2);

        $scope.min_student_performance = studentsProcessedInfo.min_ira.toFixed(2);
        $scope.min_student_performance_prog = studentsProcessedInfo.min_ira_prog.toFixed(2);

        $scope.mean_student_performance = studentsProcessedInfo.media_ira.toFixed(2);
        $scope.mean_student_performance_prog = studentsProcessedInfo.media_ira_prog.toFixed(2);

        $scope.num_students = studentsProcessedInfo.num_alunos;

    };

    var processingStudents = function (data, status, headers, config) {
        $scope.students = data;
        console.log('Got students histories from alunos_data.json.');

        var alunos_ejudge = [];
        for (var i = 0; i < $scope.students.length; i++) {
            if ($scope.students[i].ejudge)
                alunos_ejudge.push($scope.students[i]);
        }

        $scope.students_ejudge = alunos_ejudge;
    };

    // Pega o JSON com os dados processados dos estudantes
    $http.get('./database/json/alunos_data.json')
        .success(processingStudentsData)
        .error(function (data, status, headers, config) {
            console.log('Failed to get students processed data from alunos_data.json.');
        });

    // Pega JSON com os historicos dos estudantes
    $http.get('./database/json/historicos.json')
        .success(processingStudents)
        .error(function (data, status, headers, config) {
            console.log('Failed to get students histories from historicos.json.');
        });
});

app.controller('ClassesController', function ($scope) {
    $scope.title = "Turmas";
});

app.controller('AboutController', function ($scope) {
    $scope.title = "Sobre";
});