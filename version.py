from cvs import CVS


def main():  # pragma: no cover
    cvs = CVS()
    commands = {'init': cvs.init,
                'add': cvs.add,
                'commit': cvs.commit,
                'reset': cvs.reset,
                'log': cvs.log,
                '-h': print_help,
                '--help': print_help}
    while True:
        user_input = input()
        arguments = user_input.split()
        command = arguments[0]
        if command not in commands.keys():
            print(f'Wrong command! {command}')
            continue
        if len(arguments) > 1:
            key = arguments[1]
            commands[command](key)
        else:
            commands[command]()


def print_help():
    print('This is a cvs-like version control system.')
    print('Commands are:')
    print('\tinit [path] - set new working directory at path')
    print('\t\tCurrent execution path if none')
    print('')
    print('\tadd filename - add new file to repository')
    print('\t\tSystem will remember added file state')
    print('\t\tShould be used after any changes to file')
    print('')
    print('\tcommit commit_message - make new commit')
    print('\t\tSaves current added files state at the repository')
    print('')
    print('\treset [--soft, --mixed, --hard] - resets repository state')
    print('\t\t--soft - resets last commit to previous at repository')
    print('\t\t--mixed - --soft and changed files are ones from last commit')
    print('\t\t--hard - --mixed and replaces files at the working directory')
    print('\t\t\twith files of the last commit')
    print('')
    print('\tlog - prints commits history')
    print('')


if __name__ == "__main__":
    main()
