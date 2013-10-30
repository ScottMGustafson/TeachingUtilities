from classUtils import *
from seat_randomizer import *
from stats import *

"""
a few other functions that may be useful as well as a main() function to 
put things together if so desired.
"""

def assign_seats(sections=None):
  """
  reads input data and then runs seat_randomizer
  """
  cfg_dict = read_config()

  try:
    if sections is None:  
      sections = cfg_dict["mysections"]  #split with _ as opposed to comma because everything gets sanitized
    tables = int(cfg_dict['tables'])
    seats  = int(cfg_dict["seats_per_table"])
  except KeyError:
    print('\nkey not in dict: check data.cfg.\n\n')
    raise
  except ValueError:
    print('\nvalues for seats and tables must be ints.\n\n')
    raise
  for item in sections:
    studentList = getData(cfg_dict,item)
    assert(len(studentList)>0)
    assert(tables!=0)
    assert(seats!=0)
    print(item+" "+str(len(studentList)))
    seat_randomizer(item,studentList,tables,seats,filename=str(item)+".txt")

  return

def printScores(assignments,sections=None):
  if sections is None:
    cfg_dict=read_config()
    sections = cfg_dict['mysections']
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

def getuname(sections=None,ext="@ucsd.edu"):
  """print out email friendly comma-separated string of all email addresses"""
  cfg_dict = read_config()
  if sections is None:  
    try:
      sections = cfg_dict["mysections"]
    except KeyError:
      print("key: \'mysections\' does not exist")
      raise
    except:
      print("exception: key is "+cfg_dict["mysections"])
      raise
  for section in sections:
    print("\n\n  "+str(section))
    studentList = getData(mySection=section)
    string = ''
    for item in studentList:
      string+=item.username+ext+","
    print(string)

from matplotlib.pylab import *

def plotStats(data,maxVal):
  binsize = float(maxVal)/20.
  n, bins, patches = hist(data, bins=25, histtype='bar')
  setp(patches, 'facecolor', 'g', 'alpha', 0.75)
  x = [val for val in range(0,int(maxVal),int(binsize)) ]
  figure()
  show()
  
def getTotals(section):
  studentlist, cfg_dict = init(section)
  print len(studentlist)
  data = []
  for student in studentlist:
    data.append(getTotal(student,cfg_dict))
  return data

def runAll():
  """
  just an example of how to run a few of these functions
  """

  #getuname()
  assign_seats() 
  #printScores( ['quiz04', 'prelab04', 'inlab04', 'conclusion03'] )

if __name__ == '__main__':
  runAll()
      
    
