"""Provide preconfigured functions, linear and bilinear forms for elasticity simualtion
"""

__all__ = ["eigenvalue_ratio","eigenvalue_ratio_xy",
           "most_compressive_eigenvector","least_compressive_eigenvector",
           "most_compressive_eigenvector_xy", "least_compressive_eigenvector_xy",
           "d_direction",
           "add_d",
           "stretch_ratio_xy",
           "least_compressive_direction_xy",
           "most_compressive_direction_xy"
           ]



# Import from the sub files
from .single_strain import eigenvalue_ratio
from .single_strain import eigenvalue_ratio_xy
from .single_strain import most_compressive_eigenvector
from .single_strain import least_compressive_eigenvector
from .single_strain import most_compressive_eigenvector_xy
from .single_strain import least_compressive_eigenvector_xy

from .strain_addition import d_direction
from .strain_addition import add_d
from .strain_addition import stretch_ratio_xy
from .strain_addition import least_compressive_direction_xy
from .strain_addition import most_compressive_direction_xy



