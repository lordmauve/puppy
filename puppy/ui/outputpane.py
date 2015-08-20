from PyQt5.QWidgets import QTextEdit, QTextCursor


class OutputPane(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)

    def append(self, txt):
        tc = self.textCursor()
        tc.movePosition(QTextCursor.End)
        self.setTextCursor(tc)
        self.insertPlainText(txt)
        self.ensureCursorVisible()
