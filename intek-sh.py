#!/usr/bin/env python3
import os
import subprocess
import stat


# =CD====================================================================

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


# =PRINTENV=============================================================

def printenv(type_in):
    if len(type_in) == 1:
        for key in os.environ.keys():
            print(key + '=' + os.environ[key])
    else:
        variable = type_in[1]
        try:
            print(os.environ[variable])
        except KeyError:
            return


# =EXPORT==============================================================

def export(type_in):
    if len(type_in) == 1:
        return
    variable = type_in[1]
    if '=' not in variable:
        return
    else:
        variable = variable.split('=')
        os.environ[variable[0]] = variable[1]


# =UNSET================================================================

def unset(type_in):
    if len(type_in) == 1:
        return
    variable = type_in[1]
    try:
        del os.environ[variable]
    except KeyError:
        return


# =EXIT=================================================================

def sh_exit(type_in):
    if len(type_in) == 1:
        print('exit')
    elif type_in[1].isdigit():
        print('exit')
    else:
        print('exit\nintek-sh: exit:')
    raise SystemExit


# =SCRIPT================================================================

def isexecutable(file):
    st = os.stat(file)
    return bool(st.st_mode & stat.S_IXOTH)


def run_script(type_in):
    script = type_in
    if isexecutable(script[0]):
        subprocess.run(script)
    else:
        print('intek-sh: %s: Permission denied' % script[0])


# =MAIN=================================================================

def get_input():
    type_in = input('intek-sh$ ')
    while type_in == '':
        type_in = input('intek-sh$ ')
    # handle multiple spaces
    type_in = type_in.split(' ')
    while '' in type_in:
        type_in.remove('')
    return type_in[0], type_in[1:]


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
        elif command.startswith('./'):
            run_script(type_in)
        else:
            print('intek-sh: %s: command not found' % command)


if __name__ == '__main__':
    try:
        main()
    except EOFError:
        pass
