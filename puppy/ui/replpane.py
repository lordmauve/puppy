from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QIODevice
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
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setObjectName('replpane')

        # open the serial port
        import pdb; pdb.set_trace()
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
