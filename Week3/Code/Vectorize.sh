#!/bin/bash
# Author: Yuchen Yang (yy5819@ic.ac.uk)

echo -e "=================================="
echo -e "time spent for Vectorize1.R: \n"
echo -e "=================================="
Rscript Vectorize1.R
echo -e "=================================="
echo -e "time spent for Vectorize1.py: \n"
echo -e "=================================="
python3 Vectorize1.py
echo -e "=================================="
echo -e "time spent for Vectorize2.R: \n"
echo -e "=================================="
Rscript Vectorize2.R
echo -e "=================================="
echo -e "time spent for Vectorize2.py: \n"
echo -e "=================================="
python3 Vectorize2.py