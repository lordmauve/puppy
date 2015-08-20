import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout
from PyQt5.Qsci import QsciScintilla

from project_tree import ProjectTree

# FIXME: project chooser needed
ROOT = '/home/mauve/dev/puppy'


class EditorPane(QsciScintilla):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure()

    def configure(self):
        """Set up the editor component."""
        self.setUtf8(True)
        self.setAutoIndent(True)
        self.setIndentationsUseTabs(False)
        self.setBackspaceUnindents(True)
        self.setIndentationWidth(4)
        self.setTabWidth(4)
        self.setEdgeColumn(79)
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, 50)


class Puppy(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        #self.setWindowIcon(QtGui.QIcon(os.path.join("Resources", "images", "Icon")))
        self.setWindowTitle("Puppy IDE")

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.editor = EditorPane()
        self.tree = ProjectTree(ROOT, self)

        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.editor)


app = QApplication(sys.argv)

main = Puppy()
main.show()
sys.exit(app.exec_())
