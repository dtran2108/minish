#!/usr/bin/env python3
import os
import subprocess


def cd(type_in):
    if len(type_in) == 1:
        path = ''
    else:
        path = type_in[1]
    if path:
        if '..' in path:
            os.chdir('../')
            os.environ['PWD'] = os.getcwd()
        else:
            try:
                os.chdir(os.path.abspath(path))
                os.environ['PWD'] = os.getcwd()
            except FileNotFoundError:
                print('intek-sh: cd: %s: No such file or directory' % path)
    else:
        if 'HOME' in os.environ:
            os.chdir(os.environ['HOME'])
            os.environ['PWD'] = os.getcwd()
        else:
            print('intek-sh: cd: HOME not set')


def printenv(type_in):
    if len(type_in) == 1:
        for key in os.environ.keys():
            print(key + '=' + os.environ[key])
    else:
        variable = type_in[1]
        if variable in os.environ.keys():
            print(os.environ[variable])
        else:
            return None


def export(type_in):
    if len(type_in) == 1:
        return
    variables = type_in[1:]
    for variable in variables:
        if '=' not in variable:
            os.environ[variable] = ''
        else:
            variable = variable.split('=')
            os.environ[variable[0]] = variable[1]


def unset(type_in):
    if len(type_in) == 1:
        return None
    variables = type_in[1:]
    for variable in variables:
        if variable in os.environ.keys():
            del os.environ[variable]
        else:
            return None


def sh_exit(type_in):
    print('exit')
    if len(type_in) > 1 and not type_in[1].isdigit():
        print('intek-sh: exit:')


def run_file(type_in):
    check = False
    if './' in type_in[0]:
        try:
            subprocess.run(type_in[0])
        except PermissionError:
            print('intek-sh: ' + type_in[0] + ': Permission denied')
        except FileNotFoundError:
            print("intek-sh: " + type_in[0] + ": No such file or directory")
    else:
        try:
            PATH = os.environ['PATH'].split(':')
        except KeyError:
            print("intek-sh: " + type_in[0] + ": command not found")
            return
        for item in PATH:
            if os.path.exists(item+'/'+type_in[0]):
                subprocess.run([item+'/'+type_in.pop(0)]+type_in)
                check = True
                break
        if not check:
            print("intek-sh: " + type_in[0] + ": command not found")


def get_input():
    type_in = input('intek-sh$ ')
    type_in = type_in.split(' ')
    while '' in type_in:
        type_in.remove('')
    if type_in == []:
        get_input()
    print(type_in)
    return type_in[0], type_in

    # while type_in == '' or type_in == ' ':
    #     type_in = input('intek-sh$ ')
    # # handle multiple spaces
    # type_in = type_in.split(' ')
    # while '' in type_in:
    #     type_in.remove('')
    # return type_in[0], type_in


def main():
    flag = True
    while flag:
        try:
            command, type_in = get_input()
        except EOFError:
            return
        if 'pwd' in command:
            print(os.getcwd())
        elif 'cd' in command:
            cd(type_in)
        elif 'printenv' in command:
            printenv(type_in)
        elif 'export' in command:
            export(type_in)
        elif 'unset' in command:
            unset(type_in)
        elif 'exit' in command:
            sh_exit(type_in)
            flag = False
        else:
            run_file(type_in)


if __name__ == '__main__':
        main()
