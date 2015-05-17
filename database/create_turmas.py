# -*- coding: utf-8 -*-

import json
from sets import Set
from operator import itemgetter
from pprint import pprint

##########################################################################

# Pega um objeto em um dicionario cujo valor da chave é igual o valor desejado
def getObj(dictionary, key, value):
    for obj in dictionary:    
        if obj[key] == value:
            return obj
    return None

# Pega uma turma de determinado periodo e ano de uma disciplina
def getTurma(disciplinas,codigo,ano,periodo):
    for disciplina in disciplinas:
        if disciplina["codigo"] == codigo:
            for turma in disciplina["turmas"]:
                if turma["ano"] == ano and turma["periodo"] == periodo:
                    return turma
    return None

# Adiciona um aluno em uma determinada turma
def addAlunoIn(array_turmas,ano,periodo,codigo,aluno):
    for t_ano in array_turmas:
        if t_ano["ano"] == ano:
            for t_periodo in t_ano["periodos"]:
                if t_periodo["periodo"] == periodo:
                    for t_turma in t_periodo["turmas"]:
                        if t_turma["codigo"] == codigo: 
                            t_turma["alunos"].append(aluno)

# Retorna os alunos de uma turma

print 'INICIO: JSON Turmas'

##########################################################################
# Abrindo arquivos de dados
alunos_file_path = "./json/historicos.json"
disciplinas_file_path = "./json/disciplinas_programacao.json"

# Historicos de todos os alunos
with open(alunos_file_path) as data_file:
    historicos = json.load(data_file)
# Disciplinas de programação
with open(disciplinas_file_path) as data_file:
    disciplinas = json.load(data_file)

##########################################################################
#Set com os códigos das disciplinas de programação
disciplinas_programacao = []
for disciplina in disciplinas:
    disciplinas_programacao.append(disciplina["codigo"])
    
disciplinas_programacao = Set(disciplinas_programacao)

##########################################################################
# Filtrando as menções de cada aluno por disciplina, por periodo
resultados = []
for aluno in historicos:   
    for semestre in aluno["historico"]:
        ano = semestre["ano"] 
        periodo = semestre["periodo"]
        for disciplina in semestre["disciplinas"]:
            if disciplina["codigo"] in disciplinas_programacao:
                entrada = {}
                entrada["aluno"] = aluno["id"]
                entrada["mencao"] = disciplina["mencao"]
                entrada["codigo"] = disciplina["codigo"]
                entrada["periodo"] = periodo
                entrada["ano"] = ano
                resultados.append(entrada)

##########################################################################
# Pegar todos os anos na base de dados
anos = Set([])
for aluno in historicos:
    for semestre in aluno["historico"]:
        anos.add(semestre["ano"])

# Cria as turmas por ano e por semestre
turmas = []
for num in anos:
    ano = {}
    ano["ano"] = num
    ano["periodos"] = []
    
    temp_turmas = []
    for codigo in disciplinas_programacao:
        obj = {}
        obj["codigo"] = codigo
        obj["alunos"] = []
        temp_turmas.append(obj)
    
    primeiro_periodo = {}
    primeiro_periodo["periodo"] = "1"
    primeiro_periodo["turmas"] = temp_turmas
    
    segundo_periodo = {}
    segundo_periodo["periodo"] = "2"
    segundo_periodo["turmas"] = temp_turmas
    
    
    ano["periodos"].append(primeiro_periodo)
    ano["periodos"].append(segundo_periodo)
    
    turmas.append(ano)

##########################################################################
i = 1
for e in resultados:
#    print "{} {}/{} {} {}".format(e["aluno"], e["ano"], e["periodo"], e["codigo"], e["mencao"])
    
    aluno = {}
    aluno["id"] = e["aluno"]
    aluno["mencao"] = e["mencao"]
    
    addAlunoIn(turmas,e["ano"],e["periodo"],e["codigo"], aluno)

##########################################################################
# Cria o JSON com as turmas
print '-- Criando JSON com as turmas das disciplinas de programação'
turmasJSON = open('./json/turmas.json','w')
turmasJSON.write(json.dumps(turmas, sort_keys=False, indent=4, separators=(',',': ')))
print 'FIM: JSON Turmas'