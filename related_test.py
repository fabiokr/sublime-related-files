import unittest
import os
from related import *


class RelatedTest(unittest.TestCase):

    def __patterns(self):
        return {".+\/app\/controllers\/(.+)_controller.rb": ["*/app/views/$1/**", "*/test/controllers/$1_controller_test.rb"]}

    def __file(self):
        return self.__expand("fixtures/app/controllers/examples_controller.rb")

    def __expand(self, path):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

    def test_list_from_config(self):
        # should convert pattern (i.e. */test/*.js) to formatter
        related_files = Related(self.__file(), self.__patterns())

        self.assertEqual(related_files.all(), [
          "fixtures/app/views/examples/show.html",
          "fixtures/app/views/examples/index.html",
          "fixtures/test/controllers/examples_controller_test.rb",
        ])

if __name__ == '__main__':
    unittest.main()
