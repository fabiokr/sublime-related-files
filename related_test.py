import unittest
import os
from related import *


class RelatedTest(unittest.TestCase):

    def __patterns(self):
        return {
          ".+\/app\/controllers\/(.+)_controller.rb": ["app/views/$1/**", "app/helpers/$1_helper.rb"],
          ".+\/app\/(.+).rb": ["test/$1_test.rb"]
        }

    def __file(self):
        return self.__expand("fixtures/example1/app/controllers/examples_controller.rb")

    def __folders(self):
        return [self.__expand("fixtures/example1"), self.__expand("fixtures/example2")]

    def __expand(self, path):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

    def test_list_with_matching_file(self):
        related_files = Related(self.__file(), self.__patterns(), self.__folders())

        self.assertEqual(related_files.all(), [
          [
              "example1/app/helpers/examples_helper.rb",
              self.__expand("fixtures/example1/app/helpers/examples_helper.rb"),
          ],
          [
              "example1/app/views/examples/index.html",
              self.__expand("fixtures/example1/app/views/examples/index.html"),
          ],
          [
              "example1/app/views/examples/show.html",
              self.__expand("fixtures/example1/app/views/examples/show.html"),
          ],
          [
              "example1/test/controllers/examples_controller_test.rb",
              self.__expand("fixtures/example1/test/controllers/examples_controller_test.rb"),
          ]
        ])

    def test_list_with_not_matching_file(self):
        # should convert pattern (i.e. */test/*.js) to formatter
        related_files = Related("/should/not/match", self.__patterns(), self.__folders())

        self.assertEqual(related_files.all(), [])

if __name__ == '__main__':
    unittest.main()
