# -*- coding: utf-8 -*-

import json

alunos = []

for i in range(237):
    # Abre o arquivo
    filename = "./raw_data/" + str(i+1) + ".data"
    
    file = open(filename, 'r')
    # Separa cada linha do arquivo em um array de strings
    content = file.readlines()
    
    # Cria um aluno
    aluno = {}
    aluno['periodos'] = []
    
#    print 'Aluno ' + str(i+1) + ': '
    
    pos = 0
    for line in content:
        if line != '\n':
            # Ingresso na Unb
            if 'Ingresso na UnB:' in line:
                line = line.replace('Ingresso na UnB: ', '')
                aluno['ano_ingresso'], aluno['periodo_ingresso'] = line.split('/')
                aluno['periodo_ingresso'] = aluno['periodo_ingresso'][:-1] #limpa um /n indesejado
            
            # ID
            if 'StudentID:' in line:
                line = line.replace('StudentID: ','')
                aluno['id'] = line[:-1]
                
            # Nascimento
            if 'Nascimento:' in line:
                line = line.replace('Nascimento: ', '')
                aluno['data_nascimento'] = line[:-1]
            
            # Semestres
            if 'Período:' in line:
                periodo = {}
                
                codigos = []
                mencoes = []
                nomes = []
                creditos = []
                
                # Pega o período
                line = line.replace('Período: ', '')
                periodo['ano'], periodo['periodo'] = line.split('/')
                periodo['periodo'] = periodo['periodo'][:-1]
                
                periodo['disciplinas'] = []
                
                # Disciplinas e mençoes
                # conta o numero de materias
                temp = pos+1
                count = 0
                while content[temp] != '\n':
                    temp += 1
                    count += 1
                
                # pega os codigos das materias, mencoes, nomes e creditos
                temp_2 = temp+1
                for i in range(temp+1, temp+count+1):
                    codigos.append(content[i][:-1])
                    temp_2 += 1
                
                temp = temp_2
                for i in range(temp+1, temp+count+1):
                    mencoes.append(content[i][:-1])
                    temp_2 += 1
                
                temp = temp_2
                for i in range(temp+1, temp+count+1):
                    nomes.append(content[i][:-1])
                    temp_2 += 1
                
                temp = temp_2
                for i in range(temp+1, temp+count+1):
                    creditos.append(content[i][:-1])
                    temp_2 += 1
                
#                print codigos 
                
                
                
                
        pos += 1
    
    # Adiciona o aluno na lista de alunos
#    aluno['periodos'].pop()
    alunos.append(aluno)

#    print alunos
# Cria o JSON com os alunos
historicos = open('./json/historicos.json','w')
historicos.write(json.dumps(alunos, sort_keys=True, indent=4, separators=(',',': ')))