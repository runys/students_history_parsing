# -*- coding: utf-8 -*-

import json
from sets import Set
from pprint import pprint

# Abrindo o arquivo de alunos
turmas_file_path = "./json/turmas.json"
with open(turmas_file_path) as data_file:
    turmas = json.load(data_file)
    
for ano in turmas:
    for periodo in ano["periodos"]:
        print ano["ano"], periodo["periodo"]
        for disciplina in periodo["turmas"]:
            if len(disciplina["alunos"]) > 0:
                print disciplina["codigo"], len(disciplina["alunos"])