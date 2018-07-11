#!/bin/bash -l                                                                                                                                                                                              
#                                                                                                                                                                                                           
#SBATCH --account=s710                                                                                                                                                                                      
#SBATCH --job-name="gevolution"                                                                                                                                                                             
#SBATCH --time=24:00:00                                                                                                                                                                                     
#SBATCH --partition=normal                                                                                                                                                                                  
#SBATCH --ntasks=16                                                                                                                                                                                       
#SBATCH --ntasks-per-node=12                                                                                                                                                                                
#SBATCH --cpus-per-task=1                                                                                                                                                                                   
#SBATCH --constraint=gpu                                                                                                                                                                                    
#SBATCH --output=gevolution.%j.o                                                                                                                                                                            
#SBATCH --error=gevolution.%j.e                                                                                                                                                                             
#======START=====                                                                                                                                                                                           
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
module load daint-gpu
module load cray-hdf5-parallel
module load fftw
module load GSL
echo "The current job ID is $SLURM_JOB_ID"
echo "Running on $SLURM_NNODES nodes"
echo "Using $SLURM_NTASKS_PER_NODE tasks per node"
echo "A total of $SLURM_NTASKS tasks is used"
srun -n $SLURM_NTASKS --ntasks-per-node=$SLURM_NTASKS_PER_NODE -c \
$SLURM_CPUS_PER_TASK ./gevolution -n 4 -m 4 -s settings_small.ini
