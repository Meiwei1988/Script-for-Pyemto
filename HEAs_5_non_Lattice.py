#!/usr/bin/python

# Calculate the equilibrium volume and bulk modulus of
# fcc CoCrFeMnNi high-entropy alloy using DLM.

# !!! NOTE !!!
# This script DOES NOT automatically start running
# the batch scripts. It only generates the input files
# and batch scripts which the user runs by themselves
# !!! NOTE !!!

import pyemto
import os
import numpy as np
import itertools

# It is recommended to always use absolute paths
folder = os.getcwd()                 # Get current working directory.
latpath = "/BIGDATA1/th_sz_kyu_1/weimei/Emto/structure"   # Folder where the structure output files are.
EMTOdir = "/BIGDATA1/th_sz_kyu_1/weimei/Source/5.8.1/build1/"

atom_lib = ['Ti','V','Cr','Zr','Nb','Mo','Hf','Ta','W']
#atom_lib = ['Ti','V','Cr','Zr','Nb','Mo']

quinary_combination=list(itertools.combinations(atom_lib,5))

sws = np.linspace(2.90,3.20,12) # 11 different volumes from 2.5 Bohr to 2.7 Bohr

m1 = [20,20,20,15,25]
m2 = []
for i in itertools.permutations(m1):
#    print(i)
    m2.append(i)

from collections import Counter

m3 = dict(Counter(m2))
m4 = []
for key,value in m3.items():
    m4.append(list(key))

# Set KGRN and KFCD values using a for loop.
# Use write_input_file functions to write input files to disk:
neck = ''
#ncpu = 1
# slurm_options=['#SBATCH -N 1',
               # '#SBATCH -n {0}'.format(ncpu),
               # '#SBATCH --ntasks-per-node=4',
               # 'ulimit -s unlimited',
               # 'module load compiler/intel/ips2018/u1 mkl/intel/ips2018/u1 mpi/openmpi/ips2018/u1/3.0.5',
               # 'export OMP_NUM_THREADS=${SLURM_NTASKS_PER_NODE}',
               # 'export OMP_STACKSIZE=6400m']
               
for j in range(len(quinary_combination)):
    foldername = neck.join(list(quinary_combination[j]))
    os.chdir(folder)
    if os.path.exists(foldername):
        print(foldername+" is exists!")
        pass
    else:
        os.system('mkdir '+foldername)
        os.chdir(folder+'/'+foldername)
        for composition in m4:
            composition_new = [str(x) for x in composition]
            jobname = neck.join(composition_new)
            if os.path.exists(jobname):
                #print(jobname+" is exists!")
                pass
            else:
                print(jobname)
                emtopath = folder+"/"+foldername+"/"+jobname  # Folder where the calculations will be performed.
                heaname = jobname + str(j)
                heaname = pyemto.System(folder=emtopath)
                for i in range(len(sws)):   
                    heaname.bulk(lat='bcc',
                                jobname=jobname,
                                latpath=latpath,
                                atoms=list(quinary_combination[j]),
                                concs=composition,
                                splts=[0,0,0,0,0],
                                sws=sws[i],
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
                                hx=0.200,
                                tole=1.0E-7,
                                ncpa=20,
                                nkx=29,
                                nky=29,
                                nkz=29,
                                # ntry=6,
                                tfermi=500,
                                runtime='4:00:00',
                                # slurm_options=slurm_options,
                                dx=0.015,        # Dirac equation parameters
                                dirac_np=1001,   # Dirac equation parameters
                                nes=50,          # Dirac equation parameters
                                dirac_niter=300) # Dirac equation parameters
                    
                    heaname.emto.kgrn.write_input_file(folder=emtopath)
                    heaname.emto.kfcd.write_input_file(folder=emtopath)
                    heaname.emto.batch.write_input_file(folder=emtopath)
                #jobnames = heaname.lattice_constants_batch_generate(sws=sws)
                #jobIDs = heaname.submit_jobs(jobnames,folder=emtopath)
                #heaname.wait_for_jobs(jobIDs)
                #sws0, B0, e0, grun = heaname.lattice_constants_batch_calculate(sws=sws)
                
                #f=open(emtopath+"/"+jobname+".a-e","a")
                #energies = []
                #for m in range(len(sws)):
                #    name = jobname + '_' + str('%f'%sws[m])
                #    energy = heaname.get_energy(jobname=name,func="PBE")
                #    f.write(' '.join([str(sws[m]),str(energy)])+'\n')
                #f.close()
                    
                #f = open("results_new","a")
                #f.write(jobname+' '+str(sws0)+' '+str(B0)+' '+str(e0)+' '+str(grun)+'\n')
                #f.close()