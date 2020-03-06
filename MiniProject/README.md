# MiniProject
model fitting

## Author
Yuchen Yang (yy5819@imperial.ac.uk)

    ```console
    ## results are already uploaded in case there's anything wrong with it..
    ## but!
    ## could also run the whole thing by doing and check if it works:
    bash run_MiniProject.sh
    ```

## Requirements
R Version Used: 3.4.4
Required R packages:
    -ggplot2, reshape2
    
Python Version Used: 3.5.2
Required Python packages:
    -pandas, math, numpy, lmfit

***

## structure
there are 4 directories.
- **Data** 
    ```
    where original and processed data are stored
    ```
- **Code** 
    ```
    where scripts are, also where the compiled .tex pdf is
    ```
- **Results** 
    - **allPlots** 
    ```
    where plot for every fitting are stored
    ```
    - **anaPlots**
    ```
    where plots for analysis are stored
    ```
- **Sandbox** 


### detailed script description
- 1_data_preparation.py
    ```
    initial data preparation
    ```
- 2_fitting.py
    ```
    does the fitting using limfit and store the resutls in .csv
    ```
- 3_plot_analysis.R
    ```
    plot all fit result and conduct stats analysis
    ```
- CompileLaTeX.sh
    ```
    bash to compile the final Latex
    ```
- run_MiniProject.sh
    ```
    main script, glue everything together
    ```
- minireport.tex, minireport.bib
    ```
    report in latex and ref
    ```
