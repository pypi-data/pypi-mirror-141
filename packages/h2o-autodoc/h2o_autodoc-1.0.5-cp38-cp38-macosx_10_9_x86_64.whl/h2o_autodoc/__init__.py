import warnings

from h2o_autodoc.config.config import Config
from h2o_autodoc.h2o3.autodoc import render_autodoc

try:
    from . import build_info as bi

    __version__ = {n: getattr(bi, n) for n in dir(bi) if not n.startswith("__")}
except ImportError:
    __version__ = {}

warnings.filterwarnings("ignore", category=DeprecationWarning)
