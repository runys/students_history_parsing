# -*- coding: utf-8 -*-

import json
from sets import Set
from operator import itemgetter

print 'Criando turmas das disciplinas de programacao'

alunos_file_path = "./json/historicos.json"
disciplinas_file_path = "./json/disciplinas_programacao.json"

with open(alunos_file_path) as data_file:
    historicos = json.load(data_file)

with open(disciplinas_file_path) as data_file:
    disciplinas = json.load(data_file)

#for disciplina in disciplinas:
#    
#    print disciplina['codigo'] +' '+ disciplina['nome']
#    cont = 0
#    for aluno in historicos:
#        for periodo in aluno['historico']:
#            for aluno_disciplina in periodo['disciplinas']:
#                if aluno_disciplina['codigo'] == disciplina['codigo']:
##                    print 'Aluno {}: {}'.format(aluno['id'], aluno_disciplina['mencao'])
#                    cont += 1
#                    break
#    print '-- {} alunos'.format(cont)
                
#Montando turma de ICC de 2014/1
t_code = '113913'
t_ano = '2013'
t_periodo = '1'

turma = {}
turma['codigo'] = t_code
turma['ano'] = t_ano
turma['periodo'] = t_periodo
turma['alunos'] = []
for aluno in historicos:
    for periodo in aluno['historico']:
        if periodo['ano'] == t_ano and periodo['periodo'] == t_periodo:
            for a_disciplina in periodo['disciplinas']:
                if a_disciplina['codigo'] == t_code:
                    a = {}
                    a['id'] = aluno['id']
                    a['mencao'] = a_disciplina['mencao']
                    turma['alunos'].append(a)
print '- Turma de {} de {}/{}: {} alunos'.format(turma['codigo'],turma['ano'],turma['periodo'], len(turma['alunos']))
for aluno in sorted(turma['alunos'],key=itemgetter('mencao')):
    print '-- {} {}'.format(aluno['id'], aluno['mencao'])
    
    
#turma = {
#    'ano':'',
#    'periodo':'',
#    'codigo':'',
#    'alunos' = [{'id':'','mencao':''}],
#    'credito':''
#}

#turma = {
#    codigo
#    periodo
#}