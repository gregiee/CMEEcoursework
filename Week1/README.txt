Yuchen's CMEE Coursework Repository - Week 1

This week's lecture covers Introduction, Unix, Shell scripting, Version Control with Git,Scientific documents with LATEX

Most of the contents under this week's folder is for Unix and Shell scripting lectures and practicles.

/Data folder contains 3 fasta data file which are used for scripts.
/Code data contains 12 scripts:

- Code/UnixPrac1.txt
	contains 5 scripts that can be copied and run in the terminal under the ../Code path, and they do the following:
		Count how many lines are in each file
	    Print everything starting from the second line for the E. coli genome
	    Count the sequence length of this genome
	    Count the matches of a particular sequence, "ATGC" in the genome of E. coli
	    Compute the AT/GC ratio. That is, the (A+T)/(G+C) ratio.
	data are stored under Data folder and called using relative path in the script.

- Code/boilerplate.sh
 	print out text to terminal

- Code/tabtocsv.sh
	create a new csv file based on input tab seperated file in the same directory.
	can be run with a file path input.

- Code/variables.sh
	shows how to read and assign value(s) from user's input.

- Code/MyExampleScript.sh
	shows how to print using variables.

- Code/CountLines.sh
	counts lines in a file, providing a file path is provided when runing the script.

- Code/ConcatenateTwoFiles.sh
	Merge two files to create a new file, need to run with 2 exisiting and 1 new file path.

- Code/tiff2png.sh
	covert .tiff file to .png file, need to install imagemagic first and provide file path.

- Code/csvtospace.sh
	create space seperated file based on given csv files.
	need file path to run and will save the new file in the same directory.

- Code/FirstExample.tex
	create a latex file.

- Code/FirstBiblio.bib
	create a bibliography file competable with latex.

- Code/CompileLaTeX.sh
	bash script to compile latax and bibliography into a pdf.