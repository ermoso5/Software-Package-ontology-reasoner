Software-Package-ontology-reasoner
==================================

A tool to build an ontology from a textual file describing packages and trace dependencies between them.

Required software
----------------------------------

  1. Python 3.x 
  2. Prolog (can be downloaded from http://www.swi-prolog.org/download/stable)

How to run
----------------------------------

  1. Open config.conf file. Adapt the variables to your environment.
      1. swipl_loc = \path\to\swipl.exe - usually C:\Program Files (x86)\swipl\bin\swipl.exe
      2. packageFile = \path\to\the\text\file\containing\textual\descriptions\of\packages
      3. ontology_loc = \absolute\path\to\the\downloaded\project\\resources\\output.owl
    
    Other variables should remain unchanged. 
  2. Run wrapper.py. Choose an option from the menu according to what you need. To obtain information about a specific package choose option 3 and input the name of the package. To get information about all the packages choose option 4.
  
