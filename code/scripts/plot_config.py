"""Shared matplotlib config for Chinese academic figures."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def setup_style():
    plt.rcParams.update({
        "font.sans-serif": ["Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei", "Noto Sans CJK JP"],
        "font.family": "sans-serif",
        "axes.unicode_minus": False,
        "font.size": 13,
        "axes.titlesize": 0,
        "axes.labelsize": 13,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 10,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })

# Standard academic figure sizes (inches)
FIG_WIDE = (10, 5.5)      # full-width figure
FIG_SQUARE = (7, 6)       # heatmap / correlation matrix
FIG_HALF = (7, 4.5)       # half-width figure
FIG_TALL = (7, 7)         # tall diagnostic
