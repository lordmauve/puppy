import os
import os.path
from configparser import ConfigParser

from .projects import PROJECTS, ENCODING


# The name of the ini file within each project containing the metadata
INI_FILENAME = 'puppy-project.ini'


class ProjectManager:
    """Manage the list of existing projects."""
    def __init__(self, root):
        self.root = root
        if not os.path.exists(self.root):
            os.makedirs(self.root)

    def __iter__(self):
        """Iterate over the names of existing projects, yielding strings."""
        for p in os.listdir(self.root):
            if os.path.exists(os.path.join(self.root, p, INI_FILENAME)):
                yield p

    def __getitem__(self, key):
        """Get a project by name."""
        inipath = os.path.join(self.root, key, INI_FILENAME)
        if not os.path.exists(inipath):
            raise KeyError(key)

        return self.project_from_ini(inipath)

    def project_from_ini(self, path):
        """Read a project from its ini file."""
        c = ConfigParser()
        c.read([path], encoding='utf8')
        template = c.get('puppy', 'template')
        metadata = dict(c.items('metadata'))

        for p in PROJECTS:
            if p.NAME == template:
                break
        else:
            raise ValueError("Unknown project template")

        return p(os.path.dirname(path), metadata)

    def write_ini(self, project):
        """Write an ini file with metadata for the project."""
        path = os.path.join(project.root, INI_FILENAME)
        config = ConfigParser()
        config.add_section('puppy')
        config.add_section('metadata')
        config.set('puppy', 'template', project.NAME)
        for k, v in project.metadata.items():
            config.set('metadata', k, v)
        with open(path, 'w', encoding=ENCODING) as f:
            config.write(f)

    def init_project(self, name, project_class, metadata={}):
        proj_root = os.path.join(self.root, name)
        proj = project_class(proj_root, {})
        proj.init_files()
        self.write_ini(proj)
        return proj
