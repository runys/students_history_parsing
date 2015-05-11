# -*- coding: utf-8 -*-

import json
from sets import Set

def isCodigoDeDisciplina (codigo):
    return codigo.isdigit() and len(codigo) == 6

mencoes = Set(['SR','II','MI','MM','MS','SS','TR','CC','AP','DP','TJ'])

print 'Validando DB de historicos'

file_path = "./json/historicos.json"

with open(file_path) as data_file:
    historicos = json.load(data_file)

print '- Validando IDs'
# IDs são sequenciais? São ids únicos?
id_anterior = 1
ids = Set([1])
for aluno in historicos:
    if aluno['id'] > 1:
        id_aluno = aluno['id']
        if id_aluno - 1 != id_anterior:
            print '-- ID ' + str(id_aluno) + ' não sequencial'
        if id_aluno in ids:
            print '-- ID ' + str(id_aluno) + ' repetido'
        ids.add(id_aluno)

    id_anterior = aluno['id']

print '- Validando disciplinas'
# Validar se disciplina possui menção
# Validar codigos de disciplinas
for aluno in historicos:
    for semestre in aluno['historico']:
        for disciplina in semestre['disciplinas']:
            if isCodigoDeDisciplina(disciplina['codigo']) == False:
                print '--' + str(aluno['id']) + ': Disciplina ' + disciplina['codigo'] + ' invalido'
            if disciplina['mencao'] == '':
                print '--' + str(aluno['id']) + ': Disciplina ' + disciplina['codigo'] + ' sem menção'
            if disciplina['credito'] == '':
                print '--' + str(aluno['id']) + ': Disciplina ' + disciplina['codigo'] + ' sem credito'
                
print '- Validando menções'
# Validar menções
for aluno in historicos:
    for semestre in aluno['historico']:
        for disciplina in semestre['disciplinas']:
            if disciplina['mencao'] not in mencoes:
                print '--' + str(aluno['id']) + ': ' + disciplina['mencao']
                