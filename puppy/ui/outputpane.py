from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QProcess, QProcessEnvironment, QIODevice

# Encoding for the subprocess' output
# We will request this (for Python processes) using PYTHONIOENCODING
ENCODING = 'utf8'


class OutputPane(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None
        self.setAcceptRichText(False)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)

    def append(self, txt):
        tc = self.textCursor()
        tc.movePosition(QTextCursor.End)
        self.setTextCursor(tc)
        self.insertPlainText(txt)
        self.ensureCursorVisible()

    def clear(self):
        self.setText('')

    def get_subprocess_env(self):
        """Get the environment variables for running the subprocess."""
        return {'PYTHONIOENCODING': ENCODING}

    def run(self, *args, cwd=None):
        env = QProcessEnvironment().systemEnvironment()
        for k, v in self.get_subprocess_env().items():
            env.insert(k, v)

        self.process = QProcess(self)
        self.process.setProcessEnvironment(env)
        if cwd:
            self.process.setWorkingDirectory(cwd)
        # self.process.error.connect(self.on_error)
        # self.process.stateChanged.connect(self.stateChanged)
        self.process.readyReadStandardOutput.connect(self.on_stdout_read)
        self.process.readyReadStandardError.connect(self.on_stderr_read)
        self.process.finished.connect(self.on_process_end)

        self.clear()
        self.process.start(args[0], args[1:], QIODevice.ReadWrite)

    def on_stdout_read(self):
        while self.process and self.process.canReadLine():
            text = self.process.readLine().data().decode(ENCODING)
            self.append(text)

    def on_stderr_read(self):
        text = self.process.readAllStandardError().data().decode(ENCODING)
        self.append(text)

    def kill(self):
        if self.process:
            self.process.kill()

    def on_process_end(self):
        self.process = None
