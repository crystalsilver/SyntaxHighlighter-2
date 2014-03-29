import sublime
import string
import random
import functools
import sublime_plugin
from xml.dom.minidom import *
import os.path
import webbrowser
import cgi


class HightlightInBrowserCommand(sublime_plugin.TextCommand):
    EXTENSION_DIR = os.path.dirname(__file__) + "/"
    TEMP_PATH = EXTENSION_DIR + "temp/"
    SYNTAX_HIGHLIGHTER_PATH = EXTENSION_DIR + "syntaxhighlighter_3.0.83/"

    BRUSHES = {'Javascript': 'JScript'}

    def __init__(self, view):
        self.view = view
        self.clean_temp()

    def clean_temp(self):
        for file in os.listdir(self.TEMP_PATH):
            os.remove(self.TEMP_PATH + file)

    def get_language(self):
        syntax = self.view.settings().get('syntax')
        print(syntax)
        if syntax is not None:
            return os.path.basename(syntax).replace(
                '.tmLanguage', '').lower().capitalize()
        else:
            return "plain"

    def run(self, edit):
        """
        Main plugin logic for the 'indent' command.
        """
        webbrowser.open_new_tab("file://" + self.generate_file(
            self.read_file(self.view.file_name())))

    def read_file(self, path):
        handle = open(path, "r")
        code = handle.read()
        handle.close()
        return code

    def write_file(self, path, content):
        handle = open(path, "w")
        handle.write(content)
        handle.close()

    def generate_file(self, content):
        chars = string.ascii_uppercase + string.digits

        tempPath = self.TEMP_PATH + functools.reduce(
            lambda acc, x: random.choice(chars) + acc, range(12), ".html")
        self.write_file(tempPath, self.generate_html(cgi.escape(content)))
        return tempPath

    def generate_html(self, content):
        brush = self.get_brush()
        return (self.read_file(self.EXTENSION_DIR + 'template.html')
                % (brush, brush.lower(), content))  # redo

    def get_brush(self):
        language = self.get_language()
        if language in self.BRUSHES:
            return self.BRUSHES[language]
        else:
            return language
