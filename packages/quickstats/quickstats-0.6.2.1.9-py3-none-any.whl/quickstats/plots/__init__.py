import quickstats

from .color_schemes import *
from .abstract_plot import AbstractPlot
from .hypotest_inverter_plot import HypoTestInverterPlot
from .score_distribution_plot import score_distribution_plot
from .test_statistic_distribution_plot import TestStatisticDistributionPlot
from .upper_limit_1D_plot import UpperLimit1DPlot
from .upper_limit_2D_plot import UpperLimit2DPlot
from .upper_limit_benchmark_plot import UpperLimitBenchmarkPlot
from .likelihood_1D_plot import Likelihood1DPlot
from .pdf_distribution_plot import PdfDistributionPlot

from matplotlib import style, colors

# Reference from https://github.com/beojan/atlas-mpl

style.core.USER_LIBRARY_PATHS.append(quickstats.stylesheet_path)
style.core.reload_library()
style.use("quick_default")

colors.EXTRA_COLORS = EXTRA_COLORS
colors.colorConverter.colors.update(EXTRA_COLORS)