import csv
#import sys
import re
import os
#from collections import namedtuple
#from pkg_resources import resource_stream
import stringtools
from error import *

def defaultfilepath(cfgpath=os.path.join('Data','data.cfg')):  #is this a source of issues?
  """get the path to the default location for the data directory"""
  data_path, _ = os.path.split(__file__)
  data_path_lst = data_path.split(os.sep)
  data_path = (os.sep).join(data_path_lst[0:-1])
  data_path = os.path.join(data_path,cfgpath)
  try:
    if not os.path.isfile(data_path):
      raise FileDNE(data_path)
  except FileDNE:
    raise
  return os.path.abspath(data_path)

@lenchecker
def read_config(filestream = open(defaultfilepath())):
  """
  read the configuration file, by default data.cfg.
  returns a dict containing relevant config info.
  """
  cfg_dict = {}
  for line in stringtools.non_blank(filestream):
    key, value = line.split('::')
    if 'mysections' in key:
      key = 'mysections' 
      value=[item.strip() for item in value.split(',')]
    elif 'csvfile' in key:
      key = 'csvfile'
      value = os.path.abspath(value.strip())
      assert(os.path.isfile(value))
    elif 'email_text' in key:
      key = 'emailtext'
      value = os.path.abspath(value.strip())
      assert(os.path.isfile(value))
    else:
      key  = stringtools.sanitize(key)
      value= stringtools.sanitize(value)
    cfg_dict[key] = value  
  return cfg_dict

def getData(cfg_dict=None, mySection=None,verbose=False):  #this code only works if csv.reader returns a list
  """
  input a csv file
  output a list of student instances
  """
  if not cfg_dict: cfg_dict = read_config()
  stringtools.stripExtraCommas(cfg_dict['csvfile'])
  gradeFile = csv.DictReader(open(cfg_dict['csvfile']), delimiter=',', quotechar='\"')

  old_keys = gradeFile.fieldnames
  new_keys = stringtools.sanitizeKeys(cfg_dict,old_keys) 
  
  assert(type(new_keys) is list and type(old_keys) is list)

  studentList = []
  
  for row in gradeFile:
    for i in range(0,len(old_keys)): 
      row[ new_keys[i] ] = row.pop(old_keys[i]) 

    if mySection is not None:
      try:
        tmp1 = int(mySection)
        if row['section'] is None:   #this will happen when a student has no listed section
          continue
        else:
          tmp2 = int(row['section'])
      except ValueError, TypeError:
        tmp1 = stringtools.numConvert(str(mySection))
        tmp2 = stringtools.numConvert(str(row['section']))
      if tmp1==tmp2:
        studentList.append(row)
    else:
      studentList.append(row)
  return studentList

def init_it(section=None):
  cfgdict = read_config(open(os.path.abspath('Data'+os.sep+'data.cfg')))
  if section is None:
    lst = []
    for item in cfgdict["mysections"]:
      lst+=getData(cfg_dict=cfgdict,mySection=item)
  else:
    lst = getData(cfg_dict=cfgdict,mySection=section)
  if len(lst)==0: 
    raise EmptyList("student list is empty for section "+str(section))
  return lst, cfgdict

