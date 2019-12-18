import configparser
import copy
import os
from os.path import join
from shutil import copyfile

from cvs_trees.index import Index
from data_objects.directory_info import DirectoryInfo


class WorkingDirectory:

    def __init__(self):
        self.__not_indexed_files = set()
        self.config = configparser.ConfigParser()

    @property
    def not_indexed_files(self):
        self.load_config()
        return copy.copy(self.__not_indexed_files)

    def find_not_indexed_files(self, indexed: set):
        """Finds not indexed files"""
        self.load_config()
        di = DirectoryInfo()
        for file in os.listdir(di.working_path):
            is_file = os.path.isfile(join(di.working_path, file))
            if is_file and file not in indexed:
                self.__not_indexed_files.add(file)
                info = self.config['info']
                files = info['not_indexed']
                info['not_indexed'] = f'{files},{file}'.strip(',')
        self.save_config()

    def reset(self, index: Index):
        """Rewrites file in current working __directory"""
        print('Working directory reset')
        di = DirectoryInfo()
        for filename in index.indexed_files:
            file_indexed = os.path.join(di.index_path, filename)
            file_origin = os.path.join(di.working_path, filename)
            copyfile(file_indexed, file_origin)
            print(f'Copied file from {file_indexed} to {file_origin}')

    def load_config(self):
        di = DirectoryInfo()
        path = os.path.join(di.cvs_path, 'wd.ini')
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(path)
        self.config = config
        self.get_data_from_config(path)

    def save_config(self):
        di = DirectoryInfo()
        path = os.path.join(di.cvs_path, 'wd.ini')
        with open(path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        di = DirectoryInfo()
        path = os.path.join(di.cvs_path, 'wd.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['not_indexed'] = ''
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)

    def get_data_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(config_path)

        self.__not_indexed_files = set()

        files = config['info']['not_indexed']
        if files != '':
            self.__not_indexed_files = set(files.split(','))
