# -*- coding: utf-8 -*-

import json
from pprint import pprint

def isCodigoDeDisciplina (codigo):
    return codigo.isdigit() and len(codigo) == 6

# Abre o arquivo
filename = "./data/disciplinas.data"
file = open(filename, 'r')    
# Separa cada linha do arquivo em um array de strings
content = file.readlines()

# Conta as disciplinas
i = 0
for line in content:
    if isCodigoDeDisciplina(line[:-1]):
        i += 1
    else:
        break

codigos = []
nomes = []
status = []
prerequisitos = []
j = 0
for line in content:    
    if j < i:
        codigos.append(line[:-1])
    elif j < i*2:
        nomes.append(line[:-1])
    elif j < i*3:
        status.append(line[:-1])
    else:
        prerequisitos.append(line[:-1])
    j += 1
    
disciplinas = []
for k in range(i):
    disciplina = {}
    disciplina['codigo'] = codigos[k]
    disciplina['nome'] = nomes[k]
    disciplina['status'] = status[k]
    disciplina['prerequisitos'] = prerequisitos[k]
    
    disciplinas.append(disciplina)

print 'Criando JSON das disciplinas de programação'
disciplinasJSON = open('./json/disciplinas_programacao.json','w')
disciplinasJSON.write(json.dumps(disciplinas, sort_keys=False, indent=4, separators=(',',': ')))
