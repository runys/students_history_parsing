# -*- coding: utf-8 -*-

import json
from sets import Set
from pprint import pprint

# Abrindo o arquivo de alunos
alunos_file_path = "./json/historicos.json"
with open(alunos_file_path) as data_file:
    historicos = json.load(data_file)

# IRA
pesos = {
    'SR':  0,
    'II':  1,
    'MI':  2,
    'MM':  3,
    'MS':  4,
    'SS':  5,
    'TR': -1,
    'CC': -1,
    'AP': -1,
    'DP': -1,
    'TJ': -1
}

def calcularIRA(aluno):
    ira = 0.0
    num_disciplinas = 0
    for semestre in aluno["historico"]:
        for disciplina in semestre["disciplinas"]:
            if pesos[disciplina["mencao"]] != -1:
                ira += pesos[disciplina["mencao"]] * int(disciplina["credito"])
                num_disciplinas += 1
            
    return ira / num_disciplinas

#for aluno in historicos:
#    print("%d: %.2f" % (aluno["id"],calcularIRA(aluno)))

# IRA Programação
disciplinasProgramacao = Set([
        "113913",
        "116301",
        "195405",
        "206199",
        "110141",
        "195413",
        "206601",
        "101095",
        "208507",
        "103209",
        "201286",
        "206181",
        "195341",
        "193704",
        "203904",
        "107409",
        "107417",
        "206598",
        "193640",
        "201294",
        "208493",
        "103195",
        "117552",
        "203882",
        "208701"
    ])

def calcularIRASeletivo(aluno,disciplinas):
    ira = 0.0
    num_disciplinas = 0
    for semestre in aluno["historico"]:
        for disciplina in semestre["disciplinas"]:
            if pesos[disciplina["mencao"]] != -1 and disciplina["codigo"] in disciplinas:
                ira += pesos[disciplina["mencao"]] * int(disciplina["credito"])
                num_disciplinas += 1
    if num_disciplinas == 0:
        return 0
    
    return ira / num_disciplinas

#for aluno in historicos:
#    print("%d: %.2f" % (aluno["id"],calcularIRASeletivo(aluno,disciplinasProgramacao)))


# Quantas matérias de programação feitas
def contMaterias(aluno, codigos):
    cont = 0
    
    for semestre in aluno["historico"]:
        for disciplina in semestre["disciplinas"]:
            if disciplina["codigo"] in codigos:
                cont += 1
    
    return cont

for aluno in historicos:
    num_materias = contMaterias(aluno,disciplinasProgramacao)
    if num_materias > 25:
        print("%d: %d" % (aluno["id"],num_materias))


# Fez materia com juiz eletronico?
disciplinas_ejudge = [
    {"codigo":"193704","ano":2012,"periodo":2},
    {"codigo":"193704","ano":2013,"periodo":1},
    {"codigo":"208493","ano":2012,"periodo":2},
    {"codigo":"208493","ano":2013,"periodo":1},
    {"codigo":"208493","ano":2013,"periodo":2},
    {"codigo":"103195","ano":2013,"periodo":1},
    {"codigo":"103195","ano":2013,"periodo":2},
    {"codigo":"103195","ano":2014,"periodo":1},
    {"codigo":"103195","ano":2014,"periodo":2}
]

def isEjudge(aluno, disciplinas_ejudge):
    for semestre in aluno["historico"]:
        for disciplina in semetre["disciplinas"]:
            
    
    return False

# Desempenho antes do juiz
# Desempenho após o juiz