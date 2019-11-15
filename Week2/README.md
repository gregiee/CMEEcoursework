# Week2
covers `Python` basics

## Author
Yuchen Yang (yy5819@imperial.ac.uk)

***

## structure
there are 4 directories.
- **Data**
- **Code** 
- **Results** 
- **Sandbox** 

### detailed script description
- basic_io1.py
    ```python
    ##open and print the test.txt in sandbox in two different ways
    ```
- basic_io2.py
    ```python
    ##adding content to the end of testout.txt 
    ```
- basic_io3.py
    ```python
    ##dump dict into pickle file and load pickle file into dict 
    ```
- basic_csv.py
    ```python
    ## manipulate CSV files and create new csv files based on given files
    ```
- cfexercises1.py
- cfexercises2.py  
    ```python
    ##conditions and loops examples
    ##cfexercises1 modified as practicle requesteds
    ```
- oaks.py
    ```python
    ##finding oaks in lists of data using for loop and comprehensions.
    ```
- scope.py
    ```python
    ##examples on variable scope
    ```
- boilerplate.py
    ```python
    ##the very basic of python programme:
    ##the shebang, docstring, internal variables, functions and modules...
    ```
- using_name.py
    ```python
    ##understanding how main and name works
    ```
- sysargv.py
    ```python
    ##to understand sys.argv
    ```
- control_flow.py
    ```python
    ##control flow tools such as if else
    ```
- loops.py
    ```python
    ##example for loops
    ```
- lc1.py
- lc2.py
- dictionary.py
- tuple.py
    ```python
    ##practicles on list comprehensions and for loops
    ```
- test_control_flow.py
    ```python
    ##introducing unit testing with doctet
    ```
- debugme.py
    ```python
    ##example script to debug
    ``` 
- align_seqs.py
    ```python
    ## takes the DNA sequences as an input from a single external file 
    ## and saves the best alignment along with its corresponding score 
    ## in a single text file (your choice of format and file type) to an appropriate location. 
    ```
- align_seqs_fasta.py
    ```bash
    ##take explict inputs or use default fasta files and match their squences, 
    ## output one best result:
    python align_seqs_better.py ../Data/407228326.fasta ../Data/407228412.fasta
    ```
- align_seqs_better.py
    ```bash
    ##take explict inputs or use default fasta files and match their squences, 
    ## output all best results in results folder:
    python align_seqs_better.py ../Data/407228326.fasta ../Data/407228412.fasta
    ```
 - oaks_debugme.py
    ```python
    ## found and fixed the typo bug, added unit test to make sure the function
    ## work as expected, add regex rules to take ambiguous inputs, add codes 
    ## to deal with csv header for file read and write. 
    ```
