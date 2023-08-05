from ngsolve import *
from ngsolve.bvp import BVP
import netgen.meshing as nm
import math

def epsilon(u):
    """"Convenience function for the deformation tensor in linear elasticity

        This function needs ngsolve Grad function to work. As such, it can process GridFunctions and also
        symbolic TestFunctions and TrialFunctions in the variational formulation"""
    return  0.5*(Grad(u)+Grad(u).trans)

def sigma(strain,E,nu):
    """"Calculates the stress tensor in linear isotropic elasticity

        This function implements the stress tensor for an isotropic, linear elastic medium.
        - **parameters**\n
                    `strain` Strain tensor. This typically a GridFunction (3x3, given as 9-dimensional) or
                    an expression derived via the epsilon function in this package from TrialFunctions or TestFunctions\n
                    `E` Young's modulus\n
                    `nu` Poisson coefficient\n"""
    mu = E / 2 / (1 + nu)
    lam = E * nu / ((1 + nu) * (1 - 2 * nu))
    return lam*Trace(strain)*Id(round(math.sqrt(strain.dim))) + 2*mu*strain


def getElasticBilinearForm(fes,E,nu):
    """"Instantiate and initialize a bilinear form for an isotropic linear elasticity problem
            This function implements the stress tensor for an isotropic, linear elastic medium.
            - **parameters**\n
                        `fes` Finite element space, for typical linear elasticity problems, one can use something like
                        fes=H1(mesh, order=2, dim=3), the mesh being an ngsolve mesh. Higher orders give smoother functions, but
                        also require more ressources and pose some problems in direct calculations on the grid because these
                        terms refer to higher order slopes rather than just the value
                        an expression derived via the epsilon function in this package from TrialFunctions or TestFunctions\n
                        `E` Young's modulus\n
                        `nu` Poisson coefficient\n"""
    a = BilinearForm(fes, symmetric=True, condense=True)
    a += (BFI("elasticity", coef=(E, nu)))
    # In 3D, the elastic bilinear form can also be defined explicitly as below, this is equivalent to the pre-implemented BFI
    #v = fes.TestFunction()
    #u = fes.TrialFunction()
    #e=epsilon(v)
    #s=sigma(epsilon(u),E,nu)
    #a+=(s[0]*e[0]+s[1]*e[1]+s[2]*e[2]+s[3]*e[3]+s[4]*e[4]+s[5]*e[5]+s[6]*e[6]+s[7]*e[7]+s[8]*e[8])*dx
    return a



# This is like the additional thermal expansion element described in this paper
    # IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 25, NO. 11, NOVEMBER 2006 https://pubmed.ncbi.nlm.nih.gov/17117771/
def GetIsotropicCompressionLinearContribution(fes, E,nu,compression):
    """Action of isotropic cell contraction.

    In the absence of additional external forces or constraining boundary conditions, the compressio argument dictates
    how much the material will contract under the cellular force
     - **parameters**\n
                        `fes` Finite element space, for typical linear elasticity problems, one can use something like
                        fes=H1(mesh, order=2, dim=3), the mesh being an ngsolve mesh. Higher orders give smoother functions, but
                        also require more ressources and pose some problems in direct calculations on the grid because these
                        terms refer to higher order slopes rather than just the value
                        an expression derived via the epsilon function in this package from TrialFunctions or TestFunctions\n
                        `E` Young's modulus. Can be a number, but also a Coefficient Function if spatially variable\n
                        `nu` Poisson coefficient. Can be a number, but also a Coefficient Function if spatially variable\n
                        `compression` The spontaneous amount of compression induced by the cells. This can also be CoefficientFunction
                        if spatially variable"""
    v = fes.TestFunction()
    e=-Id(v.dim) * compression
    s=sigma(epsilon(v),E,nu)
    return (s[0]*e[0]+s[1]*e[1]+s[2]*e[2]+s[3]*e[3]+s[4]*e[4]+s[5]*e[5]+s[6]*e[6]+s[7]*e[7]+s[8]*e[8])*dx




