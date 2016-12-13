#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Part of the Reusables package.
#
# Copyright (c) 2014-2016 - Chris Griffith - MIT License
"""
Functions to only be used on Interactive instances to ease life.

Designed to be used as a start import. `from reusables.cli import *`

"""
import os as _os

# Keep touch and download import so it can be imported with other CLI commands
from .shared_variables import *
from .reusables import run, win_based, find_all_files, touch
from .web import download


_saved_paths = []


def cmd(command, ignore_stderr=False, raise_on_return=False, timeout=None,
        encoding="utf-8"):
    """ Run a shell command and have it automatically decoded and printed

    :param command: Command to run as str
    :param ignore_stderr: To not print stderr
    :param raise_on_return: Run CompletedProcess.check_returncode()
    :param timeout: timeout to pass to communicate if python 3
    :param encoding: How the output should be decoded
    """
    result = run(command, timeout=timeout, shell=True)
    if raise_on_return:
        result.check_returncode()
    print(result.stdout.decode(encoding))
    if not ignore_stderr and result.stderr:
        print(result.stderr.decode(encoding))


def pushd(directory):
    """Change working directories in style and stay organized!

    :param directory: Where do you want to go and remember?
    :return: saved directory stack
    """
    directory = _os.path.expanduser(directory)
    _saved_paths.insert(0, _os.path.abspath(_os.getcwd()))
    _os.chdir(directory)
    return [directory] + _saved_paths


def popd():
    """Go back to where you once were.

    :return: saved directory stack
    """
    try:
        directory = _saved_paths.pop(0)
    except IndexError:
        return [_os.getcwd()]
    _os.chdir(directory)
    return [directory] + _saved_paths


def pwd():
    """Get the current working directory"""
    return _os.getcwd()


def cd(directory):
    """Change working directory, with built in user (~) expansion

    :param directory: New place you wanted to go
    """
    _os.chdir(_os.path.expanduser(directory))


def ls(params="", directory=".", printed=True):
    """Know the best python implantation of ls? It's just to subprocess ls...
    (uses dir on windows).

    :param params: options to pass to ls or dir
    :param directory: if not this directory
    :param printed: If you're using this, you probably wanted it just printed
    :return: if not printed, you can parse it yourself
    """
    command = "{0} {1} {2}".format("ls" if not win_based else "dir",
                                   params, directory)
    response = run(command, shell=True)  # Shell required for windows
    response.check_returncode()
    if printed:
        print(response.stdout.decode("utf-8"))
    else:
        return response.stdout


def find(name=None, ext=None, directory=".", match_case=False,
         disable_glob=False, depth=None):
    """ Designed for the interactive interpreter by making default order
    of find_all_files faster.

    :param name: Part of the file name
    :param ext: Extensions of the file you are looking for
    :param directory: Top location to recursively search for matching files
    :param match_case: If name has to be a direct match or not
    :param disable_glob: Do not look for globable names or use glob magic check
    :param depth: How many directories down to search
    :return: list of all files in the specified directory
    """
    return find_all_files(directory=directory, ext=ext, name=name,
                          match_case=match_case, disable_glob=disable_glob,
                          depth=depth)


def head(file_path, lines=10, encoding="utf-8", printed=True,
         errors='strict'):
    """
    Read the first N lines of a file, defaults to 10

    :param file_path: Path to file to read
    :param lines: Number of lines to read in
    :param encoding: defaults to utf-8 to decode as, will fail on binary
    :param printed: Automatically print the lines instead of returning it
    :param errors: Decoding errors: 'strict', 'ignore' or 'replace'
    :return: if printed is false, the lines are returned as a list
    """
    data = []
    with open(file_path, "rb") as f:
        for _ in range(lines):
            try:
                if python_version > (2, 6):
                    data.append(next(f).decode(encoding, errors=errors))
                else:
                    data.append(next(f).decode(encoding))
            except StopIteration:
                break
    if printed:
        print("".join(data))
    else:
        return data


def cat(file_path, encoding="utf-8", errors='strict'):
    """
          ^-^
         (-.-)
          |.|
         /  \\
        |    |   _/
        | || |  |
        \_||_/_/

    :param file_path: Path to file to read
    :param encoding: defaults to utf-8 to decode as, will fail on binary
    :param errors: Decoding errors: 'strict', 'ignore' or 'replace'
    """

    with open(file_path, "rb") as f:
        if python_version > (2, 6):
            print(f.read().decode(encoding, errors=errors))
        else:
            print(f.read().decode(encoding))


def tail(file_path, lines=10, encoding="utf-8",
         printed=True, errors='strict'):
    """
    A really silly way to get the last N lines, defaults to 10.


    :param file_path: Path to file to read
    :param lines: Number of lines to read in
    :param encoding: defaults to utf-8 to decode as, will fail on binary
    :param printed: Automatically print the lines instead of returning it
    :param errors: Decoding errors: 'strict', 'ignore' or 'replace'
    :return: if printed is false, the lines are returned as a list
    """
    data = []

    with open(file_path, "rb") as f:
        for line in f:
            if python_version > (2, 6):
                data.append(line.decode(encoding, errors=errors))
            else:
                data.append(line.decode(encoding))
            if len(data) > lines:
                data.pop(0)
    if printed:
        print("".join(data))
    else:
        return data
