#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob


def find_files():

    files = glob.glob('*.txt')

    return sorted(files)


def find_name(path):

    name = False

    with open(path) as f:
        for line in f:
            line = line.strip()

            if line == 'NOME DO ALUNO':
                name = True
                continue

            if line == 'MATRÍCULA' or len(line) == 0:
                continue

            if name: 
                    return line

    return 'Not found'


def is_matricula(text):

    if len(text) < 3:
        return False

    if text[2] != '/':
        return False

    text = text[0:2] + text[3:]

    return text.isdigit()


def remove_personal_data(path, sid):

    name = find_name(path)
    matricula = ''
    lines = []

    with open(path) as f:
        for line in f:
            line = line.strip()

            if line == name:
                print 'Removed name: [{}] (SID {})'.format(line, sid)
                continue

            if 'Pai' in line or 'Mãe' in line:
                print 'Removed parents: [{}]'.format(line)
                continue

            if is_matricula(line):
                matricula = line
                print 'Removed ID: [{}]'.format(line)
                lines.append('StudentID: {}'.format(sid))
                continue
            
            lines.append(line)

    output = '{}.data'.format(sid)
    data = '\n'.join(lines)

    with open(output, 'w') as f:
        f.write(data)

    with open('sid.list', 'a') as f:
        f.write('{}: {}\n'.format(sid, matricula))


if __name__ == '__main__':

    files = find_files()

    for i in range(len(files)):
        print '\nProcessing {}..'.format(files[i])
        remove_personal_data(files[i], i + 1)

