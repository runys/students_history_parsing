# -*- coding: utf-8 -*-

import json
from sets import Set
from pprint import pprint

# Abrindo o arquivo de alunos
alunos_file_path = "./json/historicos.json"
with open(alunos_file_path) as data_file:
    historicos = json.load(data_file)

# Quantas matérias de programação feitas
# IRA
# IRA Programação
# Desempenho antes do juiz
# Desempenho após o juiz

alunos_ejudge = []
for aluno in historicos:
    if aluno["ejudge"]:
        alunos_ejudge.append(aluno)
    
num_aluno_melhorou = 0
alunos_melhoraram = []
num_aluno_piorou = 0
alunos_pioraram = []
num_aluno_manteve = 0
alunos_mantiveram = []

for aluno in alunos_ejudge:
    if float(aluno["desempenho_antes_ejudge"]) < float(aluno["desempenho_depois_ejudge"]):
        num_aluno_melhorou += 1
        alunos_melhoraram.append(aluno["id"])
    elif float(aluno["desempenho_antes_ejudge"]) > float(aluno["desempenho_depois_ejudge"]):
        num_aluno_piorou += 1
        alunos_pioraram.append(aluno["id"])
    else:
        num_aluno_manteve += 1
        alunos_mantiveram.append(aluno["id"])

print '+',num_aluno_melhorou,'\n-', num_aluno_piorou,'\n=', num_aluno_manteve

print alunos_melhoraram
print alunos_pioraram
print alunos_mantiveram