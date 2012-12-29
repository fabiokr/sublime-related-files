import re
import glob
import itertools


class Related(object):
    # Initializes the RelatedFiles object.
    #
    # file_name - the file to look related files for
    # patterns  - a dictionary of patterns in the following format:
    #               {"(.+)_controller.rb": ["*/the/paths/$1/**", "*/test/$1_controller_test.rb"]}
    #
    # The glob paths will have their $i replaced by the matched groups within the file name
    # matcher.
    def __init__(self, file_name, patterns):
        self.file_name = file_name
        self.patterns = patterns

    # Returns a list with all related files.
    def all(self):
        match, paths = self.__lookup_pattern()

        # returns a flattened file list
        return list(itertools.chain.from_iterable(self.__files_for_path(match, paths)))

    # Retrives the matching regex and paths.
    def __lookup_pattern(self):
        for regex, paths in self.patterns.iteritems():
            match = re.compile(regex).match(self.file_name)
            if match:
                return [match, paths]

    # Retrieves a list of files fot the given match and paths
    def __files_for_path(self, match, paths):
        paths = [self.__replaced_path(match, path) for path in paths]
        return [glob.glob(path) for path in paths]

    # Retrieves a path with its interpolation vars replaces by the found groups
    # on match.
    def __replaced_path(self, match, path):
        replaced_path = path
        for i, group in enumerate(match.groups()):
            replaced_path = replaced_path.replace("$%s" % (i + 1), group)
        return replaced_path
