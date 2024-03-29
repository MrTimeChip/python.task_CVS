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
        help='File to add to current commit.')

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
        choices=['soft', 'mixed', 'hard'],
        default='mixed',
        help='Reset types. Warning! --hard will overwrite your files!')

    update_parser = subparsers.add_parser(
        'update',
        help='Get certain version from repository.',
        description='Gets certain version from repository.'
                    'Replaces your current version with one from repository.')
    update_parser.add_argument(
        'file',
        help='Filename to get from repository.')
    update_parser.add_argument(
        'version',
        help='Version of file to get.')

    branch_parser = subparsers.add_parser(
        'branch',
        help='Make new branch.',
        description='Makes new branch.')
    branch_parser.add_argument(
        'branchname',
        help='New branch name')

    branches_parser = subparsers.add_parser(
        'branches',
        help='Returns branches list.',
        description='Returns all branches list')

    checkout_parser = subparsers.add_parser(
        'checkout',
        help='Checkout branch.',
        description='Sets current branch.')
    checkout_parser.add_argument(
        'checkout_branchname',
        help='Branch name to checkout.')

    diff_parser = subparsers.add_parser(
        'diff',
        help='Show diff between two files version.',
        description='Shows diff between two files version.')
    diff_parser.add_argument(
        'diff_filename',
        help='Name of file to compare.')
    diff_parser.add_argument(
        'first_version',
        help='First of versions to compare.')
    diff_parser.add_argument(
        'second_version',
        help='Second of versions to compare')

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
    elif namespace.command == 'commit':
        cvs.commit(namespace.commit_message)
    elif namespace.command == 'reset':
        cvs.reset(namespace.type)
    elif namespace.command == 'add':
        cvs.add(namespace.filename)
    elif namespace.command == 'log':
        cvs.log()
    elif namespace.command == 'update':
        cvs.update(namespace.file, namespace.version)
    elif namespace.command == 'branch':
        cvs.branch(namespace.branchname)
    elif namespace.command == 'branches':
        cvs.branches()
    elif namespace.command == 'checkout':
        cvs.checkout(namespace.checkout_branchname)
    elif namespace.command == 'diff':
        cvs.diff(namespace.diff_filename,
                 namespace.first_version,
                 namespace.second_version)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
