try:
    from .version import git_revision as __git__revision__
    from .version import version as __version__
except ImportError:
    __git__revision__ = 'Unknown'
    __version__ = 'Unknown'

from . import math
