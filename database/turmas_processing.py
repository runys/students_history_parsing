# -*- coding: utf-8 -*-

import json
from sets import Set
from pprint import pprint

# Abrindo o arquivo de turmas
turmas_file_path = "./json/turmas.json"
with open(turmas_file_path) as data_file:
    turmas = json.load(data_file)
    
disciplinas_programacao_file_path = "./json/disciplinas_programacao_indexado.json"
with open(disciplinas_programacao_file_path) as data_file:
    disciplinas_programacao_indexado = json.load(data_file)

#pprint(disciplinas_programacao_indexado)

turmas_data = {}

# Turmas com eJudge
    
# Histogramas
for ano in turmas:
    for periodo in ano["periodos"]:
#        print '\n',ano["ano"], periodo["periodo"]
        for disciplina in periodo["turmas"]:
            turma = {}
            turma["codigo"] = disciplina["codigo"]
            turma["ano"] = ano["ano"]
            turma["periodo"] = periodo["periodo"]
            turma["nome"] = disciplinas_programacao_indexado[disciplina["codigo"]]["nome"]
            turma["alunos_mencoes"] = []
            for aluno in disciplina["alunos"]:
                turma["alunos_mencoes"].append(aluno["mencao"])
                
            turma["alunos_ids"] = []
            for aluno in disciplina["alunos"]:
                turma["alunos_ids"].append(aluno["id"])
            
            turma["histograma"] = {}
            # Inicializa o histograma
            turma["histograma"]['SR'] = 0
            turma["histograma"]['II'] = 0
            turma["histograma"]['MI'] = 0
            turma["histograma"]['MM'] = 0
            turma["histograma"]['MS'] = 0
            turma["histograma"]['SS'] = 0
            turma["histograma"]['TR'] = 0
            turma["histograma"]['CC'] = 0
            turma["histograma"]['AP'] = 0
            turma["histograma"]['DP'] = 0
            turma["histograma"]['TJ'] = 0
            
            for mencao in turma["alunos_mencoes"]:
                turma["histograma"][mencao] += 1
            
            key = turma["codigo"] + '_' + turma["ano"] + '_' + turma["periodo"]
            
            turmas_data[key] = turma
            
pprint(turmas_data)

turmasDataJSON = open('./json/turmas_data.json','w')
turmasDataJSON.write(json.dumps(turmas_data, sort_keys=False, indent=4, separators=(',',': ')))
            