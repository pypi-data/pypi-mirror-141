"""Provide preconfigured functions, linear and bilinear forms for elasticity simualtion
"""

__all__ = ["epsilon","sigma","getElasticBilinearForm","GetIsotropicCompressionLinearContribution"]



# Basic tools
from .simulation import epsilon
from .simulation import sigma
from .simulation import getElasticBilinearForm
from .simulation import GetIsotropicCompressionLinearContribution
