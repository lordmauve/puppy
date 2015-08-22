from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

# TODO:
#   - shutdown serial port cleanly on exit
#   - use monospace font
#   - get backspace and arrow keys working

MICROBIT_PID = 516
MICROBIT_VID = 3368


def find_microbit():
    """
    Returns the port for the first microbit it finds connected to the host
    computer. If no microbit is found, returns None.
    """
    available_ports = QSerialPortInfo.availablePorts()
    for port in available_ports:
        pid = port.productIdentifier()
        vid = port.vendorIdentifier()
        if pid == MICROBIT_PID and vid == MICROBIT_VID:
            return port.portName()
    return None


class REPLPane(QTextEdit):
    """
    REPL = Read, Evaluate, Print, Loop.

    This widget represents a REPL client connected to a BBC micro:bit.
    """
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setObjectName('replpane')
        # A flag to indicate that we've sent some sort of escape
        # character e.g. \b
        self.escape_flag = False

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
        self.escape_flag = False
        text = data.text()
        msg = bytes(text, 'utf8')
        key = data.key()
        if key == Qt.Key_Backspace:
            msg = '\b'
            self.delete()
            self.escape_flag = True
        elif key == Qt.Key_Up:
            msg = '\x1B[A'
        elif key == Qt.Key_Down:
            msg = '\x1B[B'
        self.serial.write(msg)

    def append(self, data):
        txt = str(data, 'utf8')
        if self.escape_flag:
            return
        tc = self.textCursor()
        tc.movePosition(QTextCursor.End)
        self.setTextCursor(tc)
        self.insertPlainText(txt)
        self.ensureCursorVisible()

    def delete(self):
        tc = self.textCursor()
        block_text = tc.block().text()
        if not (block_text.startswith('>>> ') or
                block_text.startswith('... ')):
            return
        if block_text in [">>> ", "... "]:
            return
        tc.deletePreviousChar()

    def clear(self):
        self.setText('')

    def kill(self):
        if self.serial.isOpen():
            self.serial.close()
