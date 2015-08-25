import os.path
import os
import datetime
from configparser import ConfigParser
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

    def ensure_root(self):
        """Ensure the root directory for this project exists."""
        try:
            os.makedirs(self.root)
        except FileExistsError:
            pass

    def from_template(self, path_template, contents_template_name, **params):
        """Render a templated source file to theself project directory."""
        tmpl = env.get_template(contents_template_name)
        template_params = {
            'project': self,
        }
        template_params.update(self.metadata)
        template_params.update(params)
        contents = tmpl.render(**template_params)
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
        self.ensure_root()
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


class PythonScript(Project):
    NAME = "Python Script"
    DESCRIPTION = """
    Create a Python program.

    This is suitable for processing text input, generating output, or
    manipulating files on disk.

    """

    def __init__(self, root, metadata):
        super().__init__(root, metadata)
        if 'py_file' not in self.metadata:
            self.metadata['py_file'] = self.name + '.py'

    @property
    def py_file(self):
        return self.metadata['py_file']

    def init_files(self):
        """Create the files for the project."""
        self.ensure_root()
        self.from_template(
            self.py_file,
            'py_file.py.tmpl',
            date=datetime.date.today()
        )
        self.from_template('README.md', 'readme.md.tmpl')

    def build_ui(self, parent=None):
        self.ui = Editor(self, parent=parent)
        self.outputpane = OutputPane()
        self.ui.add_tab('README.md')
        self.ui.add_tab(self.py_file)
        self.ui.add_pane(self.outputpane)
        return self.ui

    def run(self):
        self.ui.save_all()
        self.outputpane.run('python3', self.py_file, cwd=self.root)


# This is a list of all the project templates we know how to build
PROJECTS = [
    HelloWorld,
    PythonScript,
]
