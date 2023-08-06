# __init__.py

__module_name__ = "__init__.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])

# package imports #
# --------------- #
import matplotlib as _mpl
import matplotlib.font_manager as _font_manager
import os as _os

from ._utilities._get_mscorefonts import _get_mscorefonts

# matplotlib rcParams #
# ------------------- #

# install mscorefonts and clear the previous parameter cache file.
_os.system("rm ~/.cache/matplotlib -rf")
_mscore_install = _get_mscorefonts()

_font = {"size": 12}
_mpl.rc(_font)
_mpl.rcParams["font.sans-serif"] = "Arial"
_mpl.rcParams["font.family"] = "sans-serif"


# import sub-packages and Plot module #
# ----------------------------------- #
from ._plot._PlotModule import _Plot as Plot
from . import _color_palettes as colors
