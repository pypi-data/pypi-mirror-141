"""
This package provides some convenient tools to compute transport based dependency measures such as the transport correlation.

Examples
--------
# Compute transport correlation and test for independence
>>> from transport_dependency import tcor, permutation_test
>>> x = [[1, 2, 3],
...     [4, 5, 6],
...     [7, 8., 9]]
>>> y = [1, 0, 0.3]
>>> res = tcor(x, y)
>>> test = permutation_test(x, y, coef=tcor)
>>> p_val = test["p_val"]


Reference
--------
Transport Dependency: Optimal Transport Based Dependency Measures, Thomas Giacomo Nies, Thomas Staudt and Axel Munk, 2021
"""

__version__ = "0.0.1"

from .td_functions import tcor, mtcor, td, mtd
from .independence_test import permutation_test
