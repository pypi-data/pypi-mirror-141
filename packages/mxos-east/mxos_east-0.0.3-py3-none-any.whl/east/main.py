import sys
import os
import errno
import pathlib
import argparse
import subprocess

__version__ = '0.0.3'

def mkdir_p(path):  # type: (str) -> None
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise

def get_env():  # type: () -> None
    home = str(pathlib.Path.home())
    env_path = os.path.abspath(os.path.join(home, '.mxos-east'))
    if not os.path.exists(env_path):
        print(f'Directory {env_path} was not found.')
        print(f'Creating {env_path} ...')
        mkdir_p(env_path)
    return env_path

def do_build(args):
    env_path = get_env()
    build_diretory = f'build/{args.application}-{args.module}'
    subprocess.run(f'cmake -B {build_diretory} -GNinja -DAPP={args.application} -DMODULE={args.module} -DFLASH={"NONE" if not args.flash else args.flash} -DMXOS_ENV={env_path}', 
        shell=True)
    subprocess.run(f'cmake --build {build_diretory}', shell=True)

def main(argv=None):

    parser = argparse.ArgumentParser(prog='east',
        description=f'The MXOS meta-tool v{__version__}.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version',
        version=f'East version: v{__version__}',
        help='print the program version and exit')

    subparsers = parser.add_subparsers(metavar='<command>', dest='command')

    parser_build = subparsers.add_parser('build', help='build a MXOS application')
    parser_build.add_argument('-m', '--module', required=True, help='module to build for')
    parser_build.add_argument('-f', '--flash', required=False, help='type to flash, can be APP or ALL')
    parser_build.add_argument('application', help='application source directory')
    parser_build.set_defaults(func=do_build)

    if len(sys.argv) <= 1:
        parser.print_help()
        return

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
