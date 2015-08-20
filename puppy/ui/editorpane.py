import sys
import keyword
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QColor, QFont


# FONT related constants:
DEFAULT_FONT_SIZE = 12
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

    def needs_write(self):
        return self.isModified()
