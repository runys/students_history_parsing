# -*- coding: utf-8 -*-

import json
from sets import Set
from pprint import pprint

# Abrindo o arquivo de alunos
alunos_file_path = "./json/historicos.json"
with open(alunos_file_path) as data_file:
    historicos = json.load(data_file)

# Objeto que irá armazenar os resultados dos processamentos    
data = {}

# Numero de alunos
data["num_alunos"] = len(historicos);

# Quantas matérias de programação feitas
# IRA
# IRA Programação
# Desempenho antes do juiz
# Desempenho após o juiz

# Todos os alunos que tiveram contato com ejudge
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
    if float(aluno["desempenho_antes_ejudge"]) < float(aluno["desempenho"]):
        num_aluno_melhorou += 1
        alunos_melhoraram.append(aluno["id"])
    elif float(aluno["desempenho_antes_ejudge"]) > float(aluno["desempenho"]):
        num_aluno_piorou += 1
        alunos_pioraram.append(aluno["id"])
    else:
        num_aluno_manteve += 1
        alunos_mantiveram.append(aluno["id"])

#print '+',num_aluno_melhorou,'\n-', num_aluno_piorou,'\n=', num_aluno_manteve

data["num_aluno_melhorou"] = num_aluno_melhorou
data["alunos_melhoraram"] = alunos_melhoraram 
data["num_aluno_piorou"] = num_aluno_piorou
data["alunos_pioraram"] = alunos_pioraram 
data["num_aluno_manteve"] = num_aluno_manteve
data["alunos_mantiveram"] = alunos_mantiveram 

# Maior IRA
# Menor IRA
max_ira = 0
min_ira = 9999

# Maior IRA Programacao
# Menor IRA Programacao
max_ira_prog = 0
min_ira_prog = 9999

# Media IRA
# Media IRA Programacao
sum_ira = 0
media_ira = 0
sum_ira_prog = 0
media_ira_prog = 0

for aluno in historicos:
    if aluno["desempenho"] > max_ira:
        max_ira = aluno["desempenho"]
        
    if aluno["desempenho"] < min_ira:
        min_ira = aluno["desempenho"]
    
    if aluno["desempenho_programacao"] > max_ira_prog:
        max_ira_prog = aluno["desempenho_programacao"]
    
    if aluno["desempenho_programacao"] < min_ira_prog:
        min_ira_prog = aluno["desempenho_programacao"]
        
    sum_ira += aluno["desempenho"]
    sum_ira_prog += aluno["desempenho_programacao"]
    
media_ira = sum_ira / data["num_alunos"]
media_ira_prog = sum_ira_prog / data["num_alunos"]

data["max_ira"] = max_ira
data["max_ira_prog"] = max_ira_prog
data["min_ira"] = min_ira
data["min_ira_prog"] = min_ira_prog
data["media_ira"] = media_ira
data["media_ira_prog"] = media_ira_prog

# Top 25 alunos IRA
# IRA
# IRA Prog
# IRA Depois = IRA
# IRA Antes de Ejudge

#pprint(data)
print(data)

alunosDataJSON = open('./json/alunos_data.json','w')
alunosDataJSON.write(json.dumps(data, sort_keys=False, indent=4, separators=(',',': ')))