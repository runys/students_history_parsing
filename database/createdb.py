# -*- coding: utf-8 -*-

import json

# Métodos auxiliares
### Confere se é ou não um código de disciplina
def isCodigoDeDisciplina (codigo):
    if codigo.isdigit() and len(codigo) == 6:
        return True
    return False

### Confere se é ou não uma menção
def isMencao (mencao):
    if mencao.isalpha() and len(mencao) == 2 and mencao != 'FT':
        return True
    return False

####### Processamento dos Arquivos #######

# Array para armazenar todos os alunos
alunos = []

# Passar por todos os arquivos
for i in range(257):
    # Abre o arquivo
    filename = "./data_1/" + str(i+1) + ".data"
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
            aluno['periodo_ingresso'] = aluno['periodo_ingresso'][:-1]
            break
    
    # StudentID
    for line in content:
        if 'StudentID:' in line:
            line = line.replace('StudentID: ','')
            aluno['id'] = line[:-1]
            break;
    
    # Data de Nascimento
    for line in content:
        if 'Nascimento:' in line:
            line = line.replace('Nascimento: ', '')
            aluno['data_nascimento'] = line[:-1]
    
    # Semestres
    periodos = []
    codigos_disciplinas = []
    mencoes = []
        
    # Códigos de Disciplina
    for line in content:
        words = line.split(' ')
        if len(words) > 1:
            if isCodigoDeDisciplina(words[1][:-1]):
                codigos_disciplinas.append(words[1][:-1])
        else:
            if isCodigoDeDisciplina(words[0][:-1]):
                codigos_disciplinas.append(words[0][:-1])
    
    # Menções
    for line in content:
        if isMencao(line[:-1]):
            mencoes.append(line[:-1])
    mencoes.pop()
    mencoes.pop()
    mencoes.pop()
    mencoes.pop()

    # Períodos
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
    
    # Contagem de disciplinas por período
    periodo_atual = 0
    cont = 0
    for line in content:
        if 'Período:' in line:
            if '(Continuação)' in line:
                pass
            else:
                # Atribuir o cont pro periodo
                if periodo_atual > 0:
                    periodos[periodo_atual - 1]['num_disciplinas'] = cont
                # Atualizar o periodo que estou contando
                periodo_atual += 1
                # Zerar o contador
                cont = 0    
        else:
            words = line.split(' ')
            if len(words) > 1:
                if isCodigoDeDisciplina(words[1][:-1]):
                    cont += 1
            else:
                if isCodigoDeDisciplina(words[0][:-1]):
                    cont += 1

    periodos[periodo_atual-1]['num_disciplinas'] = cont
    
    # Montar Histórico
    historico = []
    num = 1
    for periodo in periodos:
        semestre = {}
        semestre['numero'] = num
        num += 1
        semestre['ano'] = periodo['ano']
        semestre['periodo'] = periodo['periodo']
        semestre['disciplinas'] = []
        for i in range(periodo['num_disciplinas']):
            disciplina = {}
            disciplina['codigo'] = codigos_disciplinas.pop(0)
            disciplina['mencao'] = mencoes.pop(0)
            semestre['disciplinas'].append(disciplina)
        
        historico.append(semestre)

    aluno['historico'] = historico

    # Adiciona o aluno na lista de alunos
    alunos.append(aluno)

# Cria o JSON com os alunos
historicos = open('./json/historicos.json','w')
historicos.write(json.dumps(alunos, sort_keys=False, indent=4, separators=(',',': ')))


