# -*- coding: utf-8 -*-

import json

def isCodigoDeDisciplina (codigo):
    if codigo.isdigit() and len(codigo) == 6:
        return True
    return False

def isMencao (mencao):
    if mencao.isalpha() and len(mencao) == 2:
        return True
    return False

# Alunos que irão compor a base de dados
alunos = []

for i in range(257):
    # Abre o arquivo
    filename = "./raw_data/" + str(i+1) + ".data"
    
    file = open(filename, 'r')
    # Separa cada linha do arquivo em um array de strings
    content = file.readlines()
    
    # Cria um aluno
    aluno = {}
    

    # Ingresso na UnB
    for line in content:
        if 'Ingresso na UnB:' in line:
            line = line.replace('Ingresso na UnB: ', '')
            aluno['ano_ingresso'], aluno['periodo_ingresso'] = line.split('/')
            aluno['periodo_ingresso'] = aluno['periodo_ingresso'][:-1] #limpa um /n indesejado
            break
    
    # StudentID
    for line in content:
        if 'StudentID:' in line:
            line = line.replace('StudentID: ','')
            aluno['id'] = line[:-1]
            break;
    
    # Nascimento
    for line in content:
        if 'Nascimento:' in line:
            line = line.replace('Nascimento: ', '')
            aluno['data_nascimento'] = line[:-1]
    
    # Semestres
    periodos = []
    codigos_disciplinas = [];
    mencoes = []
        
    # Pega todos os códigos de disciplina
    for line in content:
        if isCodigoDeDisciplina(line[:-1]):
            codigos_disciplinas.append(line[:-1])
    
    # Pega todas as menções
    for line in content:
        if isMencao(line[:-1]):
            mencoes.append(line[:-1])
    # retira 4 mencoes que ficam ao final do arquivo em uma legenda
    mencoes.pop()
    mencoes.pop()
    mencoes.pop()
    mencoes.pop()

    if len(mencoes) - len(codigos_disciplinas) > 3 or len(codigos_disciplinas) - len(mencoes) > 3:
        print 'ERROR: Look at ' + str(i+1) + '.data', 'Mencoes: ', len(mencoes), 'Disciplinas:', len(codigos_disciplinas), len(mencoes) - len(codigos_disciplinas)

    # Pega todos os períodos
    # Conta quantas disciplinas em cada períodos
    for line in content:
        if 'Período:' in line:
            periodo = {}
            line = line.replace('Período: ', '')
            periodo['ano'], periodo['periodo'] = line.split('/')
            periodo['periodo'] = periodo['periodo'][:-1]
            periodo['num_disciplinas'] = 0
            if '(Continuação)' in line:
                pass
            else:
                # print line[:-1]
                periodos.append(periodo)

    periodo_atual = 0
    cont = 0
    # print '-- Temos ', len(periodos), ' periodos no total'
    
    for line in content:
        if 'Período:' in line:
            if periodo_atual == 0:
                # print '--- Achei o primeiro período! ', line[:-1]
                periodo_atual += 1
            elif '(Continuação)' in line:
                # print '---- ', line[:-1]
                pass
            else:
                # print '--- O periodo possui ', cont, ' disciplinas' 
                periodos[periodo_atual-1]['num_disciplinas'] = cont
                periodo_atual += 1
                # print '--- Achei um novo periodo ', line[:-1], '. Comecando a contar.'
                cont = 0

        if isCodigoDeDisciplina(line[:-1]):
            cont += 1
    # print '--- O periodo ', line[:-1], ' possui ', cont, ' disciplinas'
    periodos[periodo_atual-1]['num_disciplinas'] = cont
    # print '-- Total de disciplinas cursadas: ', len(codigos_disciplinas  )
    
    # Monta histórico
    historico = []

    for periodo in periodos:
        semestre = {}
        semestre['ano'] = periodo['ano']
        semestre['periodo'] = periodo['periodo']
        semestre['disciplinas'] = []
        for i in range(periodo['num_disciplinas']):
            disciplina = {}
            disciplina['codigo'] = codigos_disciplinas.pop(0)
            disciplina['mencao'] = mencoes.pop(0)
            semestre['disciplinas'].append(disciplina)

        historico.append(semestre)

    # print historico

    aluno['historico'] = historico
    # Adiciona o aluno na lista de alunos
    alunos.append(aluno)

# DEBUG
# print alunos

# Cria o JSON com os alunos
historicos = open('./json/historicos.json','w')
historicos.write(json.dumps(alunos, sort_keys=True, indent=4, separators=(',',': ')))


