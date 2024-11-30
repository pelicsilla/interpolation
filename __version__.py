# my_project/__version__.py
name = "interpolation"
__version__ = "0.0.1"
description = ("Input temperature (csv) data is interpolated and visualized "
               "using MetPy, cartopy, matplotlib, numpy and pandas packages, and saved to png.")
python = "3.12"
install_requires = "MetPy, cartopy, matplotlib, numpy, pandas"
features ={
    "MATH-1": ["Implement temperature interpolation and mapping"],
    "MATH-2": ["Implement add metpy logo on the map"]
    }
