"""
Puppy IDE.

Copyright (C) 2015 Dan Pope and Nicholas H.Tollervey

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import os
import keyword
from os.path import expanduser
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QHBoxLayout,
                             QSplashScreen, QTabWidget, QToolBar, QAction)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import QSize, Qt
from PyQt5.Qsci import QsciScintilla, QsciLexerPython


# We should probably create a default directory within this directory.
ROOT = expanduser('~')


# FONT related constants:
DEFAULT_FONT_SIZE = 16
DEFAULT_FONT = 'Bitstream Vera Sans Mono'
# Platform specific alternatives...
if sys.platform == 'win32':
    DEFAULT_FONT = 'Consolas'
elif sys.platform == 'darwin':
    DEFAULT_FONT = 'Monaco'


class PythonLexer(QsciLexerPython):
    """
    Defines the styles associated with various types of token used in Python.
    """

    # The names of tokens and their associated id used by Scintilla
    # (apparently).
    token_id = {
        'Default': 0,
        'Comment': 1,
        'Number': 2,
        'DoubleQuotedString': 3,
        'SingleQuotedString': 4,
        'Keyword': 5,
        'TripleSingleQuotedString': 6,
        'TripleDoubleQuotedString': 7,
        'ClassName': 8,
        'FunctionMethodName': 9,
        'Operator': 10,
        'Identifier': 11,
        'CommentBlock': 12,
        'UnclosedString': 13,
        'HighlightedIdentifier': 14,
        'Decorator': 15,
    }

    # Each token type is associated with a list containing the font to use,
    # the font colour, the font size, bold flag, italic flag, and background
    # colour.
    default_style = {
        'UnclosedString': [DEFAULT_FONT, '#000000', DEFAULT_FONT_SIZE, False,
                           False, '#00fd00'],
        'Decorator': [DEFAULT_FONT, '#00cc00', DEFAULT_FONT_SIZE, False, False,
                      '#ffffff'],
        'Default': [DEFAULT_FONT, '#000000', DEFAULT_FONT_SIZE, False, False,
                    '#ffffff'],
        'HighlightedIdentifier': [DEFAULT_FONT, '#900090', DEFAULT_FONT_SIZE,
                                  False, False, '#ffffff'],
        'CommentBlock': [DEFAULT_FONT, '#0000ff', DEFAULT_FONT_SIZE, False,
                         False, '#ffffff'],
        'FunctionMethodName': [DEFAULT_FONT, '#0000ff', DEFAULT_FONT_SIZE,
                               False, False, '#ffffff'],
        'DoubleQuotedString': [DEFAULT_FONT, '#00aa00', DEFAULT_FONT_SIZE,
                               False, False, '#ffffff'],
        'Operator': [DEFAULT_FONT, '#000000', DEFAULT_FONT_SIZE, False, False,
                     '#ffffff'],
        'TripleSingleQuotedString': [DEFAULT_FONT, '#00aa00',
                                     DEFAULT_FONT_SIZE, False, False,
                                     '#ffffff'],
        'Number': [DEFAULT_FONT, '#000000', DEFAULT_FONT_SIZE, False, False,
                   '#ffffff'],
        'Keyword': [DEFAULT_FONT, '#0000ff', DEFAULT_FONT_SIZE, False, False,
                    '#ffffff'],
        'Identifier': [DEFAULT_FONT, '#000000', DEFAULT_FONT_SIZE, False,
                       False, '#ffffff'],
        'ClassName': [DEFAULT_FONT, '#0000ff', DEFAULT_FONT_SIZE, False, False,
                      '#ffffff'],
        'SingleQuotedString': [DEFAULT_FONT, '#00aa00', DEFAULT_FONT_SIZE,
                               False, False, '#ffffff'],
        'TripleDoubleQuotedString': [DEFAULT_FONT, '#00aa00',
                                     DEFAULT_FONT_SIZE, False, False,
                                     '#ffffff'],
        'Comment': [DEFAULT_FONT, '#0000ff', DEFAULT_FONT_SIZE, False, False,
                    '#ffffff']
    }

    def __init__(self):
        QsciLexerPython.__init__(self)
        for key, attrib in self.default_style.items():
            value = self.token_id[key]
            self.setColor(QColor(attrib[1]), value)
            self.setEolFill(True, value)
            self.setPaper(QColor(attrib[5]), value)
            self.setPaper(QColor(attrib[5]), value)

            font = QFont(attrib[0], attrib[2])
            font.setBold(attrib[3])
            font.setItalic(attrib[4])
            self.setFont(font, value)
        self.setDefaultPaper(QColor("#ffffff"))

    def keywords(self, flag):
        """
        Returns a list of Python keywords.
        """
        if flag == 1:
            return ' '.join(keyword.kwlist)
        return ' '.join(dir(__builtins__))


class EditorPane(QsciScintilla):
    """
    Represents the text editor.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure()

    def configure(self):
        """Set up the editor component."""
        # Font information
        font = QFont(DEFAULT_FONT)
        font.setFixedPitch(True)
        font.setPointSize(DEFAULT_FONT_SIZE)
        self.setFont(font)
        # Generic editor settings
        self.setUtf8(True)
        self.setAutoIndent(True)  # DOES NOT SEEM TO DO ANYTHING!!!?!?!!
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setTabWidth(4)
        self.setEdgeColumn(79)
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, 50)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        # Use the lexer defined above
        lexer = PythonLexer()
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)


class ButtonBar(QToolBar):
    """
    Represents the bar of buttons across the top of the editor and defines
    their behaviour.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.configure()

    def configure(self):
        """Set up the buttons"""
        self.setMovable(False)
        self.setIconSize(QSize(64, 64))
        self.setToolButtonStyle(3)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("StandardToolBar")
        # Create actions to be added to the button bar.
        self.new_python_file_act = QAction(
            QIcon(os.path.join("resources", "images", "new")),
            "New", self,
            statusTip="Create a new Python file",
            triggered=self._new_python_file)
        self.open_python_file_act = QAction(
            QIcon(os.path.join("resources", "images", "open")),
            "Open", self,
            statusTip="Open a Python file",
            triggered=self._open_python_file)
        self.save_python_file_act = QAction(
            QIcon(os.path.join("resources", "images", "save")),
            "Save", self,
            statusTip="Save a Python file",
            triggered=self._save_python_file)
        self.run_python_file_act = QAction(
            QIcon(os.path.join("resources", "images", "run")),
            "Run", self,
            statusTip="Run your Python file",
            triggered=self._run_python_file)
        self.build_python_file_act = QAction(
            QIcon(os.path.join("resources", "images", "build")),
            "Build", self,
            statusTip="Build Python into Hex file",
            triggered=self._build_python_file)
        self.zoom_in_act = QAction(
            QIcon(os.path.join("resources", "images", "zoom-in")),
            "Zoom in", self,
            statusTip="Make the text bigger",
            triggered=self._zoom_in)
        self.zoom_out_act = QAction(
            QIcon(os.path.join("resources", "images", "zoom-out")),
            "Zoom out", self,
            statusTip="Make the text smaller",
            triggered=self._zoom_out)
        self.help_act = QAction(
            QIcon(os.path.join("resources", "images", "help")),
            "Help", self,
            statusTip="Help about this editor",
            triggered=self._help)
        # Add the actions to the button bar.
        self.addAction(self.new_python_file_act)
        self.addAction(self.open_python_file_act)
        self.addAction(self.save_python_file_act)
        self.addSeparator()
        self.addAction(self.run_python_file_act)
        self.addAction(self.build_python_file_act)
        self.addSeparator()
        self.addAction(self.zoom_in_act)
        self.addAction(self.zoom_out_act)
        self.addAction(self.help_act)

    def _new_python_file():
        """
        Handle the creation of a new Python file.
        """
        pass

    def _open_python_file():
        """
        Handle opening an existing Python file.
        """
        pass

    def _save_python_file():
        """
        Save the current Python file.
        """
        pass

    def _run_python_file():
        """
        Attempt to run the current file.
        """
        pass

    def _build_python_file():
        """
        Generate a .hex file to flash onto a micro:bit.
        """
        pass

    def _zoom_in():
        """
        Make the text BIGGER.
        """
        pass

    def _zoom_out():
        """
        Make the text smaller.
        """
        pass

    def _help():
        """
        Display some help about the editor.
        """
        pass


class Puppy(QWidget):
    """
    Represents the application.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Gotta have a nice icon.
        self.setWindowIcon(QIcon(os.path.join('resources', 'images', 'icon')))
        self.setWindowTitle("Puppy IDE")
        # Vertical box layout.
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # The application has two aspects to it: buttons and the editor.
        self.buttons = ButtonBar()
        self.editor = EditorPane()
        # Add the buttons and editor to the user inteface.
        self.layout.addWidget(self.buttons)
        self.layout.addWidget(self.editor)
        # Ensure we have a minimal sensible size for the application.
        self.setMinimumSize(800, 600)


# The app object is the application running on your computer.
app = QApplication(sys.argv)

# A splash screen is a logo that appears when you start up the application.
# The image to be "splashed" on your screen is in the resources/images
# directory.
splash = QSplashScreen(QPixmap(os.path.join('resources', 'images', 'splash')))
# Show the splash.
splash.show()

# Make the editor with the Brian class defined above.
the_editor = Puppy()
the_editor.show()

# Remove the splash when the_editor has finished setting itself up.
splash.finish(the_editor)

# Stop the program after application finishes executing.
sys.exit(app.exec_())
