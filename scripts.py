from classUtils import *
from seat_randomizer import *
from stats import *

"""
a few other functions that may be useful as well as a main() function to 
put things together if so desired.
"""

def assign_seats():
  """
  reads input data and then runs seat_randomizer
  """
  cfg_dict = read_config()

  try:
    #sections = cfg_dict["mysections"].split('_')  #split with _ as opposed to comma because everything gets sanitized
    sections = ['784952','784964']
    tables = int(cfg_dict['tables'])
    seats  = int(cfg_dict["seats_per_table"])
  except KeyError:
    print('\nkey not in dict: check data.cfg.\n\n')
    raise
  except ValueError:
    print('\nvalues for seats and tables must be ints.\n\n')
    raise
  except: raise
  for item in sections:
    studentList = getData(cfg_dict,item)
    assert(len(studentList)>0)
    assert(tables!=0)
    assert(seats!=0)
    seat_randomizer(item,studentList,tables,seats,filename=str(item)+".txt")
  return

def printScores(sections,assignments):
  for section in sections:
    print("\nsection: "+str(section))
    print("===========================================")
    for assignment in assignments:
      scores = getStats(assignment,section)
      string = "  %(asgn)-12s  %(mean)-6.3lf  +/-  %(std)-6.3lf"%{'asgn':assignment, 'mean':scores[0], 'std':scores[1]}
      print(string)
    scores = getOverallStats(section)
    string = "  totals:       %(mean)-6.3lf  +/-  %(std)-6.3lf"%{'mean':scores[0], 'std':scores[1]}
    print("-------------------------------------------")
    print(string)
  return

def getuname(sections,ext="@ucsd.edu"):
  """print out email friendly comma-separated string of all email addresses"""
  for section in sections:
    print("\n\n  "+section)
    studentList = getData(mySection=section)
    string = ''
    for item in studentList:
      string+=item.username+ext+","
    print(string)

def main():
  
  sections = ['784952','784964']
  assignments = ['quiz01','prelab01','inlab01','conclusion01','quiz02','prelab02','inlab02']
  getuname(sections)

  assign_seats() 
  printScores(sections, assignments)
  

if __name__ == '__main__':
  main()
      
    
