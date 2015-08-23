import os.path
import os
from jinja2 import Environment, PackageLoader
from .ui.editor import Editor
from .ui.outputpane import OutputPane
from .ui.replpane import REPLPane, find_microbit
from .resources import load_svg

# The encoding to use for reading/writing files
ENCODING = 'utf8'

env = Environment(
    loader=PackageLoader(__name__, 'templates')
)


class Project:
    def __init__(self, root, metadata):
        self.root = root
        self.name = os.path.basename(root)
        self.metadata = metadata

    def abspath(self, path):
        return os.path.join(self.root, path)

    def read_file(self, path):
        with open(self.abspath(path), 'rU', encoding=ENCODING) as f:
            return f.read()

    def write_file(self, path, data):
        with open(self.abspath(path), 'w', encoding=ENCODING) as f:
            f.write(data)

    def from_template(self, path_template, contents_template_name):
        """Render a templated source file to theself project directory."""
        tmpl = env.get_template(contents_template_name)
        contents = tmpl.render(**self.metadata)
        path = path_template.format(**self.metadata)
        self.write_file(path, contents)

    def create(self):
        """Create the initial files in the project."""
        raise NotImplementedError("Projects must implement create()")


class HelloWorld(Project):
    NAME = "Hello World"
    DESCRIPTION = """
    Create a simple Python program to print out "Hello World!"."""

    def init_files(self):
        """Create the files for the project."""
        try:
            os.makedirs(self.root)
        except FileExistsError:
            pass
        self.from_template('hello_world.py', 'hello_world.py.tmpl')

    def build_ui(self, parent=None):
        self.ui = Editor(self, parent=parent)
        self.ui.add_svg('About Hello World', load_svg('about_hello_world.svg'))
        self.ui.add_tab('hello_world.py')
        self.outputpane = OutputPane(parent=self.ui)
        self.ui.add_pane(self.outputpane)
        mb_port = find_microbit()
        if mb_port:
            port = '/dev/{}'.format(mb_port)
            print(port)
            self.replpane = REPLPane(port=port, parent=self.ui)
            self.ui.add_pane(self.replpane)
        return self.ui

    def run(self):
        self.ui.save_all()
        self.outputpane.run('python3', 'hello_world.py', cwd=self.root)


# This is a list of all the project templates we know how to build
PROJECTS = [
    HelloWorld,
]
