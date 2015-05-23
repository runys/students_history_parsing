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

# Histogramas
for ano in turmas:
    for periodo in ano["periodos"]:
        print '\n',ano["ano"], periodo["periodo"]
        for disciplina in periodo["turmas"]:
            for aluno in disciplina["alunos"]:
            