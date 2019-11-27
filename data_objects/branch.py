from data_objects.commit import Commit


class Branch:

    def __init__(self, name):
        self.name = name
        self.current_commit = None

    def set_current_commit(self, commit):
        """Sets current commit"""
        self.current_commit = commit

    def get_current_commit(self) -> Commit:
        """
        Returns current commit
        :returns current commit
        """
        return self.current_commit
