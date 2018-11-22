#!/usr/bin/env python3
import os
import subprocess
import stat


# =CD===========================================================================

def cd(type_in):
    if len(type_in) == 1:
        path = ''
    else:
        path = type_in[1]
    if path != '':
        try:
            os.chdir(os.path.abspath(path))
        except FileNotFoundError:
            print('intek-sh: cd: %s: No such file or directory' % path)
    elif path == '..':
        os.chdir('../')
    elif path == '':
        if 'HOME' in os.environ:
            os.chdir(os.environ['HOME'])
        else:
            print('intek-sh: cd: HOME not set')


# =PRINTENV=====================================================================

def printenv(type_in):
    if len(type_in) == 1:
        for key in os.environ.keys():
            print(key + '=' + os.environ[key])
    else:
        variable = type_in[1]
        if variable in os.environ.keys():
            print(os.environ[variable])
        else:
            return


# =EXPORT=======================================================================

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


# =UNSET========================================================================

def unset(type_in):
    if len(type_in) == 1:
        return
    variables = type_in[1:]
    for variable in variables:
        if variable in os.environ.keys():
            del os.environ[variable]
        else:
            return


# =EXIT=========================================================================

def sh_exit(type_in):
    if len(type_in) == 1:
        print('exit')
    elif type_in[1].isdigit():
        print('exit')
    else:
        print('exit\nintek-sh: exit:')


# =SCRIPT=======================================================================

def isexecutable(file):
    st = os.stat(file)
    return bool(st.st_mode & stat.S_IXOTH)


def run_script(type_in):
    script = type_in
    if isexecutable(script[0]):
        subprocess.run(script)
    else:
        print('intek-sh: %s: Permission denied' % script[0])


# =RUN_FILE=====================================================================

def getPath():
    if 'PATH' not in os.environ:
        return []
    elif ':' in os.environ['PATH']:
        return os.environ['PATH'].split(':')
    elif '.' in os.environ['PATH']:
        return [os.getcwd()]


def get_str_arg(type_in):
    temp = []
    for i in type_in:
        if type_in.index(i) != 0:
            if type_in.index(i) != len(type_in) - 1:
                temp.append(i)
            else:
                temp.append(i)
    return temp


def run_file_in_path(type_in):
    paths = getPath()
    flag = True
    if len(paths) > 0:
        for i in paths:
            file = i + '/' + type_in[0]
            if os.path.exists(file):
                if os.access(file, os.X_OK):
                    runlst = []
                    runlst.append(file)
                    if len(type_in) > 1:
                        arg = get_str_arg(type_in)
                        for i in arg:
                            runlst.append(i)
                    subprocess.run(runlst)
                    flag = False
    if flag:
        print("intek-sh: " + type_in[0] + ": command not found")


# =MAIN=========================================================================

def get_input():
    type_in = input('intek-sh$ ')
    while type_in == '' or type_in == ' ':
        type_in = input('intek-sh$ ')
    # handle multiple spaces
    type_in = type_in.split(' ')
    while '' in type_in:
        type_in.remove('')
    return type_in[0], type_in


def main():
    flag = True
    while flag:
        try:
            command, type_in = get_input()
        except EOFError:
            return
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
            flag = False
        elif command.startswith('./'):
            run_script(type_in)
        else:
            run_file_in_path(type_in)


if __name__ == '__main__':
        main()
