import pandas as pd
import numpy as np


class _SHAREseq:
    def __init__(self):

        self.celltypes = np.array(
            [
                "alpha-high-CD34+ Bulge",
                "alpha-low-CD34+ Bulge",
                "Isthmus",
                "K6+ Bulge/Companion Layer",
                "TAC-1",
                "TAC-2",
                "IRS",
                "Medulla",
                "Hair Shaft - Cuticle/Cortex",
                "ORS",
                "Basal",
                "Spinous",
                "Granular",
                "Infundibulum",
                "Endothelial",
                "Dermal Fibroblast",
                "Dermal Sheath",
                "Dermal Papilla",
                "Macrophage DC",
                "Melanocyte",
                "Sebaceous Gland",
                "Schwann Cell",
                "Mixed",
            ],
        )

        self.colors = np.array(
            [
                "#0F532C",
                "#1D8342",
                "#42B649",
                "#69C4A5",
                "#FDD82F",
                "#FCAE1F",
                "#F57A03",
                "#EF2D1A",
                "#A10109",
                "#660A17",
                "#96CBE8",
                "#149FD7",
                "#0765AC",
                "#427FC2",
                "#8984C0",
                "#6C4CA1",
                "#98479C",
                "#A80864",
                "#491786",
                "#ECE819",
                "#FEC75C",
                "#E84C9D",
                "#161616",
            ],
        )
        self.column_labels = ["celltypes", "colors"]

    def df(self):

        """"""

        return pd.DataFrame(
            np.stack([self.celltypes, self.colors]), index=["celltype", "color"]
        ).T
    
def _SHAREseq_palette():
    
    """Returns SHARE-seq color palette."""
    
    SHAREseq = _SHAREseq()
    return SHAREseq.df()['color'].tolist()