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
import os.path
from PyQt5.QtWidgets import (
    QApplication, QSplashScreen, QStackedWidget, QDesktopWidget
)

from .resources import load_icon, load_pixmap
from .projects import HelloWorld

# We should probably create a default directory within this directory.
ROOT = os.path.expanduser('~/puppy-projects/')


class Puppy(QStackedWidget):
    """
    Represents the application.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Gotta have a nice icon.
        self.setWindowIcon(load_icon('icon'))
        self.update_title()

        # Ensure we have a minimal sensible size for the application.
        self.setMinimumSize(800, 600)
        self.projects = {}

    def update_title(self, project=None):
        title = "Puppy IDE"
        if project:
            title += ' - ' + project.root
        self.setWindowTitle(title)

    def add_project(self, project):
        """Add a project to the UI and show it."""
        if project.name in self.projects:
            return
        self.projects[project.name] = project
        self.addWidget(project.build_ui(self))
        self.update_title(project)

    def autosize_window(self):
        screen = QDesktopWidget().screenGeometry()
        w = int(screen.width() * 0.8)
        h = int(screen.height() * 0.8)
        self.resize(w, h)
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2
        )


def main():
    # The app object is the application running on your computer.
    app = QApplication(sys.argv)

    # A splash screen is a logo that appears when you start up the application.
    # The image to be "splashed" on your screen is in the resources/images
    # directory.
    splash = QSplashScreen(load_pixmap('splash'))
    # Show the splash.
    splash.show()

    # Make the editor with the Brian class defined above.
    the_editor = Puppy()

    proj_root = os.path.join(ROOT, 'hello_world')
    proj = HelloWorld(proj_root, {})
    if not os.path.isdir(proj_root):
        proj.init_files()
    the_editor.add_project(proj)

    the_editor.show()
    the_editor.autosize_window()

    # Remove the splash when the_editor has finished setting itself up.
    splash.finish(the_editor)

    # Stop the program after application finishes executing.
    sys.exit(app.exec_())
