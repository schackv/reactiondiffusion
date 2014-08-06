# -*- coding: utf-8 -*-
"""
Created on Tue May 20 10:48:17 2014

@author: jsve
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import RD

def savefig(fname,formats=('.png','.pdf'),**args):
    if save_flag:
        for ext in formats:
            plt.savefig(os.path.join(plot_dir,fname + ext),bbox_inches='tight',**args)


def saveim(A,B,it,suffix=''):
    if (np.mod(it,100)==0) & (it>0):        
        plt.figure() 
        plt.imshow(A)
        plt.colorbar()
        savefig('twodA_t{}{}'.format(it,suffix))
        plt.close()
        plt.figure() 
        plt.imshow(B)
        plt.colorbar()
        savefig('twodB_t{}{}'.format(it,suffix))
        plt.close()
        savebinary(A,B,it,suffix)
        print(it)

def savebinary(A,B,it,suffix=''):
    plt.figure()
    plt.imshow(A>4)
    savefig('twodA_bw_t{}{}'.format(it,suffix))
    plt.close()
    plt.figure()
    plt.imshow(B>4)
    savefig('twodB_bw_t{}{}'.format(it,suffix))
    plt.close()

def oned_figures():
    times = (500,3000,10000)
    scales = (0.25*0.03125, 0.03125)
    print(scales)
    
    for t in times:
        snum = 1
        for s in scales:
            A, B = RD.simulate_pattern(s=s,nt=t)
            print(t)
            
            plt.figure()
            plt.plot([0, len(A)],[4, 4],'k',label='$a_0=b_0$')
            plt.plot(A,color='r',label='a')
            plt.plot(B,color='b',label='b')
            plt.tight_layout()
            plt.xlabel('Cells')
            plt.ylabel('Concentration')
            plt.legend()
    #        plt.show()
            savefig('oned_t{}_s{}'.format(t,snum))
            snum +=1

def twod_figures():
       
    # Get frames out
    A, B = RD.simulate_pattern(p=(120,120),sigma0=0.001,s=0.03125,dt=0.5,nt=1000,plotfun=saveim)

    p = (120,120)
#     Get end result for dotty and stripy patterns
    nt = 5000
    k = 1
    for D_b in (0.0125,0.05):
        A, B = RD.simulate_pattern(p=p,D_b=D_b,sigma0=0.001,s=0.03125,dt=0.5,nt=nt)
        saveim(A,B,nt,'_Db{}'.format(k))
        k+=1
    
    # Combine dotty and stripy
    nt = 10000
    D_B = RD.stretch_for_image( (0.0125,0.05), p)
    A, B = RD.simulate_pattern(p=(120,120),D_b=D_B,sigma0=0.001,s=0.03125/2,dt=0.5,nt=nt)
    saveim(A,B,nt,'_Dbstretch')
    print(D_B.shape)
    
    # Anisotropic diffusion
    nt = 10000
    for idx, deltaA in enumerate([-0.95,0.95]):
        A, B = RD.simulate_pattern(p=(120,120),D_b=0.01,deltaA=deltaA,
                                        sigma0=0.001,s=0.03125/8,dt=0.7,nt=nt)
#        plt.figure()
#        plt.imshow(A)
#        plt.show()
        saveim(A,B,nt,'_anisotropy{}'.format(idx))


    
    
    
if __name__=='__main__':
    # Run all experiments
    save_flag = True
    plot_dir = 'plots'
    try:
        os.mkdir(plot_dir)
    except:
        pass
    oned_figures()
    twod_figures()
    
    

#twod_figures()
