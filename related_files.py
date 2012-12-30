import sublime
import sublime_plugin
from related import *


class RailsRelatedFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit, index):
        if index >= 0:
            self.open_file(index)
        else:
            try:
                self.__build_related_files()
                sublime.active_window().show_quick_panel(self.__files(), self.open_file)
            except:
                return False

    # Opens the file in path.
    def __open_file(self, index):
        if index >= 0:
            sublime.active_window().open_file(os.path.join(self.__get_working_dir(), self.files[index]))

    # Builds a list of related files for the current open file.
    def __build_related_files(self):
        self.files = Related(self.__active_file_path(), self.__patterns()).all()

    # Retrieves the patterns from settings.
    def __patterns(self):
        return sublime.load_settings("RelatedFiles.sublime-settings").get('patterns')

    # Returns the activelly open file path from sublime.
    def __active_file_path(self):
        view = self.view
        if view and view.file_name() and len(view.file_name()) > 0:
            return view.file_name()

    # Returns the working dir from the active file, or the first one available
    # from sublime.
    def __get_working_dir(self):
        file_path = self.__active_file_path()
        if file_path:
            return os.path.dirname(file_path)
        else:
            return self.window.folders()[0]
