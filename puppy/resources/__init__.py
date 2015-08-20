from pkg_resources import resource_filename

from PyQt5.QtGui import QPixmap, QIcon


def path(name):
    return resource_filename(__name__, "images/" + name)


def load_icon(name):
    """Load an icon from the resources directory."""
    return QIcon(path(name))


def load_pixmap(name):
    """Load a pixmap from the resources directory."""
    return QPixmap(path(name))
