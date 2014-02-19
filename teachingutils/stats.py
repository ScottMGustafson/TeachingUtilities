from classUtils import *
import scipy.stats as stats
from stringtools import *
import numpy as np
from sys import exit

"""
Some functions to get relevant statistics
"""
def getStats(assignment,section):
  """
  input:  assignment name (str), section number
  output: tuple of (mean, stdev).  returns None on failure
  """
  studentlist, cfg_dict = init_it(section)
  try:
    assert(isassn(cfg_dict,assignment))
  except AssertionError:
    print(assignment+" is not in dict")
    return None
  except:
    raise
  data = []


  for item in studentlist:
    temp = item[assignment]
    try:
      data.append(float(temp))
    except ValueError:  #item is presumably None
      if temp is None or temp=='':
        pass
      else:
        print(assignment+": "+str(temp))
        raise

  return np.mean(data), np.std(data)
  
def getAssignments(cfg_dict):
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
  lst, cfg_dict = init_it(section)
  data = []
  for item in lst:
    data.append(getTotal(item,cfg_dict))
  try:
    return np.mean(data),np.std(data)
  except:
    print data
    raise

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
  summ = 0.
  for item in student.keys():
    if isassn(cfg_dict,item):
      try:
        summ+=float(student[item])
      except ValueError, TypeError:
        pass
  return summ
  
