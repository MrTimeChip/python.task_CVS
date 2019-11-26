from cvs import CVS


def main():
    cvs = CVS()
    command = ''
    key = 'none'
    commands = {'init': cvs.init,
                'add': cvs.add,
                'commit': cvs.commit,
                'reset': cvs.reset,
                'log': cvs.log}
    commands[command](key)


if __name__ == "__main__":
    main()
