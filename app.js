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

app.controller('ClassesController', function ($scope, $http) {
    $scope.disciplinas_ejudge = [
        {
            "codigo": "193704",
            "ano": "2012",
            "periodo": "2"
        },
        {
            "codigo": "193704",
            "ano": "2013",
            "periodo": "1"
        },
        {
            "codigo": "208493",
            "ano": "2012",
            "periodo": "2"
        },
        {
            "codigo": "208493",
            "ano": "2013",
            "periodo": "1"
        },
        {
            "codigo": "208493",
            "ano": "2013",
            "periodo": "2"
        },
        {
            "codigo": "103195",
            "ano": "2013",
            "periodo": "1"
        },
        {
            "codigo": "103195",
            "ano": "2013",
            "periodo": "2"
        },
        {
            "codigo": "103195",
            "ano": "2014",
            "periodo": "1"
        },
        {
            "codigo": "103195",
            "ano": "2014",
            "periodo": "2"
        }
];

    $scope.dicionarioDisciplinas;
    $scope.gotDicionario = false;
    $scope.chartTitle = "";
    $scope.turmas;
    $scope.isDesempenho = false;
    $scope.turmaFocada = '';

    $scope.getNomeTurma = function (codigo) {
        if (!$scope.gotDicionario)
            return '';

        return $scope.dicionarioDisciplinas[codigo].nome;
    };

    $scope.desenharGrafico = function () {
        var turma = $scope.turmas[$scope.turmaFocada];

        if ($scope.isDesempenho) {
            console.log("Desenhado grafico de desempenho");
            drawPerformanceChart("turmaChart", turma);
        } else {
            console.log("Desenhado grafico de histograma");
            drawHistogramChart("turmaChart", turma);
        }

    };

    $scope.trocarTurma = function (key) {
        $scope.turmaFocada = key;
        $scope.desenharGrafico();

        var turma = $scope.turmas[key];

        $scope.chartTitle = turma.ano + '/' + turma.periodo + ' ' + $scope.getNomeTurma(turma.codigo);
    };

    // Lendo os JSONs 
    $http.get('./database/json/turmas_data.json')
        .success(function (data, status, headers, config) {
            $scope.turmas = data;

            $scope.trocarTurma("193704_2012_2");
        })
        .error(function (data, status, headers, config) {
            console.log('Failed to get classes data from turmas_data.json.');
        });


    $http.get('./database/json/disciplinas_programacao_indexado.json')
        .success(function (data, status, headers, config) {
            $scope.dicionarioDisciplinas = data;
            $scope.gotDicionario = true;
        })
        .error(function (data, status, headers, config) {
            console.log('Failed to get classes dictionary from disciplinas_programacao_indexado.json.');
        });

    // Desenhar Gráficos
    var drawBarGraph = function (id, labels, values) {
        var ctx = document.getElementById(id).getContext("2d");

        var data = {
            labels: labels,
            datasets: [
                {
                    label: name,
                    fillColor: "rgba(220,220,220,0.5)",
                    strokeColor: "rgba(220,220,220,0.8)",
                    highlightFill: "rgba(220,220,220,0.75)",
                    highlightStroke: "rgba(220,220,220,1)",
                    data: values
                }
            ]
        };

        var myBarChart = new Chart(ctx).Bar(data);
    };

    var drawHistogramChart = function (id, turma) {
        var labels = ['SR', 'II', 'MI', 'MM', 'MS', 'SS', 'TR', 'CC', 'AP', 'DP', 'TJ'];
        var values = [];

        for (var i = 0; i < labels.length; i++) {
            values.push(turma.histograma[labels[i]]);
        }

        drawBarGraph(id, labels, values);
    }

    var drawPerformanceChart = function (id, turma) {
        var labels = [];
        var values = [];

        var pesos = {
            'SR': 0,
            'II': 2,
            'MI': 4,
            'MM': 6,
            'MS': 8,
            'SS': 10,
            'TR': 0,
            'CC': 0,
            'AP': 0,
            'DP': 0,
            'TJ': 0
        };

        for (var i = 0; i < turma.alunos_ids.length; i++) {
            labels.push(turma.alunos_ids[i]);
            values.push(pesos[turma.alunos_mencoes[i]]);
        }

        drawBarGraph(id, labels, values);
    }
});

app.controller('AboutController', function ($scope) {
    $scope.title = "Sobre";
});