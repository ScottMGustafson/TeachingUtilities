TeachingUtilites
==============================

some helpful tools I've developed to assist with grading and contacting students

What it does:
--------------------------
it parses a csv file (data from a grading spreadsheet) to extract relevant 
information and then has functions to perform several tasks such as:
--randomize a seating chart
--harvest all email addresses
--calculate class statistics

Notes on input:
--------------------------
follow the instructions in data.cfg on configuration info. Right now, all info 
is set up such that an assignment number will be replaced with the character '$'
so if the header to the spreadsheet contains this or a comma ',' then these need
to be removed since they may break the program. I have not yet added 
functionality to check for this from the beginning.

Examples:
---------------------------
under scripts.py I already have a few useful examples that can be run (editting 
them to your needs of course).

