import csv
from sys import exit
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
      if len(lst.keys())==0: 
        print("\n\n"+repr(lst))
        print("is empty\n\n")
        raise EmptyDict
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

def defaultfilepath(cfgpath=os.path.join('Data','data.cfg')):
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

#@lenchecker
def read_config(filestream = open(defaultfilepath())):
  """
  read the configuration file, by default data.cfg.
  returns a dict containing relevant config info.
  """
  cfg_dict = {}
  f = filestream
  for line in stringtools.non_blank(f):
    temp = line.split('::')
    if not '::' in line or len(temp)>2: 
      raise BadFormatting(line)
    elif len(re.findall(r'\$',line.split()[1]))>1:
      raise BadFormatting(line+": should only have 1 \'$\' character.")   
    elif 'mysections' in temp[0]:
      key = 'mysections'  
      value=[item.strip() for item in temp[1].split(',')]
    elif 'csvfile' in temp[0]:
      key = temp[0].strip()
      temp[1] = temp[1].strip()
      value = os.path.abspath(temp[1])
      assert(os.path.isfile(value))
    else:
      key  = stringtools.sanitize(temp[0])
      value= stringtools.sanitize(temp[1])
    cfg_dict[key] = value  
  print cfg_dict
  return cfg_dict
  
def getData(cfg_dict=read_config(), mySection=None,verbose=False):  #this code only works if csv.reader returns a list
  """
  input a csv file
  output a list of student instances
  """

  assert(os.path.isfile(cfg_dict['csvfile'])) 
  
  stringtools.stripExtraCommas(cfg_dict['csvfile'])
  f = open(cfg_dict['csvfile'], 'r')
  gradeFile = list(csv.reader(f, delimiter=',', quotechar='\"'))
  assert(type(gradeFile)==list)

  head = stringtools.sanitizeKeys(cfg_dict,gradeFile[0])
  assert(len(head)==6)
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

