#!/bin/bash
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=1:mem=1gb
module load anaconda3/personal
echo "R is about to run"
cp $HOME/YY5819_HPC_2019_main.R $TMPDIR
R --vanilla < $HOME/YY5819_HPC_2019_cluster.R
mv YY5819* $HOME/test
echo "R has finished running"
# this is a comment at the end of the file