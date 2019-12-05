import sys

from cvs import CVS
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description=
                                     'Git-like version control system.',
                                     epilog=
                                     '(c) Danil Pankov 2019. '
                                     'CS-201 study project.')
    subparsers = parser.add_subparsers(
        dest='command',
        title='Available commands.',
        description='Commands to pass as first parameter.')

    init_parser = subparsers.add_parser(
        'init',
        help='Initialize VCS at certain directory.',
        description='Initializes working directories for VCS (.CVS).')
    init_parser.add_argument(
        'directory',
        help='Directory where cvs will look for files.')

    add_parser = subparsers.add_parser(
        'add',
        help='Add file to current commit.',
        description='Current state will be saved and added to current commit.')
    add_parser.add_argument(
        'filename',
        help='File to add to current commit.',
        type=argparse.FileType())

    commit_parser = subparsers.add_parser(
        'commit',
        help='Save current changes and make a commit.',
        description='Save current changes and make a commit.'
                    'Commit will be saved at the repository.')
    commit_parser.add_argument(
        'commit_message',
        help='Commit message.')

    reset_parser = subparsers.add_parser(
        'reset',
        help='Reset current CVS state.',
        description='Resets CVS state. '
                    'Takes info from last versions from repository.')
    reset_parser.add_argument(
        'type',
        choices=['--soft', '--mixed', '--hard'],
        default='--mixed',
        help='Reset types. Warning! --hard will overwrite your files!')

    subparsers.add_parser(
        'log',
        help='Show commit history.',
        description='Shows commits, starting from last.')

    return parser


def main():  # pragma: no cover
    cvs = CVS()
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.command == 'init':
        cvs.init(namespace.directory)
    if namespace.command == 'commit':
        cvs.commit(namespace.commit_message)
    if namespace.command == 'reset':
        cvs.reset(namespace.type)
    if namespace.command == 'add':
        cvs.add(namespace.filename)
    if namespace.command == 'log':
        cvs.log()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
