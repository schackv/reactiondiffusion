# -*- coding: utf-8 -*-
"""
Created on Tue May 20 16:45:14 2014

@author: jsve
"""
import numpy as np
from scipy.ndimage.filters import convolve

def diffuse(X,deltaA=0):
    """Calculate the diffusion of the 1D or 2D array X to neighboring elements.
    The diffusitivity is specified by a discrete approximation to the Laplacian.
    Anistropy is introduced for deltaA\neq 0 and X.ndim == 2."""
    
    if len(X.shape)==1:
        Xpad = np.pad(X,1,mode='wrap')
        dX = np.convolve(Xpad,[1, -2, 1],mode='valid')
    else:
        K = np.array([(0,1,0),(1,-4,1),(0,1,0)])
        if deltaA!=0:
            theta = [0,np.pi*0.5]   # Horizontal and vertical
            d_antr = anisotropy(theta,deltaA)
            hor = d_antr[0]
            vert = d_antr[1]
            D_antr = np.array([(0, vert, 0),
                               (hor,0.5*(hor+vert), hor),
                                (0, vert, hor)])
            K = D_antr*K
            K = K/abs(K[1,1])*4
            assert np.sum(K)**2 < 1e-5, "Diffusion in and out is not balanced (sum={})".format(np.sum(K))
            
        dX = convolve(X,K,mode='wrap')
#        dX = laplace(X,mode='wrap')
    return dX


def anisotropy(theta,delta):
    """Anisotropy function due to Shoji (2003) and Allen (2010).
    theta is angle of diffusion and delta is the anisotropy magnitude."""
    return 1/np.sqrt(1-delta * np.cos(2*theta))

def stretch_for_image(limits,shape):
    """Generate a numpy array of size shape
    with values along axis 0 stretched linearly between limits[0] and limits[1].
    The values along each row are the same."""
    
    x = np.linspace(0,1,num=shape[0])

    values = x * (limits[1]-limits[0]) + limits[0]
    
    X = np.tile(values[:,np.newaxis],(1,shape[1]))
    return X

def simulate_pattern(p=(120,),sigma0=0.05,dt=1,D_a=0.25,D_b=0.0625,s=0.03125,nt=2000,deltaA=0,plotfun=None):
    """Simulate the pattern formation mechanism proposed by Turk (1991)
    with the possibility of anisotropy by letting deltaA be different from 0"""
    
    # Model specific parameters
    a0 = b0 = 4
    
    # Initialize model
    beta = 12 + sigma0 * np.random.randn(*p) # Initial level plus pertubations
    A = np.ones(p)*a0  # Initial concentration of A
    B = np.ones(p)*b0
    
    for i in range(nt):
        dA = s * (16 - A*B)         + D_a * diffuse(A,deltaA=deltaA)
        dB = s * (A*B - B - beta)   + D_b * diffuse(B)
        
        A = np.maximum(0,A + dt*dA)
        B = np.maximum(0,B + dt*dB)

        if plotfun:
            plotfun(A,B,i)
            
    return A, B