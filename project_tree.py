from PyQt5.QtWidgets import QTreeView, QFileSystemModel


class ProjectTree(QTreeView):
    def __init__(self, root, parent=None):
        QTreeView.__init__(self, parent)

        self.setAnimated(True)
        self.setAutoScroll(True)
        self.setObjectName("ProjectTree")

        self.model = QFileSystemModel()
        self.model.setRootPath(root)
        self.model.setNameFilterDisables(False)
        self.setModel(self.model)
        self.setColumnWidth(0, 300)
