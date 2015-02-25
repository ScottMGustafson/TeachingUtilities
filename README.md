
TeachingUtilites
==============================
Some helpful tools I've developed to assist with grading and contacting students.  This was written specifically for my TA duties at UC San Diego.

What it does:
--------------------------
it parses a `.csv` file (data from a grading spreadsheet) to extract relevant 
information and then has functions to perform several tasks such as:

* randomize a seating chart
* harvest all email addresses and send mass emails to students
* calculate class statistics

Setting it up:
--------------
* Put a `.csv` file in the same directory as the source and make sure it has the same name as what is stated in `configdata.cfg`.  See the first bullet-point in Known Issues and work-arounds to prevent an existing bug from crashing the code.
    * *specifically for UCSD courses, this `.csv` file can be gotten from TED.  Go to the grade center --> full grade center --> work offline --> download and for "delimiter type" choose "comma".*
* read `configdata.cfg` and fill in all the relevant data for you.  Header data should match exactly.
* adjust `scripts.py` to your needs.  In other words, comment/uncomment relevant functions calls in `scripts.py`. 

Running it:
-----------
run as

`python scripts.py`

If you run into any issues, please let me know.


Known Issues and work-arounds (as of 2014-01-20):
-------------------------------------------------
* When first running with a `.csv` file specifically from UCSD TED, there is some mysterious control character before the first visible character that I can't figure out.

 * **Work-around:** Delete it manually in a text editor.  (That is to say, go to the first visible character and then delete whatever invisible stuff is in front of it.  I use gedit on ubuntu 13.10 and this works)

Notes on input:
--------------------------
Follow the instructions in configdata.cfg on configuration info. Right now, all info 
is set up such that an assignment number will be replaced with the character '?'
so if the header to the spreadsheet contains this or a comma ',' then these need
to be removed since they may break the program. I have not yet added 
functionality to check for this from the beginning.

Examples:
---------------------------
Under scripts.py I already have a few useful examples that can be run (editing 
them to your needs of course).

