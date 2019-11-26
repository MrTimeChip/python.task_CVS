class Branch:

    def __init__(self, name):
        self.name = name
        self.current_commit = None

    def set_current_commit(self, commit):
        self.current_commit = commit
