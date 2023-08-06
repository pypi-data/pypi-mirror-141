#!/usr/bin/env python3
# encoding:utf-8


import glob
import itertools
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, ArgumentTypeError, Action, ArgumentError
from collections import OrderedDict
from os.path import expanduser
from pathlib import Path
from tempfile import TemporaryDirectory

SIGNATURES_EXTENSIONS = frozenset(['asc', 'gpg', 'sig'])


def sort_argparse_help(parser: ArgumentParser):
    for g in parser._action_groups:
        g._group_actions.sort(key=lambda x: x.dest)


def check_positive(value):
    try:
        int_value, float_value = int(value), float(value)
    except ValueError:
        raise ArgumentTypeError(f"invalid int value: '{value}'")
    if (int_value != float_value) or (int_value <= 0):
        error = f'{value} must be a positive integer'
        raise ArgumentTypeError(error)
    return int_value


def check_path_exists(value):
    path = Path(value)
    if not path.exists():
        error = f"path '{path}' does not exist"
        raise ArgumentTypeError(error)
    return path.resolve()


def check_folder_name(folder_name):
    tmp = TemporaryDirectory()
    path = Path(tmp.name).joinpath(folder_name)
    try:
        path.mkdir(exist_ok=True)
    except:
        error = f"specified folder name '{folder_name}' is invalid"
        raise ArgumentTypeError(error)
    finally:
        tmp.cleanup()


def check_destination(value):
    path = Path(value)
    parent, folder_name = path.parent, path.name
    if path.exists():
        path = path.resolve()
        if path.is_file():
            error = f"specified destination '{path}' is a file"
            raise ArgumentTypeError(error)
        return path
    parent = check_path_exists(parent)
    path = parent.joinpath(folder_name)
    try:
        path.mkdir(exist_ok=True)
        path.rmdir()
    except PermissionError:
        error = f"permission denied to create folder '{folder_name}' inside '{parent}'"
        raise ArgumentTypeError(error)
    return path


def get_files(value):
    pval = Path(value)
    if pval.exists():
        return (pval.resolve(),) if pval.is_file() and not pval.is_symlink() and pval.suffix[1:] not in SIGNATURES_EXTENSIONS else tuple()
    return [p.resolve() for p in sorted((Path(x) for x in glob.iglob(expanduser(value))), key=lambda x: str(x).lower())
            if p.is_file() and not p.is_symlink() and p.suffix[1:] not in SIGNATURES_EXTENSIONS]


def get_folders(value):
    pval = Path(value)
    if pval.exists():
        return (pval.resolve(),) if pval.is_dir() and not pval.is_symlink() else tuple()
    return [p.resolve() for p in (Path(x) for x in glob.iglob(expanduser(value))) if p.is_dir() and not p.is_symlink()]


class FlatFilesListsAction(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        res = list(itertools.chain.from_iterable(values))
        if not len(res):
            error = f'no files selected'
            raise ArgumentError(self, error)
        res = list(OrderedDict.fromkeys(res))
        setattr(namespace, self.dest, res)


class FlatFoldersListsAction(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        res = set(itertools.chain.from_iterable(values))
        setattr(namespace, self.dest, res)


# SIGNER PARSER
sign_parser = ArgumentParser(prog='gpg-multiple-signatures', description='Sign multiple files with GPG at the same time.', formatter_class=ArgumentDefaultsHelpFormatter)
sign_parser.add_argument('--binary', '-b', action='store_true', help='the signatures are generated in binary format instead of ASCII-armored')
sign_parser.add_argument('--destination', '-d', metavar='FOLDER', type=check_destination,
                         help='name or path of the folder in which the generated signatures will be stored. If a single folder name is specified and it does not exist, '
                              'it will be created if possible. The default behavior is to store signatures in the same place as the files being signed.')
sign_parser.add_argument('--extension', '-e', choices=SIGNATURES_EXTENSIONS, default='sig', help='signature files extension')
sign_parser.add_argument('--overwrite', '-o', action='store_true', help='if a signature file already exists, it will be overwritten. '
                                                                        'The default behavior is to skip files whose signatures already exist.')
sign_parser.add_argument('--threads', '-t', default=3, type=check_positive, help='number of threads running simultaneously to sign files in parallel')
sign_parser.add_argument('--users', '-u', metavar='USER', nargs='+', help='add one user or key to sign the files. If the option is not specified, the default GPG user is used.')
sign_parser.add_argument('--files', '-f', metavar='FILE', nargs='+', type=get_files, action=FlatFilesListsAction,
                         help='list of files to be signed. Files with extension .[asc|gpg|sig] will be ignored. Supports UNIX expansion.', required=True)

# VERIFIER PARSER
verify_parser = ArgumentParser(prog='gpg-multiple-verifications', description='Verify multiple detached signatures with GPG at the same time.', formatter_class=ArgumentDefaultsHelpFormatter)
verify_parser.add_argument('--append-folders', '-a', dest='folders', metavar='FOLDER', nargs='+', type=get_folders, action=FlatFoldersListsAction,
                           help='add a folder to the folder list to search for file signatures. By default, the program searches the folder where each '
                                'file is located and one more sublevel. Supports UNIX expansion.')
verify_parser.add_argument('--threads', '-t', default=3, type=check_positive, help='number of threads running simultaneously to verify signatures in parallel')
verify_parser.add_argument('--files', '-f', metavar='FILE', nargs='+', type=get_files, action=FlatFilesListsAction,
                           help='list of files to be verified. Files with extension .[asc|gpg|sig] will be ignored. Supports UNIX expansion.', required=True)

# SORTING HELP
sort_argparse_help(sign_parser)
sort_argparse_help(verify_parser)
