# my_project/__version__.py
name = "interpolation"
__version__ = "0.0.1"
description = ("Input temperature (csv) data is interpolated and visualized "
               "using MetPy, cartopy, matplotlib, numpy and pandas packages, and saved to png.")
python = "3.12"
install_requires = "requirements.txt"
features ={
    "INTPOL-1": ["Implement temperature interpolation and mapping"],
    "INTPOL-2": ["Implement add metpy logo on the map"],
    "INTPOL-3": ["Add reference date and time and write it on the map"],
    "INTPOL-4": ["Implement tight-layout"]
    }
