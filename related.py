import os
import re
import glob
import itertools
from sets import Set


class Related(object):
    # Initializes the RelatedFiles object.
    #
    # file_path - the file to look related files for
    # patterns  - a dictionary of patterns in the following format:
    #               {"(.+)_controller.rb": ["*/the/paths/$1/**", "*/test/$1_controller_test.rb"]}
    #
    # The glob paths will have their $i replaced by the matched groups within the file name
    # matcher.
    def __init__(self, file_path, patterns, folders):
        self.file_path = file_path
        self.patterns = patterns
        self.root = self.__root(folders)

    # Returns a list with all related files.
    def all(self):
        files = Set()

        # for each matching pattern
        for regex, paths in self.patterns.iteritems():
            match = re.compile(regex).match(self.file_path)
            if match:
                # returns a flattened file list
                files.update(self.__files_for_paths(match, paths))

        # sorts items
        files = list(files)
        files.sort()

        return self.__files_with_description(files)

    # Returns the root folder for the given file and folders
    def __root(self, folders):
        for folder in folders:
            if self.file_path.startswith(folder):
                return folder

    # Retrieves a list of files fot the given match and paths
    def __files_for_paths(self, match, paths):
        paths = [self.__replaced_path(match, path) for path in paths]
        files = [glob.glob(self.root + "/" + path) for path in paths]

        flattened = list(itertools.chain.from_iterable(files))

        return flattened

    # Retrieves a list of files with their description.
    #
    # [["file/path", "/full/file/path"]]
    def __files_with_description(self, files):
        return [[self.__file_without_root(file), file] for file in files]

    # Retrieves the file name without the root part.
    def __file_without_root(self, file):
        return os.path.basename(self.root) + file[len(self.root):]

    # Retrieves a path with its interpolation vars replaces by the found groups
    # on match.
    def __replaced_path(self, match, path):
        replaced_path = path
        for i, group in enumerate(match.groups()):
            replaced_path = replaced_path.replace("$%s" % (i + 1), group)
        return replaced_path
