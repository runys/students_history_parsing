# -*- coding: utf-8 -*-

import json
from sets import Set

# Todos os códigos de menção possíveis
mencoes_legenda = Set(['SR','II','MI','MM','MS','SS','TR','CC','AP','DP','TJ'])
creditos_legenda = Set(['000','002','003','004','005','006','008','014','015','020'])

# Pesos de cada menção no calculo do rendimento do aluno
pesos = {
    'SR':  0,
    'II':  1,
    'MI':  2,
    'MM':  3,
    'MS':  4,
    'SS':  5,
    'TR': -1,
    'CC': -1,
    'AP': -1,
    'DP': -1,
    'TJ': -1
}

# Codigo das disciplinas de programação do curso
disciplinasProgramacao = Set([
        "113913",
        "116301",
        "195405",
        "206199",
        "110141",
        "195413",
        "206601",
        "101095",
        "208507",
        "103209",
        "201286",
        "206181",
        "195341",
        "193704",
        "203904",
        "107409",
        "107417",
        "206598",
        "193640",
        "201294",
        "208493",
        "103195",
        "117552",
        "203882",
        "208701"
    ])

# Turmas que usaram eJudge como auxilio a metodologia de ensino
disciplinas_ejudge = [
    {"codigo":"193704","ano":"2012","periodo":"2"},
    {"codigo":"193704","ano":"2013","periodo":"1"},
    {"codigo":"208493","ano":"2012","periodo":"2"},
    {"codigo":"208493","ano":"2013","periodo":"1"},
    {"codigo":"208493","ano":"2013","periodo":"2"},
    {"codigo":"103195","ano":"2013","periodo":"1"},
    {"codigo":"103195","ano":"2013","periodo":"2"},
    {"codigo":"103195","ano":"2014","periodo":"1"},
    {"codigo":"103195","ano":"2014","periodo":"2"}
]
# Métodos auxiliares
### Confere se é ou não um código de disciplina
def isCodigoDeDisciplina (codigo):
    return codigo.isdigit() and len(codigo) == 6

### Confere se é ou não uma menção
def isMencao (mencao):
    return mencao in mencoes_legenda

### Confere se é um número de créditos
def isCredito (credito):
    return credito in creditos_legenda

### Calcula o Indice de rendimento de um aluno
def calcularIRA(aluno):
    ira = 0.0
    num_disciplinas = 0
    for semestre in aluno["historico"]:
        for disciplina in semestre["disciplinas"]:
            if pesos[disciplina["mencao"]] != -1:
                ira += pesos[disciplina["mencao"]] * int(disciplina["credito"])
                num_disciplinas += int(disciplina["credito"])
            
    return ira / num_disciplinas

### Calcula o desempenho de um aluno com base nas disciplinas passadas por parâmetro
def calcularIRASeletivo(aluno,disciplinas):
    ira = 0.0
    num_disciplinas = 0
    for semestre in aluno["historico"]:
        for disciplina in semestre["disciplinas"]:
            if pesos[disciplina["mencao"]] != -1 and disciplina["codigo"] in disciplinas:
                ira += pesos[disciplina["mencao"]] * int(disciplina["credito"])
                num_disciplinas += int(disciplina["credito"])
    if num_disciplinas == 0:
        return 0
    
    return ira / num_disciplinas

### Calcula o desempenho do aluno antes dele fazer uma materia com ejudge
def calcularIRAAntesEjudge(aluno):    
    ira = 0.0
    num_disciplinas = 0
    turma = aluno["ejudge_turma"]
    for semestre in aluno["historico"]:
        if semestre["ano"] != turma["ano"] and semestre["periodo"] != turma["periodo"]:
            for disciplina in semestre["disciplinas"]:
#                if disciplina["codigo"] in disciplinasProgramacao and pesos[disciplina["mencao"]] != -1:
                if pesos[disciplina["mencao"]] != -1:
                    ira += pesos[disciplina["mencao"]]  * int(disciplina["credito"])
                    num_disciplinas += int(disciplina["credito"])
    if num_disciplinas == 0:
        return 0.0
    return ira / num_disciplinas

### Calcula o desempenho do aluno depois dele fazer uma materia com ejudge
def calcularIRADepoisEjudge(aluno):
    ira = 0.0
    num_disciplinas = 0
    turma = aluno["ejudge_turma"]
    for semestre in aluno["historico"]:
        if semestre["ano"] >= turma["ano"] and semestre["periodo"] >= turma["periodo"]:
            for disciplina in semestre["disciplinas"]:
                if disciplina["codigo"] in disciplinasProgramacao and pesos[disciplina["mencao"]] != -1:
                    ira += pesos[disciplina["mencao"]] * int(disciplina["credito"])
                    num_disciplinas += int(disciplina["credito"])
    
    return ira / num_disciplinas

### Conta quantas matérias com os códigos passados um aluno já fez, com repetições
def contMaterias(aluno, codigos):
    cont = 0
    
    for semestre in aluno["historico"]:
        for disciplina in semestre["disciplinas"]:
            if disciplina["codigo"] in codigos:
                cont += 1
    
    return cont

### Aluno cursou nas turmas?
def isTurma(aluno, disciplinas):
    for semestre in aluno["historico"]:
        for disciplina in semestre["disciplinas"]:
            for e in disciplinas:
                if e["ano"] == semestre["ano"] and e["periodo"] == semestre["periodo"]:
                    if e["codigo"] == disciplina["codigo"]:
                        return True
    
    return False

### Semestre ejudge
def getTurmaEjudge(aluno, disciplinas):
    for semestre in aluno["historico"]:
        for disciplina in semestre["disciplinas"]:
            for e in disciplinas:
                if e["ano"] == semestre["ano"] and e["periodo"] == semestre["periodo"]:
                    if e["codigo"] == disciplina["codigo"]:
                        return {
                            "ano": e["ano"],
                            "periodo": e["periodo"],
                            "codigo": disciplina["codigo"]
                        }


####### Processamento dos Arquivos #######
# Array para armazenar todos os alunos
alunos = []

# Passar por todos os arquivos da PRIMEIRA leva de dados
print 'Lendo arquivos de da pasta "./data_1" '
for i in range(257):
    # Abre o arquivo
    filename = "./data/data_1/" + str(i+1) + ".data"
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
            aluno['id'] = int(line[:-1])
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
    creditos = []
        
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

    # Creditos
    for line in content:
        if isCredito(line[:-1]):
            creditos.append(line[:-1])        
            
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
#    for d, m, c in zip(codigos_disciplinas, mencoes, creditos):
#        print '{} {} {}'.format(d,m,c)
    
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
            disciplina['credito'] = creditos.pop(0)
            semestre['disciplinas'].append(disciplina)
        
        historico.append(semestre)

    aluno['historico'] = historico
    
    #IRA
    aluno["desempenho"] = calcularIRA(aluno)
    
    #IRA Prog
    aluno["desempenho_programacao"] = calcularIRASeletivo(aluno, disciplinasProgramacao)
    
    #Quantidade de Materias de Programação
    aluno["num_disciplinas_programacao"] = contMaterias(aluno, disciplinasProgramacao)
    
    #Fez matéria com juiz eletrônico?
    if isTurma(aluno, disciplinas_ejudge):
        aluno["ejudge"] = True
        #Qual semestre que usou ejudge?
        aluno["ejudge_turma"] = getTurmaEjudge(aluno, disciplinas_ejudge)
        
        #IRA Antes do ejudge
        aluno["desempenho_antes_ejudge"] = calcularIRAAntesEjudge(aluno)
        #IRA depois do ejduge
        aluno["desempenho_depois_ejudge"] = calcularIRADepoisEjudge(aluno)
        
    else:
        aluno["ejudge"] = False
        
    # Adiciona o aluno na lista de alunos
    alunos.append(aluno)

print 'Dados lidos com sucesso!'
print 'Lendo arquivos de da pasta "./data_2" '
# Passar por todos os arquivos da SEGUNDA leva de dados    

for i in range(131):
    # Abre o arquivo
    filename = "./data/data_2/" + str(i+1) + ".data"
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
            
            id_aluno = int(line[:-1]) + 257
            
            aluno['id'] = id_aluno
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
    creditos = []
        
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
    
    # Creditos
    for line in content:
        if isCredito(line[:-1]):
            creditos.append(line[:-1]) 
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
            disciplina['credito'] = creditos.pop(0)
            semestre['disciplinas'].append(disciplina)
        
        historico.append(semestre)

    aluno['historico'] = historico

    #IRA
    aluno["desempenho"] = calcularIRA(aluno)
    
    #IRA Prog
    aluno["desempenho_programacao"] = calcularIRASeletivo(aluno, disciplinasProgramacao)
    
    #Quantidade de Materias de Programação
    aluno["num_disciplinas_programacao"] = contMaterias(aluno, disciplinasProgramacao)
    
    #Fez matéria com juiz eletrônico?
    if isTurma(aluno, disciplinas_ejudge):
        aluno["ejudge"] = True
        #Qual semestre que usou ejudge?
        aluno["ejudge_turma"] = getTurmaEjudge(aluno, disciplinas_ejudge)
        
        #IRA Antes do ejudge
        aluno["desempenho_antes_ejudge"] = calcularIRAAntesEjudge(aluno)
        #IRA depois do ejduge
        aluno["desempenho_depois_ejudge"] = calcularIRADepoisEjudge(aluno)
        
    else:
        aluno["ejudge"] = False
        
    
    # Adiciona o aluno na lista de alunos
    alunos.append(aluno)
print 'Dados lidos com sucesso!'

# Cria o JSON com os alunos
print 'Criando JSON com historicos dos alunos'
historicos = open('./json/historicos.json','w')
historicos.write(json.dumps(alunos, sort_keys=False, indent=4, separators=(',',': ')))

# INDEXADO
db_indexado = {}

for aluno in alunos:
    db_indexado[aluno["id"]] = aluno

# Cria o JSON indexado com os alunos
print 'Criando JSON com historicos dos alunos indexado'
historicos_indexado = open('./json/historicos_indexado.json','w')
historicos_indexado.write(json.dumps(db_indexado, sort_keys=False, indent=4, separators=(',',': ')))

