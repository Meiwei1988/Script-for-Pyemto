# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:40:16 2021

@author: Maywell2019
"""

import re
import os
import pyemto

f = open('results_new','r')
origin = []
for line in f:
    s = line.split()
    origin.append(s)

m = 'Hf'
n = []
for alloy in origin:
    element = re.findall('[A-Z][^A-Z]*', alloy[0])
    compostion = [alloy[1][i:i+2] for i in range(0, len(alloy[1]), 2)]
    if m in element:
        pass
    else:
        s = []
        s.append(element)
        s.append(compostion)
        s.append(float(alloy[2]))
        s.append(float(alloy[3]))
        n.append(s)

neck = ''
latpath = "/BIGDATA1/th_sz_kyu_1/weimei/Emto/structure"
EMTOdir = "/BIGDATA1/th_sz_kyu_1/weimei/Source/5.8.1/build1/"
folder = os.getcwd()

for new_cal in n:
    new_heasalloy = neck.join(new_cal[0])
    if not os.path.exists(new_heasalloy):
        os.mkdir(new_heasalloy)
        os.chdir(folder + '/' +new_heasalloy)
    else:
        os.chdir(folder + '/' +new_heasalloy)
    new_composition = neck.join(new_cal[1])
    os.mkdir(new_composition)
    emtopath = folder + '/' + new_heasalloy + '/' + new_composition
    HEAs = pyemto.System(folder=emtopath)
    HEAs.bulk(lat='bcc',
                jobname=new_composition,
                latpath=latpath,
                atoms=new_cal[0],
                concs=new_cal[1],
                splts=[0,0,0,0,0],
                amix=0.005,
                efmix=1.0,
                expan='S',
                sofc='Y',
                afm='P',         # Fixed-spin DLM calculation.
                iex=4,           # We want to use self-consistent GGA (PBE).
                niter=500,
                nz2=16,
                depth=0.940,
                efgs=0.200,
                hx=0.050,
                tole=1.0E-7,
                xc='PBE',
                ncpa=20,
                sws=new_cal[2],
                tfermi=500,
                dx=0.015,        # Dirac equation parameters
                dirac_np=1001,   # Dirac equation parameters
                nes=50,          # Dirac equation parameters
                dirac_niter=300) # Dirac equation parameters
    
    HEAs.elastic_constants_batch_generate(relax=True)
    os.chdir(folder)