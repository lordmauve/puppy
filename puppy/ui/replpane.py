from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QIODevice
from PyQt5.QtSerialPort import QSerialPort

# TODO:
#   - shutdown serial port cleanly on exit
#   - use monospace font
#   - get backspace and arrow keys working

class REPLPane(QTextEdit):
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setObjectName('replpane')

        # open the serial port
        self.serial = QSerialPort(self)
        self.serial.setPortName(port)
        self.serial.setBaudRate(115200)
        print(self.serial.open(QIODevice.ReadWrite))
        self.serial.readyRead.connect(self.on_serial_read)

        # clear the text
        self.clear()

    def on_serial_read(self):
        self.append(self.serial.readAll())

    def keyPressEvent(self, data):
        self.serial.write(bytes(data.text(), 'utf8'))

    def append(self, txt):
        tc = self.textCursor()
        tc.movePosition(QTextCursor.End)
        self.setTextCursor(tc)
        self.insertPlainText(str(txt, 'utf8'))
        self.ensureCursorVisible()

    def clear(self):
        self.setText('')

    def kill(self):
        if self.serial.isOpen():
            self.serial.close()
