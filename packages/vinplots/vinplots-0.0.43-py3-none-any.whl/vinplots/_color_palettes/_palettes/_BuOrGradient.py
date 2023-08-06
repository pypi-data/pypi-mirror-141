
import matplotlib as mpl
import numpy as np
import os

def _parse_stored_file():
    
    f = open(os.path.join(os.path.dirname(__file__), "BuOr.txt"))

    color_list = []
    for l in f.readlines():
        color_list.append(l.strip("\n").split(" "))
    
    return np.array(color_list).astype(float)

def _BuOrGradient(n=False):
    
    """Returns _BuOrGradient."""
    
    BuOrCmap = _parse_stored_file() # np.array
    
    if n:
        return BuOrCmap[np.linspace(1, len(BuOrCmap) - 1, n).astype(int)] / 255
    else:
        return mpl.colors.ListedColormap(BuOrCmap / 255)