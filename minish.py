#!/usr/bin/env python3
import os


def cd(type_in):
    if len(type_in) == 1:
        path = ''
    else:
        path = type_in[1]
    if path != '':
        try:
            os.chdir(os.path.abspath(path))
        except FileNotFoundError:
            print('bash: cd: %s: No such file or directory' % path)
    elif path == '..':
        os.chdir('../')
    elif path == '':
        if 'HOME' in os.environ:
            os.chdir(os.environ['HOME'])
        else:
            print('intek-sh: cd: HOME not set')


def printenv(type_in):
    if len(type_in) == 1:
        print(os.environ)
    else:
        variable = type_in[1]
        try:
            print(os.environ[variable])
        except KeyError:
            return


def export(type_in):
    if len(type_in) == 1:
        return
    variable = type_in[1]
    if '=' not in variable:
        return
    else:
        variable = variable.split('=')
        os.environ[variable[0]] = variable[1]


def unset(type_in):
    if len(type_in) == 1:
        return
    variable = type_in[1]
    try:
        del os.environ[variable]
    except KeyError:
        return


def sh_exit(type_in):
    if len(type_in) == 1:
        print('exit')
    elif type_in[1].isdigit():
        print('exit')
    else:
        print('intek-sh: exit')
    exit()


def get_input():
    type_in = input('intek-sh$ ')
    while type_in == '':
        type_in = input('intek-sh$ ')
    # handle multiple spaces
    type_in = type_in.split(' ')
    while '' in type_in:
        type_in.remove('')
    return type_in[0], type_in


def main():
    while True:
        command, type_in = get_input()
        if command == 'pwd':
            print(os.getcwd())
        elif command == 'cd':
            cd(type_in)
        elif command == 'printenv':
            printenv(type_in)
        elif command == 'export':
            export(type_in)
        elif command == 'unset':
            unset(type_in)
        elif command == 'exit':
            sh_exit(type_in)
        else:
            print('intek-sh: %s: command not found' % command)


if __name__ == '__main__':
    try:
        main()
    except EOFError:
        pass
