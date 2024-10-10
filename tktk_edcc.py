#!/usr/bin/env python3

import argparse
import itk
import numpy as np
import matplotlib.pyplot as plt

import torch.nn as nn
import torch

def laplace_p(p,sigma, spacing,size):
    return np.dot(p,spacing*np.array([np.exp(sigma*s) for s in np.linspace((-size*spacing+spacing)/2,(size*spacing-spacing)/2,size)]))


class fast_eDCC_loss(nn.Module):
    def __init__(self):
        super(fast_eDCC_loss, self).__init__()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.spacing = 4.7952
        self.mu0 = 0.013
        self.Nprojs = 120
        self.array_theta_i = torch.linspace(0, 2 * torch.pi, self.Nprojs + 1)[:-1].to(self.device)
        self.array_theta_j = self.array_theta_i.roll(-30)
        # self.array_theta_j = torch.zeros_like(self.array_theta_i)
        self.size = 128
        self.linspace = torch.linspace((-self.size*self.spacing+self.spacing)/2,
                                        (self.size*self.spacing-self.spacing)/2,self.size).to(self.device)

    def forward(self,projs):
        sigma_ij =  self.mu0 * torch.tan((self.array_theta_i - self.array_theta_j) / 2)
        x_i = torch.exp(sigma_ij[:,None]*self.linspace[None,:])*self.spacing
        P_i = (projs * x_i[None, :, None, :]).sum(-1)

        sigma_ji =  self.mu0 * torch.tan((self.array_theta_j - self.array_theta_i) / 2)
        x_j = torch.exp(sigma_ji[:,None]*self.linspace[None,:])*self.spacing
        P_j = (projs.roll(-30,dims=1) * x_j[None, :, None, :]).sum(-1)
        # P_j = (projs[:,0:1,:,:] * x_j[None, :, None, :]).sum(-1)
        edcc_fast_before_mean = 2 * torch.abs(P_i - P_j) / (P_i + P_j)
        print(edcc_fast_before_mean.shape)

        edcc_fast = torch.sum(edcc_fast_before_mean[~edcc_fast_before_mean.isnan()])/edcc_fast_before_mean.numel()
        return edcc_fast,torch.nanmean(edcc_fast_before_mean,dim=(0,2)).detach().cpu().numpy()

def main():
    print(args)
    edcc_loss = fast_eDCC_loss()
    fig,ax =plt.subplots()
    for fn in args.projs:
        projs = itk.imread(fn)
        spacing =np.array(projs.GetSpacing())[1]
        array_projs = itk.array_from_image(projs)
        size = projs.shape[1]
        N_projs = array_projs.shape[0]

        tensor_projs = torch.Tensor(array_projs)[None,:,:,:].to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

        lss,eddc_i = edcc_loss(tensor_projs)

        array_theta = np.linspace(0,2*np.pi,N_projs+1)[:-1]
        lEij = []

        for i,thetai in enumerate(array_theta):
            print(i)
            # j =0
            j = (i+30) % 120
            thetaj = array_theta[j]
            err = 0
            for l in range(size):
                sigma_ij = args.mu0 * np.tan((thetai-thetaj)/2)
                sigma_ji = args.mu0 * np.tan((thetaj-thetai)/2)
                P_i = laplace_p(p=array_projs[i,l,:],sigma=sigma_ij,spacing=spacing,size=size)
                P_j = laplace_p(p=array_projs[j,l,:],sigma=sigma_ji,spacing=spacing,size=size)
                err += 2/size * np.abs(P_i-P_j)/(P_i+P_j) if (P_i+P_j!=0) else 0
            print(err)
            lEij.append(err)

        ax.plot(lEij, label=fn)
        ax.plot(eddc_i, label="fast"+fn)
        edcc1 = sum(lEij)/len(lEij)
        print(edcc1,edcc_loss)
    plt.legend()
    plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--projs", nargs='*')
    parser.add_argument("--mu0", type = float)
    args = parser.parse_args()

    main()
