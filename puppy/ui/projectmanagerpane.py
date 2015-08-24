from functools import partial
from jinja2 import Environment, PackageLoader
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton,
    QTabWidget, QInputDialog
)
from ..projects import PROJECTS

env = Environment(
    loader=PackageLoader(__name__, 'templates')
)


DEFAULT_DETAILS = """<html>
<i>Please select a project to view details.</i>
</html>"""


class ProjectManagerPane(QWidget):
    """UI to select a project to start.

    Users are presented a list of existing projects or the available templates
    to start a new project.

    """

    def __init__(self, main_window, projlist, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.tabs.setObjectName('projectchoosertabs')

        self.layout.addWidget(self.tabs)

        self.projects = QListWidget()
        self.projects.currentItemChanged.connect(self.selected_project)

        self.templates = QListWidget()
        self.templates.currentItemChanged.connect(self.selected_template)

        if any(projlist):
            self.tabs.addTab(self.projects, "Existing Project")
        self.tabs.addTab(self.templates, "New Project")
        self.tabs.currentChanged.connect(self.tab_changed)

        self.detailspane = QVBoxLayout()
        self.layout.addLayout(self.detailspane)
        self.details = QLabel(DEFAULT_DETAILS)

        self.go = QPushButton("Go")
        self.go.setDisabled(True)
        self.go.clicked.connect(self.perform_action)
        self.detailspane.addWidget(self.details)
        self.detailspane.addWidget(self.go)

        self.action = None
        self.main_window = main_window
        self.projlist = projlist
        self.update_choices()

    def update_choices(self):
        for p in PROJECTS:
            self.templates.addItem(p.NAME)

        for name in self.projlist:
            self.projects.addItem(name)

    def tab_changed(self, index):
        """Called when the active tab is changed."""
        print("Selected tab", index)
        if self.tabs.tabText(index) == "New Project":
            self.selected_template()
        else:
            self.selected_project()

    def deselected(self):
        self.details.setText(DEFAULT_DETAILS)
        self.go.setDisabled(True)
        self.action = None

    def selected_project(self, *args):
        key = self.projects.currentItem().text()
        project = self.projlist[key]
        tmpl = env.get_template('project_details.html')
        self.details.setText(tmpl.render(project=project))
        self.go.setDisabled(False)
        self.action = partial(self.open_project, project)

    def selected_template(self, *args):
        key = self.templates.currentItem().text()
        tmpl = env.get_template('template_details.html')
        project = next(p for p in PROJECTS if p.NAME == key)
        self.details.setText(tmpl.render(project=project))
        self.go.setDisabled(False)
        self.action = partial(self.new_project, project)

    def perform_action(self):
        if not self.action:
            pass
        self.action()

    def new_project(self, project):
        dlg = QInputDialog()
        dlg.setLabelText("Please enter a name for your new %s project" % project.NAME)
        dlg.setOkButtonText("Create project")
        res = dlg.exec()
        if not res:
            return
        name = dlg.textValue()
        proj = self.projlist.init_project(name, project)
        self.main_window.add_project(proj)

    def open_project(self, proj):
        self.main_window.add_project(proj)
