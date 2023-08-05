import math
from numpy import linalg
from numpy import real

# These functions need strain values, the identity contribution is added here
def eigenvalue_ratio(s):
    """"Ratio of largest to smallest extension eigenvalue

        - **parameters**\n
            `s` Strain tensor. This is the elements of a numericla 3x3 matrix but arranged as 9-vector"""
    e=linalg.eigvals([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]], [s[6], s[7], 1 + s[8]]])
    return max(real(e))/min(real(e))

def eigenvalue_ratio_xy(s):
    """"Ratio of largest to smallest extension eigenvalue in the xy-plane

        - **parameters**\n
                `s` Strain tensor. This is the elements of a numericla 3x3 matrix but arranged as 9-vector"""
    e=linalg.eigvals([[1 + s[0], s[1]], [s[3], 1 + s[4]]])
    return max(real(e))/min(real(e))



def most_compressive_eigenvector(s):
    """"Direction showing the highest compression, calculated as the eigenvector with the lowest eigenvalue

            - **parameters**\n
                    `s` Strain tensor. This is the elements of a numericla 3x3 matrix but arranged as 9-vector"""
    e=linalg.eigvals([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]],[s[6],s[7],s[8]+1]])
    if(e[0]<e[1] and e[0]<e[2]):
        return linalg.eig([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]],[s[6],s[7],s[8]+1]])[1][0]
    else:
        if(e[0]<e[1]):
            return linalg.eig([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]],[s[6],s[7],s[8]+1]])[1][1]
        else:
            return linalg.eig([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]], [s[6], s[7], s[8] + 1]])[1][1]

def least_compressive_eigenvector(s):
    """"Direction showing the least compression, calculated as the eigenvector with the highest eigenvalue
             - **parameters**\n
                        `s` Strain tensor. This is the elements of a numericla 3x3 matrix but arranged as 9-vector"""
    e=linalg.eigvals([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]],[s[6],s[7],s[8]+1]])
    if(e[0]>e[1] and e[0]>e[2]):
        return linalg.eig([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]],[s[6],s[7],s[8]+1]])[1][0]
    else:
        if(e[0]>e[1]):
            return linalg.eig([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]],[s[6],s[7],s[8]+1]])[1][1]
        else:
            return linalg.eig([[1 + s[0], s[1], s[2]], [s[3], 1 + s[4], s[5]], [s[6], s[7], s[8] + 1]])[1][1]


def most_compressive_eigenvector_xy(s):
    """"Direction showing the highest compression, calculated as the eigenvector with the highest eigenvalue

        This function calculates the eigenvector with the highest eigenvalue, restricting analysis to the xy-plane
        - **parameters**\n
                            `s` Strain tensor. This is the elements of a numericla 3x3 matrix but arranged as 9-vector"""
    e=linalg.eigvals([[1 + s[0], s[1]], [s[3], 1 + s[4]]])
    if(e[0]<e[1]):
        return linalg.eig([[1 + s[0], s[1]], [s[3], 1 + s[4]]])[1][0]
    else:
        return linalg.eig([[1 + s[0], s[1]], [s[3], 1 + s[4]]])[1][1]

def least_compressive_eigenvector_xy(s):
    """"Direction showing the lowest compression, calculated as the eigenvector with the highest eigenvalue

            This function calculates the eigenvector with the lowest eigenvalue, restricting analysis to the xy-plane
            - **parameters**\n
                                `s` Strain tensor. This is the elements of a numericla 3x3 matrix but arranged as 9-vector"""
    e=linalg.eigvals([[1 + s[0], s[1]], [s[3], 1 + s[4]]])
    if(e[0]>e[1]):
        return linalg.eig([[1 + s[0], s[1]], [s[3], 1 + s[4]]])[1][0]
    else:
        return linalg.eig([[1 + s[0], s[1]], [s[3], 1 + s[4]]])[1][1]









