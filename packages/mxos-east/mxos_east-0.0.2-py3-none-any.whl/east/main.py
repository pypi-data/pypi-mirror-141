import sys
import argparse
from email.mime import application
import subprocess

__version__ = '0.0.2'

def do_build(args):
    print(args.application, args.module, args.flash)
    build_diretory = 'build/%s-%s' % (args.application, args.module)
    subprocess.run('cmake -B %s -GNinja -DAPP=%s -DMODULE=%s -DFLASH=%s' % 
        (build_diretory, args.application, args.module, 'NONE' if not args.flash else args.flash), 
        shell=True)
    subprocess.run('cmake --build %s' % (build_diretory), shell=True)

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
