import csv
import sys
import re
import os
from collections import namedtuple
from pkg_resources import resource_stream
import stringtools

class AllErrors(Exception):
  def __init__(self,msg=''):
    self.msg = msg

class FileDNE(AllErrors):
  def __str__(self):
    return self.msg+' does not exist'

class EmptyDict(AllErrors):
  def __str__(self):
    return(' dict is empty:'+self.msg)

class EmptyString(AllErrors):
  def __str__(self):
    return(' string is empty:'+self.msg)

class EmptyList(AllErrors):
  def __str__(self):
    return(' List is empty:'+self.msg)

class TooManyArgs(AllErrors):
  def __init__(self,expected=None,received=None):
    self.received = received
    self.expected = expected
    self.args = [item for item in args]
  def __str__(self):
    if self.expected and self.received:
      return(self.msg+"\nexpected: "+repr(self.expected)+"\nreceived: "+repr(self.received)+"\n")  
    elif self.received and self.expected is None:
      return(self.msg+"\nreceived: "+repr(self.received)+"\n")
    elif self.expected and self.received is None:
      return(self.msg+"\nreceived: "+repr(self.expected)+"\n")
    else:
      return('wrong number of args:'+self.msg)

class BadFormatting(AllErrors):
  def __str__(self):
    return "Bad formatting in "+repr(self.msg)
    
def lenchecker(func):
  """checks that a list, string or dict is not zero in length"""
  def inner(*args,**kwargs):
    lst = func(*args,**kwargs)
    if type(lst) is dict:
      if len(lst.keys())==0: raise EmptyDict
    elif type(lst) is list:
      if len(lst)==0: raise EmptyList
    elif type(lst) is str:
      if lst=='': raise EmptyString
    return lst
        
  return inner

def printFields(obj):
  """
  print all the fields.  This is useful when the object fields seem screwy
  """
  for name in obj._fields:
    print name
  return

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
  return data_path

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
    else:
      key  = stringtools.sanitize(key)
      value= stringtools.sanitize(value)
    cfg_dict[key] = value  

  print("\n\n\n")
  print(cfg_dict)
  return cfg_dict
  
def getData(cfg_dict=None, mySection=None,verbose=False):  #this code only works if csv.reader returns a list
  """
  input a csv file
  output a list of student instances
  """
  if cfg_dict is None:
    cfg_dict = read_config()
  else:
    assert(type(cfg_dict) is dict)
    assert(type(mySection) is str)

  assert(type(cfg_dict) is dict)
  stringtools.stripExtraCommas(cfg_dict['csvfile'])
  f = open(cfg_dict['csvfile'], 'r')
  gradeFile = list(csv.reader(f, delimiter=',', quotechar='\"'))
  head = stringtools.sanitizeKeys(cfg_dict,gradeFile[0])
  student = namedtuple('Student',head)  #student class factory  

  if mySection is None:  
    return  [ student._make([stringtools.sanitize(item) for item in row]) for row in gradeFile[1:] ]

  else:
    studentList = []
    for row in gradeFile[1:]:
      if mySection in row:
        pupil=student._make([stringtools.sanitize(item) for item in row])   #a list counts as only one input...need to split it up
        pupil = pupil._replace(section=stringtools.numConvert(pupil.section))
        if pupil.section == mySection:
          studentList.append(pupil)
    return(studentList)

def init_it(section=None):
  print("running")
  cfgdict = read_config()
  if section is None:
    lst = []
    for item in cfgdict["mysections"]:
      lst+=getData(cfg_dict=cfgdicct,mySection=item)
  else:
    lst = getData(cfg_dict=cfgdict,mySection=section)
  if len(lst)==0: 
    raise EmptyList("student list is empty for section "+str(item))
  return lst, cfgdict

