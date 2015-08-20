import os.path
import os
from jinja2 import Environment, PackageLoader
from .ui.editor import Editor

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
        self.ui.add_tab('hello_world.py')
        return self.ui


# This is a list of all the project templates we know how to build
PROJECTS = [
    HelloWorld,
]
