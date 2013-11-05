from classUtils import *
import scipy.stats as stats
from stringtools import *
import numpy as np
from sys import exit

"""
Some functions to get relevant statistics
"""


def init(section):
  cfg_dict=getDict_hack()
  #cfg_dict = read_config()
  lst = getData(cfg_dict,section)
  if lst is None or len(lst)==0:
    print(str(section)+" has no students")
    exit()
  else:
    return lst, cfg_dict

def getStats(assignment,section):
  """
  input:  assignment name (str), section number
  output: tuple of (mean, stdev).  returns None on failure
  """
  studentlist, cfg_dict = init(section)
  try:
    assert(isassn(cfg_dict,assignment))
  except AssertionError:
    print(assignment+" is not in dict")
    return None
  except:
    raise
  data = []
  for item in studentlist:

    try:
      temp = getattr(item, assignment)
    except:
      for name in item._fields:
        if assignment==name:
          print "the offending value: "+name+" = "+getattr(item,name)
      raise

    try:
      data.append(float(temp))
    except ValueError:  #item is presumably None
      if temp is None or temp=='':
        pass
      else:
        print(temp)
        raise

  return np.mean(data), np.std(data)

def getAssignments(cfg_dict):
  """from cfg_dict returns a list of those keys that are assignments"""
  assn = []
  for item in cfg_dict.keys():
    if "$" in item:
      assn.append(item)
  return assn
  
def isassn(cfg_dict,string):
  """tests if a given string is an assignment.  returns True if it is"""
  if rm_nums_replace(string) in getAssignments(cfg_dict):
    return True
  else:
    return False
  
def getOverallStats(section):
  """
  input:  section
  output:  tuple of (mean, stdev)
  """
  lst, cfg_dict = init(section)
  data = []
  for item in lst:
    data.append(getTotal(item,cfg_dict))
  return np.mean(data),np.std(data)

def getTotal(student,cfg_dict):
  """
  get the totals for a student.
  input:
  ----------------------------
  student: an instance of Student
  cfg_dict: the configuration dictionary defined in classUtils.read_config

  output:
  ----------------------------
  score summed over all assignments
  
  """
  summ=0
  for name in student._fields:
    if isassn(cfg_dict,name):
      try:      
        summ+=float(getattr(student,name))
      except ValueError:
        try:
          assert(isassn(cfg_dict,name))
        except AssertionError:
          print(name+" is not an assignment, but should be.")  
          raise  
      except:
        raise
  return summ
  
