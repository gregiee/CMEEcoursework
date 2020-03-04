#!/bin/bash
# Author: yuchen.yang19@imperial.ac.uk
# Script: run_MiniProject.sh
# Runs the whole project, right down to compilation of the LaTeX  document.

#data preparation
echo "running 1_data_preparation.py"
python3 1_data_preparation.py
echo "done"

#model fitting
echo "running 2_fitting.py"
python3 2_fitting.py
echo "done"

#plotting and analysis
echo "running 3_plot_analysis.R"
Rscript 3_plot_analysis.R
echo "done"

#compile latex
echo "running CompileLaTeX.sh"
bash CompileLaTeX.sh minireport
echo "done"