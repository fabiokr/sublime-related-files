import sublime
import sublime_plugin
from related import *


class RailsRelatedFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit, index):
        if index >= 0:
            self.open_file(index)
        else:
            self.__build_related_files()
            sublime.active_window().show_quick_panel(self.description_related_files, self.__open_file)

    # Opens the file in path.
    def __open_file(self, index):
        if index >= 0:
            sublime.active_window().open_file(self.related_files[index])

    # Builds a list of related files for the current open file.
    def __build_related_files(self):
        related_files = Related(self.__active_file_path(), self.__patterns(), sublime.active_window().folders()).all()
        self.description_related_files = [file[0] for file in related_files]
        self.related_files = [file[1] for file in related_files]

    # Retrieves the patterns from settings.
    def __patterns(self):
        return sublime.load_settings("RelatedFiles.sublime-settings").get('patterns')

    # Returns the activelly open file path from sublime.
    def __active_file_path(self):
        view = self.view
        if view and view.file_name() and len(view.file_name()) > 0:
            return view.file_name()
