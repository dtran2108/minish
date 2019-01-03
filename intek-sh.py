#!/usr/bin/env python3
from os import chdir, environ, getcwd, path
from subprocess import run


def check_args(args):
    """ check if args is more than 1 """
    if len(args) is not 1:
        return True
    else:
        return False


def change_dir(dir_path):
    """ change the path and set environ PWD as the path """
    environ['OLDPWD'] = getcwd()
    chdir(dir_path)
    environ['PWD'] = getcwd()


def cd(cd_args):
    """ change to the required directory"""
    _path = None
    # if args is more than 1 -> path is the last argument
    if check_args(cd_args):
        _path = cd_args[1]
    if _path:
        if _path is '..':
            change_dir('..')
        elif _path is '-':
            change_dir(environ['OLDPWD'])
        else:
            try:
                change_dir(path.abspath(_path))
            except FileNotFoundError:
                print('intek-sh: cd: ' + _path + ': No such file or directory')
    else:  # if len path is 1 -> jump to HOME
        if 'HOME' in environ:
            change_dir(environ['HOME'])
        else:
            print('intek-sh: cd: HOME not set')


def printenv(printenv_args):
    """ print all the environment or part of it """
    # if len type_in is 1 -> print all the environment
    if not check_args(printenv_args):
        for key in environ.keys():
            print(key + '=' + environ[key])
    else: # print the value of the key(printenv_args[1])
        if printenv_args[1] in environ.keys():
            print(environ[printenv_args[1]])


def export(export_args):
    """ set the key for environment PATH """
    if check_args(export_args):
        variables = export_args[1:]
        for variable in variables:
            if '=' not in variable:
                environ[variable] = ''
            else:
                variable = variable.split('=')
                environ[variable[0]] = variable[1]


def unset(unset_args):
    """ remove the key from environment PATH """
    if check_args(unset_args):
        variables = unset_args[1:]
        for variable in variables:
            if variable in environ.keys():
                del environ[variable]


def sh_exit(exit_args):
    """ exit """
    print('exit')
    if check_args(exit_args) and not exit_args[1].isdigit():
        print('intek-sh: exit:')


def run_file(file_args):
    """ run the external file """
    check = False
    if './' in file_args[0]:
        try:
            run(file_args[0])
        except PermissionError:
            print('intek-sh: ' + file_args[0] + ': Permission denied')
        except FileNotFoundError:
            print("intek-sh: " + file_args[0] + ": No such file or directory")
    else:
        try:
            # find all the possible paths
            PATH = environ['PATH'].split(':')
        except KeyError as e:
            print("intek-sh: " + file_args[0] + ": command not found")
            return e
        for item in PATH:
            print(item)
            if path.exists(item+'/'+file_args[0]):
                run([item+'/'+file_args.pop(0)]+file_args)
                check = True
                break
        if not check: # if the command didn't run
            print("intek-sh: " + file_args[0] + ": command not found")


def get_input():
    """ return the command and the entire input """
    args = input('intek-sh$ ')
    while args == '' or args == ' ':
        args = input('intek-sh$ ')
    # handle multiple spaces
    args = args.split(' ')
    while '' in args:
        args.remove('')
    return args[0], args


def main():
    flag = True
    while flag:
        try:
            command, type_in = get_input()
        except EOFError as e:
            return e
        if command == 'cd':
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
